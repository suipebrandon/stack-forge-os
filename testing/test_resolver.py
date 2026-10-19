"""Resolver unit tests — run on ANY OS (Windows OK): pytest testing/test_resolver.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "runtime-manager"))
from resolver import select_runtime

def base(**kw):
    m = {"id": "com.example.app", "name": "Ex", "type": "linux-app",
         "runtime": "flatpak", "architecture": ["x86_64"],
         "compatibility": "verified", "sources": {"origin": "flathub"},
         "version": "1.0", "permissions": ["network"]}
    m.update(kw); return m

def test_flatpak_verified():
    r = select_runtime(base())
    assert r["runtime"] == "flatpak" and r["label"] == "verified"

def test_arch_mismatch():
    r = select_runtime(base(architecture=["aarch64"]), host_arch="x86_64")
    assert r["runtime"] is None and r["label"] == "unsupported"

def test_arm_apk_blocked():
    m = base(type="android-app", runtime="waydroid", needsArmTranslation=True)
    r = select_runtime(m, host_arch="x86_64")
    assert r["label"] == "unsupported"
