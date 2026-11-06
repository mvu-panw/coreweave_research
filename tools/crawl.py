#!/usr/bin/env python3
"""Polite stdlib-only crawler: sitemap -> plain-text Markdown files + sources.csv.

Usage:
  python3 -I tools/crawl.py              # coreweave.com (blog/news/site) + docs.coreweave.com
  python3 -I tools/crawl.py --careers    # also snapshot the Greenhouse job board

Sources crawl concurrently (one thread per host, never two per host).
"""
import csv
import html
import json
import re
import subprocess
import sys
import threading
import time
import urllib.robotparser
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent / "corpus"
UA = "Mozilla/5.0 (PANW-SE account research; contact mikeovu@gmail.com)"
DELAY = {"coreweave.com": 1.5, "docs": 1.0, "careers": 1.0}  # seconds between requests, per host
SITEMAPS = {
    "docs": "https://docs.coreweave.com/sitemap.xml",
    "coreweave.com": "https://www.coreweave.com/sitemap.xml",
}
# ko/ja/fr are translations of the English docs; monolith-ai and model-distillation are acquired-product
# docs; events/sessions/webinars are event listings. None of it helps account research.
SKIP = re.compile(r"^https://(docs\.coreweave\.com/(ko|ja|fr|monolith-ai|model-distillation)"
                  r"|www\.coreweave\.com/(events?|event-category|fully-connected-sessions|fully-connected-2026|"
                  r"webinars|blog-categories|search))(/|$)")
GREENHOUSE = "https://boards-api.greenhouse.io/v1/boards/coreweave/jobs"
US = re.compile(r"United States|\bUSA?\b")
# US roles worth reading in full: they say where sites are and what gear runs there
# Security/network postings name the incumbent vendors (Cisco, CrowdStrike, Teleport, ...)
DETAIL = re.compile(r"data ?cent|facilit|network|secur|infrastructure|identity|access|"
                    r"detection|soc\b|incident|it\b|corporate|operational technology|hardware", re.I)


def fetch(url):
    # curl uses the macOS keychain for CAs; python.org builds ship without a CA bundle
    r = subprocess.run(["curl", "-sSfL", "--max-time", "30", "-A", UA, url], capture_output=True)
    if r.returncode:
        raise RuntimeError(r.stderr.decode().strip())
    return r.stdout.decode("utf-8", "replace")


class TextExtractor(HTMLParser):
    """Keeps headings, paragraphs, list items, and table cells; drops chrome."""
    SKIP = {"script", "style", "nav", "header", "footer", "svg", "noscript", "form"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "pre", "blockquote", "div", "br"}

    def __init__(self):
        super().__init__()
        self.out, self.skip, self.title, self._in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag == "title":
            self._in_title = True
        elif not self.skip:
            if tag in ("h1", "h2", "h3", "h4"):
                self.out.append("\n\n" + "#" * int(tag[1]) + " ")
            elif tag == "li":
                self.out.append("\n- ")
            elif tag in ("td", "th"):
                self.out.append(" | ")
            elif tag in self.BLOCK:
                self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self.skip:
            self.out.append(data)

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+", " ", t)
        return re.sub(r"\n\s*\n\s*\n+", "\n\n", t).strip()


def slug(url):
    p = urlparse(url)
    s = (p.netloc + p.path).strip("/").replace("/", "__")
    return re.sub(r"[^A-Za-z0-9_.-]", "-", s) or "index"


def bucket(source, url):
    if source == "docs":
        return "docs"
    for b in ("blog", "news"):
        if f"/{b}/" in url:
            return b
    return "site"


def sitemap_urls(url):
    """Expands sitemap indexes (<sitemap><loc>) into page URLs."""
    xml = fetch(url)
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    if "<sitemapindex" not in xml:
        return locs
    return [u for sm in locs for u in sitemap_urls(sm)]


def page(source, url):
    """Returns (title, text). docs.coreweave.com serves clean Markdown at <url>.md."""
    if source == "docs" and urlparse(url).path not in ("", "/"):
        md = fetch(url.rstrip("/") + ".md")
        # every page starts with the same "Documentation Index" blockquote; drop it
        md = re.sub(r"\A(>.*\n)+\s*", "", md)
        m = re.search(r"^title:\s*\"?(.+?)\"?\s*$", md, re.M) or re.search(r"^# (.+)$", md, re.M)
        return (m.group(1) if m else url), md.strip()
    body = fetch(url)
    # old /blog/<press-release> URLs 301 to the /newsroom listing; its Vue template marker gives it away
    if "{{ featured[0].title }}" in body:
        raise RuntimeError("redirected to a listing page")
    ex = TextExtractor()
    ex.feed(body)
    return ex.title.strip(), ex.text()


