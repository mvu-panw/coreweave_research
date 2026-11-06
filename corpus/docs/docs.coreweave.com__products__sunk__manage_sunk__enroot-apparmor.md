# Set up AppArmor profile for Enroot

Source: https://docs.coreweave.com/products/sunk/manage_sunk/enroot-apparmor

# Set up AppArmor profile for Enroot

> Configure the recommended AppArmor profile for Enroot unprivileged containers on SUNK compute nodes

[SUNK Standard](https://docs.coreweave.com/products/sunk.md)

[SUNK Self-Service](https://docs.coreweave.com/products/sunk/about-self-service-sunk.md)

[Enroot](https://github.com/NVIDIA/enroot) is a standalone, fully unprivileged container system from NVIDIA. It removes much of the isolation associated with traditional containers while preserving filesystem separation. This makes Enroot an optimal choice for managing HPC deployments.

[AppArmor](https://apparmor.net) is an optional component of the Linux kernel that lets you place custom restrictions on specified applications, including enroot.

The recommended profile grants necessary capabilities like mounting, pivoting root, and process tracing, while restricting access to critical system areas. It denies write access to specific parts of the `/proc` and `/sys` filesystems to enhance security and prevent unauthorized modifications.

## Default AppArmor profile

The recommended AppArmor profile is loaded onto CoreWeave nodes by default. No action is required to enable this profile.

The default CoreWeave AppArmor profile is as follows:

```text theme={"system"}
#include <tunables/global>

profile enroot flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # added
  mount,
  pivot_root,
  ptrace,

  # defaults
  network,
  capability,
  file,
  umount,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9/]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/kcore rwklx,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```
