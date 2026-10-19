# System Architecture Specification (SAS) v0.1 — Stack Forge OS
Status: DRAFT for review | Date: 2026-10-19 | Baseline: SRS v0.1 | Ref: SRS §32

## 1. Architecture Validation Verdict

**Verdict: SOUND with GAPS — proceed to prototype, do not commit to full build yet.**

The SRS layered architecture (diagram + §6) is correct for goals G1-G7:
UX → Stack Store → Universal Runtime Manager → Desktop Integration (Wayland/XDG) → Gaming → System Services (systemd) → Base OS → Immutable Engine → Boot (UEFI/SB).

What validates:
- Immutable base + Flatpak separation (AR-01/AR-02) is industry-proven (Silverblue, Bazzite, Vanilla OS).
- Runtime abstraction (AR-03) is achievable: resolver → backend dispatch (flatpak/wine/proton/waydroid/web).
- Reuse-upstream (AR-04) drastically cuts risk vs building kernel/boot/DE from scratch.

What is MISSING and must be decided before code (SRS §32 explicitly defers these):

| # | Missing Decision | Options | Recommendation + Rationale | Gate |
|---|------------------|---------|----------------------------|------|
| D1 | Base distro | Fedora Atomic / Universal Blue / Ubuntu Core / Debian+Calamares | **Fedora 41+ Atomic (bootc) via Universal Blue / Bazzite as reference.** Best OSTree+bootc, Secure Boot shim, gaming drivers, Mesa/Vulkan freshness. Ubuntu+OSTree is immature. | M0 |
| D2 | Image tech: OSTree vs bootc | Pure OSTree (rpm-ostree) vs bootc (OCI containers) | **bootc (which uses OSTree under the hood).** Container build + signing + GH Actions is simpler, reproducible, rollback-native. ADR-001. | M0 |
| D3 | Boot chain | GRUB2+shim + Secure Boot (UEFI only, no legacy BIOS for MVP) | **UEFI-only, GRUB2+shim, SB signed via Fedora shim, own MOK for custom images.** Drop BIOS to halve test matrix. Document key custody per §20. | M1 |
| D4 | Filesystem layout | /usr read-only, /etc + /var writable, /home per-user, LVM/LUKS | **bootc default: btrfs or xfs /sysroot + /ostree, /var, /etc overlay, LUKS optional via Calamares.** Validate auto-rollback on failed boot (SRS §15 warns not to assume). | M1 |
| D5 | Desktop Environment | KDE Plasma 6 (Wayland) vs GNOME 46+ | **KDE Plasma 6 Wayland.** Gaming/DPI/multi-monitor, Bazzite precedent, XWayland mature, XDG Portals coverage. GNOME alternative only if touch-first. ADR-002. | M0 |
| D6 | Installer | Calamares vs Anaconda vs Subiquity | **Calamares** (SRS reference). Light, distro-agnostic, OEM/OOBE modules, LUKS support. | M1 |
| D7 | ISO pipeline | lorax / live-media-creator vs bootc-image-builder | **bootc-image-builder for `qcow2 → ISO`.** Single Containerfile → ISO + disk images. GH Action builds it. | M1 |
| D8 | Store backend | PackageKit vs Flatpak API + custom resolver | **Custom Python/TS resolver + Flatpak system API + Wine/Proton/Waydroid adapters.** No PackageKit (mutable-apt legacy). Schema in `stack-store/app-schema.json`. | M2 |
| D9 | Android runtime | Waydroid vs Anbox (dead) vs Bliss VM | **Waydroid (binderfs + Wayland).** Only viable container path. Must document ARM-x86 gap + GApps licensing (no pre-bundled GApps). | M3 |
| D10 | Update/rollback semantics | bootc staged + greenboot healthcheck | **bootc update --staged + greenboot auto-rollback.** Must prototype failure injection per NFR-002. | M1-M3 |
| D11 | GPU matrix MVP-1 | Intel iGPU + AMD + NVIDIA-open | **MVP-1: Intel/AMD only. NVIDIA proprietary as MVP-2 opt-in** (licensing + Secure Boot MOK enrollment risk). | M0 |
| D12 | Hardware baseline | Needs measurable boot target (NFR-004) | **Baseline: 4c/8GB/SSD/UEFI, target cold boot ≤30s to SDDM, ≤45s to desktop in VM.** Benchmark then freeze. | M1 |

## 2. Recommended Technology Stack (frozen for MVP-1 unless ADR changes it)

```
Base: Fedora Atomic 41 (bootc) | Kernel: distro kernel + firmware | Boot: systemd-boot? NO → GRUB2+shim
DE: KDE Plasma 6 (Wayland) + XWayland + SDDM | Services: systemd, NetworkManager, PipeWire, BlueZ, CUPS
Immutable: bootc + OSTree + greenboot + composefs (if available)
Apps: Flatpak (Flathub, verified) | Store: in-house resolver (Python 3.12)
Gaming (MVP-2): Steam Flatpak + Proton-GE + Vulkan/Mesa + Gamescope + GameMode
Android (MVP-3): Waydroid + binderfs kernel module
Web: Chromium/Electron PWA installer → .desktop entries (XDG)
Installer: Calamares + partitioning (btrfs, LUKS optional)
Build: Containerfile → bootc-image-builder → signed ISO | CI: GitHub Actions | SBOM: syft + cosign/sigstore
Language: Python for resolver/backends (testable), QML/TS for Store UI later
```

Why not build kernel/bootloader/DE/Wine from scratch: SRS §24 + §3 out-of-scope; 10-100 person-years, no differentiation.

## 3. Data Flows (must implement)

1. Store flow: `Search → metadata.json (validated) → resolver.select_runtime() → backend.install() → .desktop + icons → launch → update/uninstall` (FR-020..025, FR-100..104).
2. Boot flow: `UEFI → shim → GRUB → ostree/greenboot → SDDM → Plasma → first-run wizard`.
3. Update flow: `UpdateManager.check() → download → verify sig → stage (bootc) → reboot → greenboot health → keep or rollback` (FR-080..082).

## 4. Security Boundaries

- SBAT/Secure Boot chain verified (SEC-001/002); image signing with cosign, keys in GH Secrets, never in repo (§20).
- Flatpak sandbox + Portals default; Wine/Proton per-prefix, no `--filesystem=host` by default (SEC-006).
- Store metadata signature + allowlist of remotes (SEC-007); CVE feed → security-update SLA (SEC-008).

## 5. What to Prototype FIRST (Phase 4, SRS §5)

PoC-1 bootable ISO → PoC-2 Flatpak hello → PoC-3 atomic update+rollback → PoC-4 Wine hello → PoC-5 Waydroid hello. Stop if PoC-1 fails; fix base before Store code.
