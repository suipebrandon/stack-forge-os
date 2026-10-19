# Decisions Log (append-only)

- 2026-10-19: SRS v0.1 validated; SAS v0.1 drafted. Base = Fedora Kinoite bootc, DE = Plasma 6, UEFI-only MVP-1, NVIDIA deferred. Pending PO sign.
- 2026-10-19: Windows host CANNOT build ISO — builder must be Fedora VM or GH Action. Documented in os/base-image/README.md.
- 2026-10-19: CI fix — quay.io/fedora-atomic-desktops/kinoite:41 returns unauthorized (EOL tag). Switched MVP-1 base to quay.io/fedora/fedora-bootc:42 + plasma-desktop layer. SAS D1 updated: Fedora 42 Bootc, Plasma on top.
- TODO(M0): Key custody for image signing (GH OIDC keyless vs HSM).
