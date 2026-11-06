# Bring your own IP

Source: https://docs.coreweave.com/products/networking/ip/bring-your-own-ip

# Bring your own IP

> Use your own IPv4 address space on CoreWeave Cloud, including LOA submission and pricing details

Bring Your Own IP (BYOIP) lets you use your own IPv4 (Internet Protocol version 4 (IPv4) is one of the core protocols that enables the Internet.) addresses on CoreWeave Cloud. This feature is useful if you have existing IP address space and want to use it for your workloads, preserving address continuity for your applications and end users.

This page explains the prerequisites, submission process, and requirements for advertising your own IP prefixes through CoreWeave.

Before using BYOIP on CoreWeave Cloud, you must:

* Submit a Letter of Authorization (LOA) to CoreWeave.
* Pay a one-time setup fee.
* Meet the requirements outlined in the following sections.
* Agree to CoreWeave's Reservation of Rights, Terms of Service, and Acceptable Use Policy.

## Submit a letter of authorization (LOA)

The LOA gives CoreWeave written permission to announce your IP space on your behalf. Submit it before CoreWeave advertises any routes for your prefix. The LOA must:

* Be on your entity's letterhead.
* Contain your entity's full legal name, principal address, and phone number.
* Authorize CoreWeave to announce your IP space on your behalf.
* Be signed by an authorized representative of your entity.

The LOA should state the following:

> "We \[CUSTOMER] at AS\[ASN] authorize CoreWeave at AS33425 to announce our IP block \[X.X.X.X/YY] for an indefinite period of time."

The LOA must include the name and title of the person signing it, along with the date signed. As a legally binding document, the LOA must contain a wet signature and be submitted in `.pdf` format.

> [!WARNING]
>
> CoreWeave doesn't accept LOAs submitted as `.jpeg` or `.png` files.

## Pricing

Contact your CoreWeave Account Manager for detailed pricing information, or see the [CoreWeave Cloud Pricing](https://www.coreweave.com/pricing) page.

## Addressing details

The following requirements describe the IP space, registry objects, and contact information you must provide before CoreWeave can advertise your prefixes.

* CoreWeave's AS number is `33425`.
* CoreWeave only supports IPv4 addressing.

Supply CoreWeave with a valid, maintained abuse email contact for any abuse-related mail.

Each subnet that you request CoreWeave to advertise must not appear in the global Internet routing table.
You must solely own and control the subnet, and it must be portable space.

The addresses in the IP address range you supply to CoreWeave must have a clean history.
CoreWeave may investigate the reputation of the IP address range and reserves the right to reject or remove any IP address range from service if it contains an IP address that has a poor reputation or is associated with malicious behavior.

The minimum supported subnet size is a `/24` block. Each subnet block you request must have a route object in one of the mainstream route object registries such as ARIN, RIPE, or RADB. This route object must also list CoreWeave's AS number (`33425`) as an origin. If you don't have a routing registry that can be updated, CoreWeave can register the object at your request. If you've signed the block with RPKI, you must also add CoreWeave's AS to a new [ROA request](https://www.arin.net/resources/manage/rpki/faq/#what-is-a-roa), just as with the route object.

Here is an example of a route object:

```yaml theme={"system"}
route:    216.153.48.0/20
origin:   AS33425
descr:    CoreWeave, Inc.
admin-c:  SALAN13-ARIN
tech-c:   BJB20-ARIN
remarks:  https://coreweave.com
notify:   noc@coreweave.com
mnt-by:   MAINT-AS33425
changed:  bbianchi@coreweave.com 20211021  #21:29:43Z
source:   RADB
```

## Reservation of rights

> [!NOTE]
>
> The BYOIP Requirements are part of CoreWeave's [Terms of Service](https://docs.coreweave.com/policies/terms-of-service.md) (TOS). By requesting BYOIP from CoreWeave, you agree to be bound by these Requirements, and you acknowledge and agree to all of CoreWeave's reservations of rights.

CoreWeave isn't responsible for, and doesn't provide, any DDoS protections for your blocks. If your block is the victim of a cyberattack, CoreWeave expressly reserves any and all rights to take whatever measures are necessary, in its sole discretion, to protect the security, integrity, and availability of the CoreWeave platform, including but not limited to, at any time, withdrawing the announcement of your blocks. CoreWeave notifies the abuse contact on file.

If CoreWeave suspects, in its sole discretion, or finds that your advertised block is in use for malicious or harmful purposes, CoreWeave expressly reserves the right to withdraw all of your route advertisements. CoreWeave notifies the abuse contact on file.

Continued participation in this configuration constitutes your acceptance of the [TOS](https://docs.coreweave.com/policies/terms-of-service/acceptable-use-policy.md) and any other applicable policies.

These CoreWeave Requirements for BYOIP are subject to change, in CoreWeave's sole discretion. Check back regularly to confirm that you're satisfying all of the requirements. Failure to meet any requirement may result in the immediate suspension of your BYOIP subnet advertisements.
