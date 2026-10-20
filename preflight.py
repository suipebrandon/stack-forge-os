    # Pre-commit check — run BEFORE git commit. Validates everything Windows CAN validate.
# It CANNOT build the ISO (needs privileged Linux + podman). Full proof = CI on a branch.
# Usage: python preflight.py
import sys, pathlib
root = pathlib.Path(__file__).parent
ok = True
def check(name, fn):
    global ok
    try:
        fn(); print(f"PASS {name}")
    except Exception as e:
        ok = False; print(f"FAIL {name}: {e}")

def yaml_valid():
    import yaml  # pip install pyyaml
    y = yaml.safe_load(open(root / ".github/workflows/stackforge-iso.yml").read())
    assert "jobs" in y and "build-iso" in y["jobs"], "jobs/build-iso missing"
    bib = str(y["jobs"]["build-iso"]["steps"])
    assert "localhost/stackforge-mvp1:ci" in bib, "localhost/ tag missing"
    assert "/var/lib/containers/storage:/var/lib/containers/storage" in bib, "storage mount missing"
    assert "--rootfs btrfs" in bib, "--rootfs missing"

def toml_block_valid():
    import tomllib
    txt = open(root / ".github/workflows/stackforge-iso.yml").read()
    start = txt.index("cat > config/config.toml")
    block = txt[start:txt.index("EOF", start)].split("<<'EOF'")[1]
    tomllib.loads(block)

def containerfile_valid():
    c = open(root / "os/base-image/Containerfile").read()
    assert c.strip().startswith("#") or c.startswith("FROM"), "missing FROM"
    assert "FROM quay.io/fedora/fedora-bootc:42" in c, "base must be fedora-bootc:42"
    assert "plasma-desktop" in c, "Plasma missing"

def shell_syntax_hint():
    y = open(root / ".github/workflows/stackforge-iso.yml").read()
    assert "set -x" in y and "$PWD/output" in y, "BIB step malformed"

check("workflow YAML", yaml_valid)
check("config.toml block", toml_block_valid)
check("Containerfile", containerfile_valid)
check("shell step shape", shell_syntax_hint)
print("RESULT:", "ALL LOCAL CHECKS PASS - push to branch for full ISO proof" if ok else "FIX FAILS ABOVE FIRST")
sys.exit(0 if ok else 1)
