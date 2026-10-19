# SPDX-License-Identifier: Apache-2.0
"""Stack Runtime Manager — resolver (pure, unit-testable, no root needed).
SRS FR-022, FR-102, ADR-004. M2 prototype.
Usage: python resolver.py metadata.json --arch x86_64
"""
import json, sys

RUNTIME_BACKEND = {
    "flatpak": "runtime-manager/flatpak/backend.py",
    "wine": "runtime-manager/wine/backend.py",
    "proton": "runtime-manager/proton/backend.py",
    "waydroid": "runtime-manager/waydroid/backend.py",
    "browser": "runtime-manager/web/backend.py",
}

COMPAT_LABEL = {
    "verified": "Works — tested by Stack Forge",
    "supported": "Should work — supported config",
    "community-tested": "May work — community reported",
    "experimental": "Experimental — expect issues",
    "unsupported": "Not supported on this device",
}

def select_runtime(meta: dict, host_arch="x86_64") -> dict:
    if host_arch not in meta.get("architecture", []):
        return {"runtime": None, "label": "unsupported",
                "reason": f"App needs {meta['architecture']}, host is {host_arch}",
                "backend": None}
    # ARM-only Android guard (SRS §12)
    if meta["type"] == "android-app" and host_arch == "x86_64" and meta.get("needsArmTranslation"):
        return {"runtime": None, "label": "unsupported",
                "reason": "ARM-only APK without translation on x86_64", "backend": None}
    rt = meta["runtime"]
    return {"runtime": rt, "label": meta["compatibility"],
            "labelText": COMPAT_LABEL[meta["compatibility"]],
            "backend": RUNTIME_BACKEND[rt], "appId": meta["id"]}

if __name__ == "__main__":
    meta = json.load(open(sys.argv[1]))
    arch = sys.argv[3] if len(sys.argv) > 3 else "x86_64"
    print(json.dumps(select_runtime(meta, arch), indent=2))
