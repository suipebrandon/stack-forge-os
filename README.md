# Stack Forge OS — Program Workspace (SDLC Baseline)

> Source of truth: `Stack_Forge_OS_SRS_v0.1.pdf` (12 pages, 19 Oct 2026) + System Architecture diagram.
> Method: Iterative SDLC per SRS §5. **Do not build everything at once.** Gate each milestone.

## Where we are (SDLC)

- [x] Phase 2 — Requirements: SRS v0.1 baseline DONE (needs SAS to close gaps)
- [ ] Phase 3 — Architecture: SAS v0.1 IN PROGRESS (`architecture/SAS-v0.1.md`)
- [ ] Phase 4 — Prototype: PoCs for boot → desktop → Flatpak → updates
- [ ] Phase 5+ — Incremental MVP-1 → MVP-2 → MVP-3

## Repo layout (per SRS §28)

```
stack-forge-os/
  architecture/       SAS, validation report, ADRs
  os/base-image/      bootc Containerfile + build scripts (Linux builder only)
  os/configuration/   users, systemd, flatpak remotes, branding
  installer/          Calamares config + partitioning plan
  stack-store/        app metadata schema + validator (differentiator #1)
  runtime-manager/    resolver + per-runtime backends (differentiator #2)
  desktop/            Plasma defaults, portals, settings
  gaming/             Steam/Proton/Gamescope/GameMode policy
  security/           Secure Boot, signing, sandbox policy, SBOM
  testing/            test plan + compatibility matrices
  ci/                 GitHub Actions: image → sign → ISO → test
  docs/               DECISIONS, ROADMAP, TRACEABILITY
```

## Critical constraint

**You cannot build a bootable Linux ISO on Windows / Next.js directly.**
This folder (`FirmAnt/`) is a marketing website. OS builds MUST run on Linux:
WSL2 + Fedora toolbox, or Fedora 41+ VM, or GitHub Actions runner.
See `os/base-image/README.md` and `ci/build-iso.yml`.

## Next actions (in order)

1. Read `architecture/SAS-v0.1.md` and `docs/DECISIONS.md`
2. Provision Linux builder (see ROADMAP M0)
3. Run M1 prototype: `os/base-image/build.sh` → VM boot → Flatpak hello
4. Only then start Stack Store resolver prototype (`runtime-manager/`)
