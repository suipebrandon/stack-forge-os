# Stack Forge OS — M1 bootc prototype + M2 resolver
SDLC: SRS v0.1 → SAS v0.1 → M1 ISO (GH Action) → M2 Store.
Base: Fedora Kinoite 41 bootc. DE Plasma 6 Wayland. UEFI-only. Intel/AMD MVP-1.
CI: push to main builds ISO artifact `stackforge-mvp1-iso`.
Local check: `python -m pytest testing/test_resolver.py -v`
