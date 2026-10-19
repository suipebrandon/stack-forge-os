# Architecture Decision Records (ADRs)

## ADR-001 — bootc over plain OSTree/rpm-ostree
Date: 2026-10-19 | Status: PROPOSED
Context: SRS §15, §24 require atomic updates + rollback but warn not to assume auto-rollback.
Decision: Use bootc (OCI image as source of truth, OSTree as storage).
Consequences: Container builds, GH Actions friendly, `bootc-image-builder` gives ISO/qcow2 free. Must still validate greenboot rollback.
Alternatives: rpm-ostree (more Fedora Silverblue docs, but heavier compose).

## ADR-002 — KDE Plasma 6 Wayland over GNOME
Date: 2026-10-19 | Status: PROPOSED
Context: Gaming + XWayland legacy + multi-monitor (SRS §§11,13).
Decision: Plasma 6 Wayland + SDDM.
Consequences: Larger image than GNOME, but Bazzite-tested gaming path. Portals covered.
Revisit if ISO >4.7GB or touch-first pivot.

## ADR-003 — Calamares installer
Context: Need guided + manual + LUKS (FR-005/006).
Decision: Calamares with `partition`, `luks`, `users`, `displaymanager`, `bootloader` modules.
Never build custom installer for MVP.

## ADR-004 — Stack Store resolver owns UX, backends own execution
Context: G1, FR-022, FR-102.
Decision: `runtime-manager/resolver.py` is pure function: metadata → (runtime, backend, label). Backends are thin adapters that shell out to flatpak/wine/proton/waydroid. Store UI only calls resolver.
Testability: resolver has 100% unit tests without root/VM.

## ADR-005 — No bundled GApps, no promise of all APKs
Context: SRS §12, risk table.
Decision: Waydroid vanilla + optional user-installed GApps script with license warning. Compatibility DB marks ARM-only as Unsupported on x86_64.

## ADR-006 — UEFI-only MVP
Context: Halve test matrix; all modern hardware is UEFI.
Decision: No legacy BIOS support in MVP-1. Document clearly.
