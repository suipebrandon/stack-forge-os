# Decisions Log (append-only)

- 2026-10-19: SRS v0.1 validated; SAS v0.1 drafted. Base = Fedora Kinoite bootc, DE = Plasma 6, UEFI-only MVP-1, NVIDIA deferred. Pending PO sign.
- 2026-10-19: Windows host CANNOT build ISO — builder must be Fedora VM or GH Action. Documented in os/base-image/README.md.
- TODO(M0): Freeze boot-time target after first QEMU benchmark.
- TODO(M0): Key custody for image signing (GH OIDC keyless vs HSM).
