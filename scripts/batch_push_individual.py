import subprocess
import os
import sys
import time

def get_commit_message(filepath):
    p = filepath.replace('\\', '/')
    basename = os.path.basename(p)
    name, ext = os.path.splitext(basename)

    if p == '.env.example':
        return 'chore(config): update environment configuration template'
    elif p == 'app.py':
        return 'feat(api): update FastAPI core application endpoints and lifecycle'
    elif p == 'verify_all_e2e.py':
        return 'test: add comprehensive end-to-end verification script'
    elif p.startswith('docs/'):
        clean_name = name.replace('_', ' ').lower()
        return f'docs: add clinical and regulatory documentation for {clean_name}'
    elif p.startswith('data/manifests/'):
        clean_name = name.replace('_', ' ').lower()
        return f'data(manifests): update {clean_name} dataset manifest'
    elif p.startswith('saved_models/'):
        parts = p.split('/')
        model_name = parts[1] if len(parts) > 1 else 'clinical'
        return f'build(models): update {model_name} {name} evaluation and training log'
    elif p.startswith('reports/'):
        return f'docs(reports): add clinical evaluation metrics {name}'
    elif p.startswith('src/database/'):
        return f'feat(db): update {name} database persistence module'
    elif p.startswith('src/preprocessing/'):
        return f'feat(preprocessing): enhance {name} ocular pipeline'
    elif p.startswith('src/inference/'):
        return f'feat(inference): enhance {name} clinical screening service'
    elif p.startswith('src/utils/'):
        return f'feat(utils): add {name} helper utility'
    elif p.startswith('src/config.py'):
        return 'refactor(config): update project paths and environment settings'
    elif p.startswith('static/css/'):
        return f'style(ui): update {name} clinical dashboard styling'
    elif p.startswith('static/js/'):
        return f'feat(frontend): enhance {name} clinical interactive controller'
    elif p.startswith('static/'):
        return f'feat(ui): update {name} web template layout'
    elif p.startswith('tests/scratch_'):
        clean_name = name.replace('scratch_', '').replace('_', ' ')
        return f'test(scratch): add verification routine for {clean_name}'
    elif p.startswith('tests/'):
        clean_name = name.replace('test_', '').replace('_', ' ')
        return f'test: add/update automated test for {clean_name}'
    elif p.startswith('test_images/'):
        return f'test(assets): add reference visual test asset {basename}'
    elif p.startswith('scripts/'):
        clean_name = name.replace('_', ' ')
        return f'chore(scripts): add {clean_name} automation script'
    else:
        return f'feat: update {basename}'

def run_git(cmd, check=True):
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {cmd}\nOutput: {res.stdout}\nError: {res.stderr}")
    return res

def get_pending_files():
    res = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
    files = []
    for line in lines:
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue
        path = parts[1].strip()
        if os.path.isdir(path):
            for root, dirs, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(root, f).replace('\\', '/')
                    if '__pycache__' not in fp and not fp.endswith('.pyc') and not fp.endswith('.pth') and not fp.endswith('.pt'):
                        files.append(fp)
        else:
            if '__pycache__' not in path and not path.endswith('.pyc') and not path.endswith('.pth') and not path.endswith('.pt'):
                files.append(path.replace('\\', '/'))
    return files

def main():
    files = get_pending_files()
    total = len(files)
    print(f"Total files to commit and push one-by-one: {total}")

    success_count = 0
    for idx, filepath in enumerate(files, 1):
        if not os.path.exists(filepath):
            print(f"[{idx}/{total}] Skipping non-existent: {filepath}")
            continue

        msg = get_commit_message(filepath)
        print(f"\n[{idx}/{total}] Processing: {filepath}")
        print(f"Commit msg: {msg}")

        # Git add
        run_git(f'git add "{filepath}"')

        # Git commit
        commit_res = run_git(f'git commit -m "{msg}"', check=False)
        if commit_res.returncode != 0:
            if 'nothing to commit' in commit_res.stdout or 'nothing to commit' in commit_res.stderr:
                print("Nothing new to commit, continuing...")
                continue
            else:
                print(f"Commit error: {commit_res.stderr or commit_res.stdout}")
                continue

        # Git push with retries
        pushed = False
        for attempt in range(1, 4):
            push_res = run_git('git push origin main', check=False)
            if push_res.returncode == 0:
                print(f"Successfully pushed [{idx}/{total}] -> origin main")
                pushed = True
                success_count += 1
                break
            else:
                print(f"Push attempt {attempt} failed: {push_res.stderr.strip() or push_res.stdout.strip()}")
                time.sleep(2 * attempt)

        if not pushed:
            print(f"Failed to push {filepath} after 3 attempts.")
            sys.exit(1)

    print(f"\n==========================================")
    print(f"ALL DONE! Successfully committed and pushed {success_count} commits individually.")
    print(f"==========================================")

if __name__ == '__main__':
    main()
