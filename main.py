import os
import random
import datetime
import time
from subprocess import call, DEVNULL
from tqdm import tqdm


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


def get_random_commit_count(date: datetime):
    # Check if date is weekend
    is_weekend = date.weekday() >= 5

    # Simulate coin toss if date is weekend
    if is_weekend and not random.choice([True, False]):
        return 0

    # Define the number of random commits to create
    commit_count = random.randint(0, 10)

    return commit_count


if __name__ == "__main__":
    # Define the start and end dates for the random commits
    date = datetime.datetime(2017, 1, 1, 0, 0, 0)
    delta: datetime.timedelta = datetime.datetime.now() - date

    NOD = delta.days  # Number of days after date to create commits

    TZ = "0000"

    # Initialize a Git repository if not already initialized
    if not os.path.exists(".git"):
        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = f"{date}+{TZ}"
        call(["git", "init"], env=env, stdout=DEVNULL)

        time.sleep(0.5)

    for i in tqdm(range(NOD), "Creating commits:", colour="Green"):
        commit_count = get_random_commit_count(date + datetime.timedelta(days=i))

        if commit_count != 0:
            # Create random commits
            create_random_commit(
                date + datetime.timedelta(days=i),
                date + datetime.timedelta(days=i, hours=23),
                commit_count,
                timezone=TZ,
            )
