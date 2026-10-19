# Linux builder required — READ FIRST

This folder does NOT build on Windows. The FirmAnt Next.js site and Windows PowerShell cannot produce a Linux bootable ISO.

## Option A (recommended, free): Fedora VM
1. Install VirtualBox or Hyper-V, 8c/16GB/100GB disk, UEFI enabled.
2. Install Fedora Kinoite 41 (KDE Atomic): https://fedoraproject.org/atomic-desktops/
3. Inside VM:
```bash
sudo dnf install -y podman git qemu-kvm
git clone <this-repo> && cd stack-forge-os/os/base-image
sudo ./build.sh
```

## Option B: WSL2 + nested virt (advanced)
```powershell
wsl --install -d FedoraLinux-42
# inside WSL: sudo dnf install -y podman bootc-image-builder
# Note: QEMU boot test still needs Hyper-V VM — do final test in VM.
```

## Option C: GitHub Actions (no local Linux)
Push this folder to GitHub, workflow `ci/build-iso.yml` builds ISO as artifact. Slow but works from Windows.

## Containerfile strategy (reuse, don't reinvent)
FROM quay.io/fedora-atomic-desktops/kinoite:41
- Add: Flathub remote, Steam deps, Waydroid repo (MVP-3), branding, greenboot, Calamares live ISO bits via bootc-image-builder.
- Do NOT compile kernel/Mesa/Wine. Use RPMs + Flatpaks.