LOCK = threading.Lock()


def crawl_sitemap(source, sitemap_url, writer, f):
    rp = urllib.robotparser.RobotFileParser()
    host = urlparse(sitemap_url)
    rp.parse(fetch(f"{host.scheme}://{host.netloc}/robots.txt").splitlines())
    urls = [u for u in sitemap_urls(sitemap_url)
            if not SKIP.match(u) and not re.search(r"\.(png|jpe?g|gif|svg|webp|pdf|mp4)$", u, re.I)]
    # blog/news before everything else so research can start early
    urls.sort(key=lambda u: bucket(source, u) == "site")
    print(f"[{source}] {len(urls)} urls", flush=True)
    blocked = 0
    for i, url in enumerate(urls, 1):
        dest = ROOT / bucket(source, url) / (slug(url) + ".md")
        if dest.exists():
            continue
        if not rp.can_fetch(UA, url):
            print(f"  skip (robots) {url}")
            continue
        time.sleep(DELAY[source])  # before the request, so errors are rate-limited too
        try:
            title, text = page(source, url)
            blocked = 0
        except Exception as e:  # keep going on individual page failures
            print(f"  ERR {url}: {e}", flush=True)
            if re.search(r"error: (403|429)", str(e)):
                # back off on rate limiting, then give up on the host
                blocked += 1
                if blocked >= 5:
                    print(f"[{source}] blocked; stopping. Rerun later to resume.", flush=True)
                    return
                time.sleep(60 * blocked)
            continue
        dest.write_text(f"# {title}\n\nSource: {url}\n\n{text}\n")
        with LOCK:
            writer.writerow([url, title, dest.relative_to(ROOT), datetime.now(timezone.utc).isoformat(timespec="seconds")])
            f.flush()
        if i % 25 == 0:
            print(f"  {i}/{len(urls)}", flush=True)


def snapshot_careers(writer):
    jobs = json.loads(fetch(GREENHOUSE))["jobs"]
    keep = [{"id": j["id"], "title": j["title"], "location": j["location"]["name"],
             "url": j["absolute_url"], "updated_at": j["updated_at"]} for j in jobs]
    us = [j for j in keep if US.search(j["location"]) or re.search(r", [A-Z]{2}\b|D\.C\.|Remote", j["location"])]
    print(f"[careers] {len(keep)} jobs, {len(us)} US", flush=True)
    for j in us:
        if not DETAIL.search(j["title"]):
            continue
        try:
            d = json.loads(fetch(f"{GREENHOUSE}/{j['id']}"))
        except Exception as e:
            print(f"  ERR job {j['id']}: {e}", flush=True)
            continue
        j["departments"] = [x["name"] for x in d.get("departments", [])]
        ex = TextExtractor()
        ex.feed(html.unescape(d["content"]))  # Greenhouse returns entity-escaped HTML
        j["content"] = ex.text()
        time.sleep(DELAY["careers"])
    out = ROOT / "careers" / "greenhouse.json"
    out.write_text(json.dumps({"fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "total": len(keep), "us": us, "non_us": [j for j in keep if j not in us]}, indent=2))
    writer.writerow([GREENHOUSE, f"Greenhouse jobs ({len(keep)}, {len(us)} US)", out.relative_to(ROOT),
                     datetime.now(timezone.utc).isoformat(timespec="seconds")])


def main():
    for d in ("docs", "blog", "news", "site", "careers"):
        (ROOT / d).mkdir(parents=True, exist_ok=True)
    csv_path = ROOT / "sources.csv"
    new = not csv_path.exists()
    with csv_path.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["url", "title", "file", "fetched_at"])
        if "--careers" in sys.argv:
            snapshot_careers(w)
            f.flush()
        threads = [threading.Thread(target=crawl_sitemap, args=(s, sm, w, f)) for s, sm in SITEMAPS.items()]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    main()
