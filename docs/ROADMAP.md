# Stack Forge OS — Implementation Roadmap (MVP-gated, incremental)

> Rule: No milestone starts until prior gate passes. Each milestone ends with boot/test evidence.

## M0 — Builder + Decisions (Week 1) — YOU ARE HERE
- [x] SRS v0.1 read + validation (this workspace)
- [ ] Freeze D1,D2,D5,D11 in SAS (need Product Owner sign)
- [ ] Provision builder: Fedora 41 VM (8c/16GB/100GB) OR WSL2+Fedora + QEMU/KVM. Windows CANNOT build ISO.
  ```powershell
  wsl --install -d FedoraLinux-42  # then inside: sudo dnf install -y podman qemu-kvm virt-manager
  ```
- Gate: `podman --version && qemu-system-x86_64 --version` + ADR sign-off
- Test: none (env check)

## M1 — Bootable Desktop + Flatpak (MVP-1 core, Weeks 2-4) PRIORITY #1
Deliverable: `stackforge-mvp1.iso` boots in QEMU, installs via Calamares, reaches Plasma, installs Flatpak app.
Tasks:
1. `os/base-image/Containerfile` from `quay.io/fedora-atomic-desktops/kinoite:41` + branding + flatpak remote
2. `bootc-image-builder` → ISO (see `os/base-image/build.sh`)
3. QEMU boot test + Calamares install test (see `testing/TESTPLAN.md` T-001..T-005)
4. Signed build + SBOM (`ci/build-iso.yml`)
- Gate: ISO boots, installer completes, Flatpak `org.gnome.Calculator` launches, `bootc upgrade --check` works, rollback tested.
- Risks: NVIDIA, Secure Boot MOK — defer per D11.

## M2 — Stack Store + Runtime Manager foundation (Weeks 5-7)
Deliverable: `resolver.py` + `app-schema.json` + CLI `stack-store install <id>` works for Flatpak.
Tasks: JSON schema validator, resolver unit tests (pytest 20+ cases), Flatpak backend, .desktop integration, permission display (FR-100..104).
Gate: `pytest` green, install/uninstall hello app without manual runtime choice.

## M3 — Windows/Gaming (MVP-2, Weeks 8-11)
Wine prefixes per-app, Steam Flatpak, Proton-GE pin, compat DB `compatibility.csv`, diagnostics bundle.
Gate: 1x Steam demo game + 1x Wine app (Notepad++ portable) launch with logs.

## M4 — Android/Web + Hardening (MVP-3, Weeks 12-15)
Waydroid init, PWA installer, permission UX, greenboot auto-rollback fault injection, hardware matrix 3 machines.
Gate: Waydroid hello, PWA install, rollback demo video/log.

## M5 — Alpha → Beta → RC → Stable (per SRS §5 Phase 8)
Freeze, full TESTPLAN, UAT with non-Linux users (NFR-001), release notes, SBOM publish.

## Effort honesty
MVP-1 minimal: 2-3 engineers, 4 weeks + hardware. Full vision (all MVPs): 6-10 engineers, 4-6 months. Solo on Windows without Linux VM: 0% ISO progress — fix builder first.
