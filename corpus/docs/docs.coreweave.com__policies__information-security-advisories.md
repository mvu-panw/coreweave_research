# Information Security Advisories

Source: https://docs.coreweave.com/policies/information-security-advisories

# Information Security Advisories

> Information on relevant CVEs and security issues for clients

## July 2024

### [CVE-2024-6387](https://www.cve.org/CVERecord?id=CVE-2024-6387) - [Qualys Security Advisory](https://www.qualys.com/2024/07/01/cve-2024-6387/regresshion.txt) - Update Advisory

| Item | Description |
| - | - |
| **Description** | OpenSSH Remote Code Execution due to Race Condition in Signal Handling (CVE-2024-6387) |
| **Severity** | 8.1 |
| **Impact to CoreWeave Platform** | The CoreWeave platform and supporting infrastructure have been upgraded to prevent exploitation of this issue. |
| **Potentially Affected Clients** | Clients running vulnerable versions of OpenSSH server are vulnerable to this CVE. Clients running an OpenSSH server version equal to or greater than "8.5p1" and less than "9.8p1" are vulnerable to this issue and should take steps to remediate. In particular, clients using VirtualServers and Slurm may need to take action to upgrade their SSH servers to a patched version or use workarounds which prevent exploitation. |
| **Actions Taken** | **Patching and Updates:** Updates have been deployed inside of the CoreWeave platform and its supporting infrastructure.   **System Status:** As of July 2nd, 2024 CoreWeave systems are operational and no outages to support upgrade operations are planned.   **Recommended Client Actions:** Clients which run a VirtualServer, container, or Slurm login Pod that uses a version of OpenSSH server should upgrade their VirtualServer, container image, or Slurm login/compute Pod images in order to obtain a patched version. Alternatively, clients may apply workarounds to their SSH server configuration to limit or prevent exploitability.   Clients running an OpenSSH server version equal to or greater than "8.5p1" and less than "9.8p1" are vulnerable to this issue and should take steps to remediate. |

### Additional information

* For clients running an **Ubuntu Linux distribution**, see [the Ubuntu Security Notice for this issue.](https://ubuntu.com/security/notices/USN-6859-1)
* For clients running a **Rocky Linux distribution**, see [the Rocky Linux news page discussing this issue.](https://rockylinux.org/news/2024-07-01-openssh-sigalrm-regression)
* For clients running a **CentOS Linux distribution**, see [the CentOS documentation for this issue.](https://access.redhat.com/security/cve/cve-2024-6387)
* **Windows** is not known to be affected by this issue at time of publishing.

Further technical details about this issue may be found in [the Qualys writeup of this issue.](https://www.qualys.com/2024/07/01/cve-2024-6387/regresshion.txt)

#### SUNK/Slurm User Guidance

Clients who are **not** on a CoreWeave-managed instance of SUNK and who meet the criteria below should take action to ensure that SUNK is patched against `CVE-2024-6387`:

* Are using SUNK versions `3.20.0` through `4.3.0`
* Are using Ubuntu images in SUNK of `22.04` or higher

If the criteria above are met, clients should take the following actions:

* Add the following items to the `s6` configuration for both login and compute Nodes in the chart `values.yaml` being used to deploy CoreWeave's Slurm chart:

```yaml theme={"system"}
login:
  s6:
    ssh-patch:
      type: oneshot
      script: |
        #!/usr/bin/env bash
        groupadd messagebus
        apt update && apt install --only-upgrade openssh-server -y
compute:
  s6:
    ssh-patch:
      type: oneshot
      script: |
        #!/usr/bin/env bash
        groupadd messagebus
        apt update && apt install --only-upgrade openssh-server -y
```

* Deploy these changes (if using ArgoCD, sync the changes with the cluster).

> [!WARNING]
>
> This will roll the NodeSet Pods for the compute Nodes. If login StatefulSets are set to use the `OnDelete` update strategy, then the login Pods to all that will be upgraded with these changes will need to be manually deleted. See [the official Kubernetes documentation on StatefulSet update strategies](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#update-strategies) for more information.

> [!NOTE]
>
> If using custom build images for SUNK, these commands can be integrated into the image build instead.

## November 2023

### [CVE-2023-23583](https://www.cve.org/CVERecord?id=CVE-2023-23583) - [INTEL-SA-00950](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/redundant-prefix-issue.html) Update Advisory

| Item | Description |
| - | - |
| **Description** | In response to Intel's Platform Update advisory [INTEL-SA-00950](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/redundant-prefix-issue.html) ([CVE-2023-23583](https://www.cve.org/CVERecord?id=CVE-2023-23583)), CoreWeave Engineering has proactively updated our systems to address the identified vulnerabilities within the named Intel products. |
| **Severity** | 8.8 |
| **Impact to CoreWeave Platform** | No impact has been observed as of this posting. CoreWeave systems have been upgraded and operational prior to public disclosure. |
| **Potentially Affected Clients** | No client impact as remediation has occurred prior to public disclosure. (**Note:** Intel components are used within our services, however, our proactive updates have ensured no client impact.) |
| **Actions Taken** | **Patching and Updates:** Updates have been implemented for [INTEL-SA-00950](https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/redundant-prefix-issue.html) ([CVE-2023-23583](https://www.cve.org/CVERecord?id=CVE-2023-23583)), ensuring compatibility and system integrity. **System Status:** As of November 14th, 2023, CoreWeave in-scope systems have been upgraded and are operational. **Recommended Client Actions:** No action is required. This advisory is informational only, to assure you of CoreWeave's commitment to infrastructure security. |

CoreWeave's Vulnerability Management Team is closely monitoring the situation and is dedicated to providing timely updates if deemed necessary. If required, updates to this page will be posted.

## December 2022

### [CVE-2022-42475](https://www.cve.org/CVERecord?id=CVE-2022-42475)

| Item | Description |
| - | - |
| **Description** | A heap-based buffer overflow vulnerability \[[CWE-122](https://cwe.mitre.org/data/definitions/122.html)] in FortiOS SSL-VPN may allow a remote unauthenticated attacker to execute arbitrary code or commands via specifically crafted requests. |
| **Severity** | 9.3 |
| **Impact to CoreWeave Platform** | Currently no known impact to CoreWeave Platform |
| **Potentially Affected Clients** | Clients using FortiOS |
| **Recommended Actions** | [Vendor-recommended mitigations](https://www.fortiguard.com/psirt/FG-IR-22-398) |

[FortiGuard Labs](https://www.fortiguard.com/psirt/FG-IR-22-398) has confirmed at least one instance of vulnerability [**CVE-2022-42475**](https://www.cve.org/CVERecord?id=CVE-2022-42475) being exploited in the wild. Given the high value (CVE critical severity rating **9.3**) and relatively low complexity of this vulnerability, CoreWeave strongly recommends upgrading to an unaffected version of FortiOS on an accelerated patch schedule, according to [vendor recommendations](https://www.fortiguard.com/psirt/FG-IR-22-398).

Vulnerability checks for **CVE-2022-42475** are available from a variety of sources. Please use caution when running any script or application to ensure it is safe.

**At this time there is no impact to CoreWeave's platform**, however customers who have FortiOS running within their environment are advised to review the [vendor-recommended mitigations](https://www.fortiguard.com/psirt/FG-IR-22-398), and take appropriate self measures to upgrade their deployments and evaluate their systems for any indicators of compromise. Our cyber security team is closely monitoring the situation, and will provide important updates should more information become available.
