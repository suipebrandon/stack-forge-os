#!/usr/bin/env bash
# MVP-1 ISO build — MUST run on Linux (Fedora 41+ or GH Action). Not Windows.
set -euo pipefail
IMAGE="ghcr.io/stackforge/stackforge-mvp1:latest"
OUT="output"

mkdir -p "$OUT"

echo "[1/4] Building bootc container..."
sudo podman build -t "$IMAGE" -f Containerfile .

echo "[2/4] Generating SBOM..."
syft "$IMAGE" -o spdx-json="$OUT/sbom.spdx.json" || echo "syft missing — dnf install syft"

echo "[3/4] Building ISO via bootc-image-builder..."
sudo podman run --rm --privileged --security-opt label=type:unconfined_t \
  -v ./config.toml:/config.toml:ro -v ./$OUT:/output \
  -v /var/lib/containers/storage:/var/lib/containers/storage \
  quay.io/centos-bootc/bootc-image-builder:latest \
  --type iso --config /config.toml "$IMAGE"

echo "[4/4] Sign checksum..."
sha256sum $OUT/*.iso > $OUT/SHA256SUMS
cosign sign-blob --yes $OUT/SHA256SUMS --output-signature $OUT/SHA256SUMS.sig || echo "cosign: configure keyless in CI"
echo "DONE: $OUT/*.iso — test with: qemu-system-x86_64 -enable-kvm -m 4096 -cdrom $OUT/*.iso -boot d"
