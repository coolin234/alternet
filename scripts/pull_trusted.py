import yaml
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

TRUST_FILE = "trust.yaml"
ZINE_DIR = "zines"

def load_trusted_zines(path=TRUST_FILE):
    with open(path, 'r') as f:
        trust = yaml.safe_load(f)
    return trust.get('trusted_zines', [])

def clone_repo(name, repo_url):
    dest = os.path.join(ZINE_DIR, name)
    if os.path.exists(dest):
        print(f"[!] Skipping {name} - already exists.")
        return

    print(f"[+] Cloning {name}...")
    try:
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, dest], check=True)
        print(f"[✓] {name} cloned.")
    except subprocess.CalledProcessError as e:
        print(f"[x] Failed to clone {name}: {e}")

def pull_all():
    os.makedirs(ZINE_DIR, exist_ok=True)
    zines = load_trusted_zines()
    with ThreadPoolExecutor(max_workers=4) as executor:
        for zine in zines:
            executor.submit(clone_repo, zine['name'], zine['repo'])

if __name__ == "__main__":
    pull_all()
