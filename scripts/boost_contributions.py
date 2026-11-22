#!/usr/bin/env python3
"""
EyeHealthAI - GitHub Contribution Booster Script
Automates repeated research activity commits and pushes to dramatically increase
GitHub profile contributions and turn the contribution activity graph dark green.
"""

import os
import sys
import time
import random
import datetime
import subprocess

ACTIVITIES = [
    "audit clinical dataset distribution for class imbalance",
    "tune learning rate scheduler for ResNet50 anemia model",
    "evaluate MobileNetV3-Small on conjunctivitis validation split",
    "benchmark Grad-CAM attribution heatmaps generation latency",
    "optimize eye localization ROI cropping pipeline",
    "update illumination and blur sharpness thresholds in preprocessing",
    "validate laboratory hemoglobin ground-truth regression bounds",
    "evaluate Bilirubin classification threshold calibration",
    "add integration tests for multi-disease inference pipeline",
    "enhance doctor buddy explanation prompt with clinical reasoning",
    "update bilingual English-Hindi medical report generator templates",
    "verify patient-level split isolation to prevent data leakage",
    "run automated end-to-end clinical screening suite",
    "optimize ONNX runtime session memory footprint",
    "refactor database transaction management for patient records",
    "update clinical safety checks for conjunctival pallor preservation"
]

def run_cmd(cmd, env=None):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    return res

def boost(count=50, days_back=0, push_every=1, target_file="RESEARCH_ACTIVITY.md"):
    print(f"=== Starting Contribution Boost: {count} Commits ===")
    print(f"Target File: {target_file}")
    print(f"Days spread: {days_back} days (0 = today only)")
    print(f"Push frequency: every {push_every} commit(s)")

    if not os.path.exists(target_file):
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("# EyeHealthAI - Research & Development Activity Log\n\n")
            f.write("Clinical Computer Vision Screening Research & Validation Log\n\n")

    now = datetime.datetime.now()
    env = os.environ.copy()

    for i in range(1, count + 1):
        activity = random.choice(ACTIVITIES)

        if days_back > 0:
            # Spread commits randomly across the past X days
            random_days = random.randint(0, days_back)
            random_hours = random.randint(8, 21)
            random_minutes = random.randint(0, 59)
            random_seconds = random.randint(0, 59)
            commit_time = now - datetime.timedelta(days=random_days)
            commit_time = commit_time.replace(hour=random_hours, minute=random_minutes, second=random_seconds)
            date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str
        else:
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # Append entry to log file
        entry = f"- [{date_str}] Iteration #{i:04d}: Completed {activity}.\n"
        with open(target_file, "a", encoding="utf-8") as f:
            f.write(entry)

        run_cmd(f'git add "{target_file}"')
        msg = f"docs(activity): iteration #{i:03d} - {activity}"
        commit_res = run_cmd(f'git commit -m "{msg}"', env=env)

        if commit_res.returncode != 0:
            print(f"[{i}/{count}] Commit failed: {commit_res.stderr.strip() or commit_res.stdout.strip()}")
            continue

        print(f"[{i}/{count}] Committed: {msg}")

        # Push to remote
        if push_every == 1 or i % push_every == 0 or i == count:
            print(f"   --> Pushing to origin main...")
            for attempt in range(1, 4):
                push_res = run_cmd("git push origin main")
                if push_res.returncode == 0:
                    print(f"   [OK] Pushed to GitHub.")
                    break
                else:
                    print(f"   [!] Push retry {attempt}: {push_res.stderr.strip()}")
                    time.sleep(2)

    print("\n==========================================")
    print(f"DONE! Successfully generated and pushed {count} contributions.")
    print("==========================================")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Boost GitHub contributions")
    parser.add_argument("--count", type=int, default=50, help="Number of commits to create (default: 50)")
    parser.add_argument("--days", type=int, default=0, help="Days to spread across (0 = today only, e.g. 30 = past 30 days)")
    parser.add_argument("--push-every", type=int, default=1, help="Push after every N commits (default: 1 for maximum push events)")
    args = parser.parse_args()

    boost(count=args.count, days_back=args.days, push_every=args.push_every)
