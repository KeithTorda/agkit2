"""
update_kit.py - Automates pulling and deploying the latest AG Kit release from GitHub.
"""
import subprocess
import sys
import os

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def main():
    repo_dir = r"c:\Users\Keith\Desktop\agkit2"
    if not os.path.isdir(repo_dir):
        print(f"[ERROR] Repository directory not found at {repo_dir}")
        sys.exit(1)

    print("Fetching updates from GitHub (origin/main)...")
    code, out, err = run_cmd("git fetch origin main", cwd=repo_dir)
    if code != 0:
        print(f"[ERROR] git fetch failed: {err}")
        sys.exit(code)

    code, local_hash, _ = run_cmd("git rev-parse HEAD", cwd=repo_dir)
    code, remote_hash, _ = run_cmd("git rev-parse origin/main", cwd=repo_dir)

    check_only = "--check" in sys.argv

    if local_hash == remote_hash:
        print(f"[UP-TO-DATE] AG Kit is already at the latest commit ({local_hash[:7]}).")
        if not check_only:
            print("Re-running install to ensure active Antigravity sync...")
    else:
        print(f"[UPDATE FOUND] Local: {local_hash[:7]} -> Remote: {remote_hash[:7]}")
        if check_only:
            sys.exit(0)

        print("Pulling latest commits...")
        code, out, err = run_cmd("git pull origin main", cwd=repo_dir)
        if code != 0:
            print(f"[ERROR] git pull failed: {err}")
            sys.exit(code)
        print(out)

    install_ps1 = os.path.join(repo_dir, "install.ps1")
    print("\nRunning install.ps1 to update Antigravity plugin and rules...")
    code, out, err = run_cmd(f'powershell -ExecutionPolicy Bypass -File "{install_ps1}"', cwd=repo_dir)
    if code != 0:
        print(f"[ERROR] Installation script failed: {err}")
        sys.exit(code)
    print(out)

    print("\n[SUCCESS] AG Kit updated and installed successfully!")

if __name__ == "__main__":
    main()
