import os
import random
import datetime
import time
from subprocess import call, DEVNULL
from tqdm import tqdm
import argparse


def random_date(start, end):
    """
    Generate a random datetime between two datetime objects.
    """
    delta = end - start
    random_hours = random.randint(0, int(delta.total_seconds() / 3600))
    random_datetime = start + datetime.timedelta(hours=random_hours)
    return random_datetime


def create_random_commit(
    start_date: datetime, end_date: datetime, commit_count, timezone="0000"
):
    # Generate a list of random dates
    random_dates = [random_date(start_date, end_date) for _ in range(commit_count)]

    # Sort the dates to ensure chronological order
    random_dates.sort()

    for random_dt in random_dates:
        # Create or modify a file
        with open("random_file.txt", "a") as file:
            file.write(f"Random commit on {random_dt}\n")

        # Add the file to staging
        call(["git", "add", "random_file.txt"], stdout=DEVNULL)

        # Commit with the random date
        commit_date = random_dt.strftime("%Y-%m-%dT%H:%M:%S")

        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = f"{commit_date}+{timezone}"
        call(
            [
                "git",
                "commit",
                "-m",
                f"Random commit on {commit_date}",
                "--date",
                f"{commit_date}+{timezone}",
            ],
            env=env,
            stdout=DEVNULL,
        )


def get_random_commit_count(date: datetime, maxcommits: int):
    # Check if date is weekend
    is_weekend = date.weekday() >= 5

    # Simulate coin toss if date is weekend
    if is_weekend and not random.choice([True, False]):
        return 0

    # Define the number of random commits to create
    commit_count = random.randint(0, maxcommits)

    return commit_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random git commits over a date range.")
    parser.add_argument('--from', dest='from_date', required=True, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--to', dest='to_date', required=True, help='End date in YYYY-MM-DD format or "now"')
    parser.add_argument('--commit_count', dest='max_commits', type=int, default=2, help='Maximum number of commits per day')
    parser.add_argument('--timezone', dest='timezone', default='0000', help='Timezone offset, e.g., 0000')
    parser.add_argument('--rewrite', action='store_true', help='Rewrite git history from root (delete .git before running)')
    parser.add_argument('--dry_run', action='store_true', help='Simulate actions without making any changes')
    args = parser.parse_args()

    date = datetime.datetime.strptime(args.from_date, "%Y-%m-%d")
    if args.to_date.lower() == "now":
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(args.to_date, "%Y-%m-%d")
    delta = end_date - date
    NOD = delta.days + 1  # Include the end date
    TZ = args.timezone
    max_commits = args.max_commits

    # Optionally rewrite git history from root
    remote_url = None
    if args.rewrite and os.path.exists(".git"):
        # Try to remember the remote URL if it exists
        import subprocess
        try:
            remote_url = subprocess.check_output([
                "git", "remote", "get-url", "origin"
            ]).decode("utf-8").strip()
        except Exception:
            remote_url = None
        if args.dry_run:
            print("[DRY RUN] Would delete .git directory.")
        else:
            import shutil
            shutil.rmtree(".git")

    # Initialize a Git repository if not already initialized
    if not os.path.exists(".git"):
        if args.dry_run:
            print(f"[DRY RUN] Would initialize git repo with GIT_COMMITTER_DATE={date}+{TZ}")
            if remote_url:
                print(f"[DRY RUN] Would restore remote 'origin' with URL: {remote_url}")
        else:
            env = os.environ.copy()
            env["GIT_COMMITTER_DATE"] = f"{date}+{TZ}"
            call(["git", "init"], env=env, stdout=DEVNULL)
            time.sleep(0.5)
            # Restore the remote if it was remembered
            if remote_url:
                call(["git", "remote", "add", "origin", remote_url], stdout=DEVNULL)

    total_commits = 0
    weekend_commits = 0
    weekday_commits = 0

    for i in tqdm(range(NOD), "Creating commits:", colour="Green"):
        current_date = date + datetime.timedelta(days=i)
        commit_count = get_random_commit_count(current_date, max_commits)
        if args.dry_run:
            print(f"[DRY RUN] {current_date.date()}: Would create {commit_count} commits" + (" (skipped, weekend)" if commit_count == 0 else ""))
        elif commit_count != 0:
            # Create random commits
            create_random_commit(
                current_date,
                current_date + datetime.timedelta(hours=23),
                commit_count,
                timezone=TZ,
            )
        # Count commits for report
        total_commits += commit_count
        if current_date.weekday() >= 5:
            weekend_commits += commit_count
        else:
            weekday_commits += commit_count

    # Print report
    print("\nCommit Report:")
    print(f"Total commits: {total_commits}")
    print(f"Weekend commits: {weekend_commits}")
    print(f"Weekday commits: {weekday_commits}")
