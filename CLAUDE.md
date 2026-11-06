# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Internal PANW account research for **CoreWeave** (NASDAQ: CRWV, AI hyperscaler), used by a sales engineer for technical enablement and firewall positioning. It has the same structure as `~/lambda` and `~/nebius`, plus a **Security Stack** page, because the account team named the incumbent security vendors: **Cisco, CrowdStrike, Teleport**.

**Deployed publicly:** pushed to the public repo `github.com/mvu-panw/coreweave_research` (branch `main`). `.github/workflows/pages.yml` (copied from `~/nebius`) runs two jobs. `check` fails on a broken internal `href`/`src`, or on any non-web file in `site/`. `deploy` publishes only `site/` to GitHub Pages on every push to `main`. Pull requests run `check` only. The repo itself, including `corpus/` and this file, is public too, so the positioning is visible to anyone. One-time manual step: Settings → Pages → Source = "GitHub Actions".

`Palo Alto Networks Resources/` (1.4 GB of public PANW PDFs, the same set as in `~/lambda`) is gitignored as local reference only. Several files are over GitHub's 100 MB limit, so use `pdftotext` or the `pages` parameter instead of reading them whole.

**Never commit internal PANW CRM data.** `*_Inventory_*.csv` (install-base exports) is gitignored. Keep any such data out of `site/` and `corpus/`. Facts from the account team are tagged `tag-account`; don't add anything more sensitive than vendor names.

## Layout

| Path | What |
|---|---|
| `site/` | Static 6-page front end: `index`, `security-stack`, `architecture`, `nvidia-gear`, `positioning`, `resources` |
| `corpus/{docs,blog,news,site}/*.md` | Plain-text crawl of docs.coreweave.com and coreweave.com from sitemaps. Grep this before searching the web. |
| `corpus/careers/greenhouse.json` | Greenhouse job board snapshot: all jobs, plus full text for US security, network, DC and infrastructure roles. This is the main incumbent-vendor evidence (Cisco IOS in DC tech postings, Wiz, CrowdStrike, Splunk, Bastille, the OT network security role). |
| `corpus/ir/` | Q2 2026 earnings release text. Q3 2026 is reported on Nov 10, 2026, so add it here. |
| `corpus/sources.csv` | url, title, local file and fetched_at for every crawled page (gitignored in `~/lambda`, committed here) |
| `tools/crawl.py` | Stdlib-only crawler, adapted from `~/nebius`. Runs one thread per host, never two per host. |

## Commands

```bash
python3 -m http.server 8600 --directory site     # preview the site
python3 -I tools/crawl.py --careers               # refresh corpus + job board (skips files that already exist; delete a file to refetch it)
```

Crawler notes:
- `crawl.py` fetches with `curl` via subprocess on purpose. The python.org Python on this Mac has no CA bundle, so `urllib` fails TLS verification. Don't "fix" this by disabling verification.
- docs.coreweave.com serves clean Markdown at `<url>.md`. The crawler strips the "Documentation Index" blockquote that starts every page. `ko/`, `ja/` and `fr/` translations, plus the acquired-product docs (`monolith-ai/`, `model-distillation/`), are skipped. That still leaves about 1,800 pages at 1 req/s.
- coreweave.com is Webflow (sitemap at `www.coreweave.com/sitemap.xml`). Old `/blog/<press-release>` URLs 301 to the `/newsroom` listing. The crawler now rejects those (Vue template marker `{{ featured[0].title }}`), but files from the first crawl may still contain listing text, so check before citing.
- The Teleport postings have aged off Greenhouse and are cited from job-aggregator mirrors.

## Site conventions

- **The UI is copied from `~/nebius`** (which came from `~/lambda` and `~/ai_sec_by_design`): the Prisma AIRS look with the cyan/purple gradient and Inter font. `site/assets/css/styles.css` is the Nebius file with the additions block relabeled, plus a CoreWeave-only tail: `.tag-account` (amber pill) and `.vendor-grid`.
- **No templating:** the nav and footer are copy-pasted into all 6 pages. Each page's `.nav-links` lists the *other* pages, with Home on every page except `index.html`. Edit all 6 files when changing the nav.
- The stylesheet is linked as `styles.css?v=1`. Bump it on every page together after CSS edits.
- **Every factual claim carries a source link and a confidence tag**: `tag-confirmed` (a CoreWeave-owned page, doc, job posting or IR release), `tag-reported` (third-party), `tag-inferred` (our reasoning), `tag-account` (PANW account team). PANW performance numbers are the same reseller-mirror datasheet figures used on the Lambda and Nebius sites, flagged as needing confirmation.
- The architecture diagram is inline SVG in `architecture.html`, with hard-coded hex colors that match the CSS tokens.

## Key account facts (verified in corpus, Nov 6, 2026)

- **Network model:** three zones: 0 (DPU management and the K8s control plane), 1 (app data plane), 2 (external ingress and egress). The fabric is a BGP-unnumbered EVPN Type-5 VXLAN Clos. Every CKS node has a BlueField-3 running CoreWeave's **Nimbus**, which does L4/L7 policy, firewalling and VXLAN termination. TORs only forward packets (`docs.coreweave.com__security__architecture.md`, `__products__networking__nimbus.md`). Tenant isolation is built in-house, so don't pitch against it.
- **CrowdStrike:** "CKS clusters include CrowdStrike by default" (security architecture doc). The November 2025 partnership has CoreWeave offering Falcon to its tenants and hosting SafeMind compute, and CrowdStrike is in the Partner Network. Positioning: complement it (XSIAM over Falcon), never displace it. BMaaS nodes have no CoreWeave agent.
- **Cisco:** "Cisco IOS and/or Juniper JunOS" appears in DC tech and manager postings at 12+ sites, and Cisco has been a shareholder since 2024. Which Cisco *security* products are deployed is unknown, so it's the first discovery question. Cisco's Hybrid Mesh Firewall-on-BlueField is the competitive pitch to expect.
- **Teleport:** infrastructure access for engineers. Coexist with it, and cover contractors, DC techs and OT vendors with Prisma Access.
- **Backbone:** 51 active DCs, multiple 400G links at every PoP, MACsec everywhere, four diverse paths per PoP. APAC and ME PoPs come online from Q4 2026 (`corpus/blog/*global-backbone*`).
- **OT:** a "Senior Network Security Engineer, Operational Technology" role is writing the OT standard now (gh 4701022006). Valvey and Racky (Mission Control) can isolate racks and trigger emergency cooling shutdowns. OT is the lead greenfield opportunity.
- **Footprint:** 49 US AZs in 20 states plus 10 outside the US, mostly Dedicated Access (`docs.coreweave.com__platform__regions__all-availability-zones.md`). Q2 2026: $2.58B revenue, about $104B backlog, 1.5 GW active, about 4.2 GW contracted by August 11.
- **Positioning logic** (same as Lambda and Nebius): firewalls go north-south only, never in the IB/RoCE fabric. Recommended: PA-7500 at PoPs and campus edges, PA-5580 per dedicated block, PA-3440 for Zone 0, OT Security plus rugged NGFW, PA-415-5G for OOB, Prisma Access, XSIAM, and CN-Series/AIRS for tenants. CN-Series rather than VM-Series, because CKS is bare-metal Kubernetes.

## Research tooling

Use WebSearch for press, DCD and earnings. The Greenhouse API is `boards-api.greenhouse.io/v1/boards/coreweave/jobs` (add `?content=true` for full text). IR releases live at `investors.coreweave.com/news/`. `gh` is not installed.
