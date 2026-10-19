# Test Plan — gated per milestone (SRS §21)

## M1 gates (bootable ISO) — must ALL pass
- T-001 ISO boots in QEMU (UEFI): `qemu-system-x86_64 -enable-kvm -m 4096 -cdrom *.iso -boot d` reaches SDDM
- T-002 Calamares install to 40GB disk completes, reboot without ISO reaches desktop
- T-003 Network + audio smoke: `nmcli`, speaker-test via PipeWire
- T-004 Flatpak hello: `flatpak install flathub org.gnome.Calculator -y && flatpak run ...` launches
- T-005 Update+rollback: `bootc upgrade --check`, stage dummy, `greenboot` health, rollback to previous deployment
- T-006 Boot time: `systemd-analyze` record (target ≤45s VM)

## M2 gates
- T-010 `pytest testing/test_resolver.py` 100% pass (runs on Windows too)
- T-011 schema validator rejects bad metadata (arch mismatch, unknown runtime)
- T-012 install/uninstall Flatpak via resolver CLI, .desktop appears, permissions shown

## Hardware matrix (SRS §21, §30) — fill before Beta
| Machine | CPU/GPU | RAM | Result M1 | Notes |
|---|---|---|---|---|
| VM QEMU | virtio | 4GB | | baseline |
| Laptop Intel iGPU | | 8GB | | |
| Desktop AMD dGPU | | 16GB | | |
| NVIDIA (MVP-2) | | | DEFERRED | needs MOK |

## Compatibility DB (SRS §11)
`testing/compatibility.csv`: app,version,runtime,host,result,log_link — start with 5 rows in M2/M3.
