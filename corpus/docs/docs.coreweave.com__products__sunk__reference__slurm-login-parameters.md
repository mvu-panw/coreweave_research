# Slurm login parameter reference

Source: https://docs.coreweave.com/products/sunk/reference/slurm-login-parameters

# Slurm login parameter reference

> Complete parameter reference for the Slurm login Helm chart, including directory cache and affinity settings

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square)

## Parameters

<table>
  <thead>
    <th>Key & Description</th>
    <th>Type</th>
    <th>Default</th>
  </thead>

  <tbody>
    <tr>
      <td id="directoryCache--affinity">
        **directoryCache.affinity**\

        The affinity for the directory-cache controller. This overrides the value of [ `global.nodeSelector.affinity`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#global--nodeSelector--affinity).
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--directories">
        **directoryCache.directoryService.directories**\

        The directory services to configure. Click to expand examples.

        > [accordion] Google Secure LDAP
        >
        > ```yaml theme={"system"}
        > directories:
        >   - name: google-example.com
        >     enabled: true
        >     ldapUri: ldaps://ldap.google.com:636
        >     user:
        >       canary: user@google-example.com
        >     defaultShell: "/bin/bash"
        >     fallbackHomeDir: "/home/%u"
        >     overrideHomeDir: /mnt/nvme/home/%u
        >     ldapsCert: google-ldaps-cert
        >     schema: rfc2307bis
        > ```

        > [accordion] CoreWeave LDAP
        >
        > ```yaml theme={"system"}
        > directories:
        >   - name: coreweave.cloud
        >     enabled: true
        >     ldapUri: ldap://openldap
        >     user:
        >       bindDn: cn=admin,dc=coreweave,dc=cloud
        >       searchBase: dc=coreweave,dc=cloud
        >       existingSecret: bind-user-sssd-config
        >       canary: admin
        >     defaultShell: "/bin/bash"
        >     fallbackHomeDir: "/home/%u"
        >     schema: rfc2307
        > ```

        > [accordion] Authentik
        >
        > ```yaml theme={"system"}
        > directories:
        >   - name: coreweave.cloud
        >     enabled: true
        >     ldapUri: ldap://authentik-outpost-ldap-outpost
        >     user:
        >       bindDn: cn=ldapsvc,dc=coreweave,dc=cloud
        >       searchBase: dc=coreweave,dc=cloud
        >       existingSecret: bind-user-sssd-config
        >       canary: ldapsvc
        >     startTLS: true
        >     userObjectClass: user
        >     groupObjectClass: group
        >     userNameAttr: cn
        >     groupNameAttr: cn
        >     schema: rfc2307bis
        > ```

        > [accordion] Active Directory
        >
        > ```yaml theme={"system"}
        > directories:
        >   - name: contoso.com
        >     enabled: true
        >     ldapUri: ldap://domaincontroller.tenant-my-tenant.coreweave.cloud
        >     user:
        >       bindDn: CN=binduser,CN=Users,DC=contoso,DC=com
        >       searchBase: DC=contoso,DC=com
        >       existingSecret: bind-user-sssd-config
        >       canary: binduser
        >     defaultShell: "/bin/bash"
        >     fallbackHomeDir: "/home/%u"
        >     schema: AD
        > ```
      </td>

      <td>list</td>
      <td>See individual settings below.</td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--directories[0]--enabled">
        **directoryCache.directoryService.directories\[0].enabled**\

        Enable the directory service.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--directories[0]--ldapsCert">
        **directoryCache.directoryService.directories\[0].ldapsCert**\

        Name of existing TLS certificate for LDAP-S. \


        > [accordion] Example: click to expand
        >
        > ```yaml theme={"system"}
        > kubectl create secret tls google-ldaps-cert \
        >         --cert=Google_2025_08_24_55726.crt \
        >         --key=Google_2025_08_24_55726.key
        > ```
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--directories[0]--name">
        **directoryCache.directoryService.directories\[0].name**\

        Name of the directory service. \
        &#x20;The primary domain should always be named: `default`
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "default"
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--directories[0]--user--existingSecret">
        **directoryCache.directoryService.directories\[0].user.existingSecret**\

        Name of an existing secret containing an SSSD configuration snippet with the `ldap_default_authtok` set for this domain.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--directories[0]--user--existingSecretFileName">
        **directoryCache.directoryService.directories\[0].user.existingSecretFileName**\

        The name of the file in the existing secret that contains the ldap passwords.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "ldap-password.conf"
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--directoryService--watchInterval">
        **directoryCache.directoryService.watchInterval**\

        The interval in seconds to check for changes in sssd configuration.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        60
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--image">
        **directoryCache.image**\

        The image to use for the directory-cache controller.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository:
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--interval">
        **directoryCache.interval**\

        Polling interval for updates to user database
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--leaderElection--enabled">
        **directoryCache.leaderElection.enabled**\

        This forces the directory-cache controller to use leader election even if the number of replicas is set to 1. \
        &#x20;Useful if planning to scale after deployment.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--logLevel">
        **directoryCache.logLevel**\

        The log level. \
        &#x20;Uses integers or [zap log level strings](https://pkg.go.dev/go.uber.org/zap#pkg-constants): <ul> <li>`debug`</li> <li>`info`</li> <li>`warn`</li> <li>`error`</li> <li>`dpanic`</li> <li>`panic`</li> <li>`fatal`</li> </ul>
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "info"
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--minimumUID">
        **directoryCache.minimumUID**\

        The minimum UID to be used to filter users. \

      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1000
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--nsscacheMaps">
        **directoryCache.nsscacheMaps**\

        The nsscache maps used to configure the directory-cache controller. This is only used if `source` is set to `nsscache`.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        [
          "passwd",
          "group"
        ]
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--podMonitor--enabled">
        **directoryCache.podMonitor.enabled**\

        Enable monitoring via the Prometheus operator `PodMonitor` CRD.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--replicas">
        **directoryCache.replicas**\

        The number of replicas of the directory-cache controller pod to run. \
        &#x20;Leader election will be enabled if this is greater than 1 or leader election is explicitly enabled.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--resources">
        **directoryCache.resources**\

        The resource to request for the directory-cache controller.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        limits:
            memory: 2Gi
        requests:
            cpu: 2
            memory: 2Gi

        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--selectGroups">
        **directoryCache.selectGroups**\

        Groups to select users from which
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--source">
        **directoryCache.source**\

        The source of user information for the directory-cache controller. Can be `sssd`, or `nsscache`.
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "nsscache"
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--sssdContainer--livenessProbe">
        **directoryCache.sssdContainer.livenessProbe**\

        The liveness probe for the sssd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--sssdContainer--readinessProbe">
        **directoryCache.sssdContainer.readinessProbe**\

        The readiness probe for the sssd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--sssdContainer--resources">
        **directoryCache.sssdContainer.resources**\

        Resources for the sssd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        limits:
            memory: 2Gi
        requests:
            cpu: 1
            memory: 2Gi

        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--sssdContainer--startupProbe">
        **directoryCache.sssdContainer.startupProbe**\

        The startup probe for the sssd container.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        map[]
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--tolerations">
        **directoryCache.tolerations**\

        The tolerations for the directory-cache controller deployment.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="directoryCache--vmPodScrape--enabled">
        **directoryCache.vmPodScrape.enabled**\

        Enable monitoring via VictoriaMetrics operator `VMPodScrape` CRD. Note: To enable this, `podMonitor` must be disabled in addition to setting `vmPodScrape.enabled` to `true`.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="imagePullSecrets">
        **imagePullSecrets**\

        Image pull secrets to configure if using custom private images.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        []
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--affinity">
        **loginController.affinity**\

        The affinity for the login controller. This overrides the value of [ `global.nodeSelector.affinity`](https://docs.coreweave.com/products/sunk/reference/slurm-parameters#global--nodeSelector--affinity).
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--image">
        **loginController.image**\

        The image to use for the login-controller.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        repository: 
        tag:

        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--leaderElection--enabled">
        **loginController.leaderElection.enabled**\

        This forces the login-controller to use leader election even if the number of replicas is set to 1. \
        &#x20;Useful if planning to scale after deployment.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--logLevel">
        **loginController.logLevel**\

        The log level. \
        &#x20;Uses integers or [zap log level strings](https://pkg.go.dev/go.uber.org/zap#pkg-constants): <ul> <li>`debug`</li> <li>`info`</li> <li>`warn`</li> <li>`error`</li> <li>`dpanic`</li> <li>`panic`</li> <li>`fatal`</li> </ul>
      </td>

      <td>string</td>

      <td>
        ```yaml wrap theme={"system"}
        "info"
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--podMonitor--enabled">
        **loginController.podMonitor.enabled**\

        Enable monitoring via the Prometheus operator `PodMonitor` CRD.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        true
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--replicas">
        **loginController.replicas**\

        The number of replicas of the login-controller pod to run. \
        &#x20;Leader election will be enabled if this is greater than 1 or leader election is explicitly enabled.
      </td>

      <td>int</td>

      <td>
        ```yaml wrap theme={"system"}
        1
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--resources">
        **loginController.resources**\

        The resource to request for the login-controller.
      </td>

      <td>object</td>

      <td>
        ```yaml wrap theme={"system"}
        limits:
            memory: 2Gi
        requests:
            cpu: 2
            memory: 2Gi

        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--tolerations">
        **loginController.tolerations**\

        The tolerations for the login-controller deployment.
      </td>

      <td>list</td>

      <td>
        ```yaml wrap theme={"system"}
        null
        ```
      </td>
    </tr>

    <tr>
      <td id="loginController--vmPodScrape--enabled">
        **loginController.vmPodScrape.enabled**\

        Enable monitoring via the VictoriaMetrics operator `VMPodScrape` CRD. Note: To enable this, `podMonitor` must be disabled in addition to setting `vmPodScrape.enabled` to `true`.
      </td>

      <td>bool</td>

      <td>
        ```yaml wrap theme={"system"}
        false
        ```
      </td>
    </tr>
  </tbody>
</table>
