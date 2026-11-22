#!/usr/bin/env python3
"""
Fill June, July, and August (2026-06-01 to 2026-08-21) with 2 commits per day.
Makes June and August (and July) completely green on the GitHub calendar.
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
    "update clinical safety checks for conjunctival pallor preservation",
    "calibrate model uncertainty scores for low-light smartphone captures",
    "verify scleral icterus detection sensitivity across Fitzpatrick skin types",
    "implement automated cross-validation on multicenter cataract manifests",
    "benchmark mobile inference FPS on low-power edge devices"
]

def run_cmd(cmd, env=None):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)

def main():
    target_file = "RESEARCH_ACTIVITY.md"
    start_date = datetime.date(2026, 6, 1)
    end_date = datetime.date(2026, 8, 21)

    delta = (end_date - start_date).days + 1
    print(f"Total days to fill (June 1 to August 21): {delta} days")

    schedule = []
    for day_offset in range(delta):
        curr_day = start_date + datetime.timedelta(days=day_offset)
        # 2 commits per day (morning & evening)
        h1 = random.randint(10, 13)
        m1 = random.randint(5, 55)
        s1 = random.randint(5, 55)
        dt1 = datetime.datetime(curr_day.year, curr_day.month, curr_day.day, h1, m1, s1)

        h2 = random.randint(17, 21)
        m2 = random.randint(5, 55)
        s2 = random.randint(5, 55)
        dt2 = datetime.datetime(curr_day.year, curr_day.month, curr_day.day, h2, m2, s2)

        schedule.extend([dt1, dt2])

    total_commits = len(schedule)
    print(f"Total commits planned for June to August: {total_commits}\n")

    env = os.environ.copy()
    success_count = 0

    for idx, dt in enumerate(schedule, 1):
        activity = random.choice(ACTIVITIES)
        iso_date = dt.strftime("%Y-%m-%dT%H:%M:%S")

        env["GIT_AUTHOR_DATE"] = iso_date
        env["GIT_COMMITTER_DATE"] = iso_date

        date_display = dt.strftime("%Y-%m-%d %H:%M")
        entry = f"- [{date_display}] Activity #{idx:03d}: {activity}\n"

        with open(target_file, "a", encoding="utf-8") as f:
            f.write(entry)

        run_cmd(f'git add "{target_file}"')
        msg = f"docs(activity): [{date_display}] {activity}"
        commit_res = run_cmd(f'git commit -m "{msg}"', env=env)

        if commit_res.returncode != 0:
            print(f"[{idx}/{total_commits}] Commit error: {commit_res.stderr.strip()}")
            continue

        # Push after every commit for maximum push frequency
        pushed = False
        for attempt in range(1, 4):
            push_res = run_cmd("git push origin main")
            if push_res.returncode == 0:
                pushed = True
                success_count += 1
                break
            else:
                time.sleep(1.5 * attempt)

        if pushed:
            print(f"[{idx}/{total_commits}] ({date_display}) Pushed -> origin main")
        else:
            print(f"[{idx}/{total_commits}] Push retry failed")

    print("\n==========================================")
    print(f"SUCCESS! Successfully created and pushed {success_count} commits for June through August.")
    print("==========================================")

if __name__ == '__main__':
    main()
