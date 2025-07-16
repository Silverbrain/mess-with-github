# Random Git Commit Generator

This script generates random commits in a Git repository over a specified date range. It creates or modifies a file and commits the changes with random timestamps, simulating activity over time.

## Features

- Generates random commit timestamps between two specified dates.
- Ensures commits are made in chronological order.
- Simulates weekend activity with reduced commit probability.
- Initializes a Git repository if one doesn't exist.
- Optionally rewrites git history from scratch and preserves remote settings.
- Supports dry run mode to preview actions without making changes.
- Uses `tqdm` to display a progress bar during commit creation.

## Requirements

- Python 3.x
- Git
- `tqdm` Python package

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Silverbrain/mess-with-github.git
   cd mess-with-github
   ```

2. **Install the required Python package:**

   ```bash
   pip install tqdm
   ```

## Usage

Run the script with the following options:

```bash
python main.py --from <YYYY-MM-DD> --to <YYYY-MM-DD|now> [--commit_count N] [--timezone ZZZZ] [--rewrite] [--dry_run]
```

### Options

- `--from <YYYY-MM-DD>`: **(required)** Start date for commits (inclusive).
- `--to <YYYY-MM-DD|now>`: **(required)** End date for commits (inclusive). You can use `now` to use the current date and time.
- `--commit_count N`: Maximum number of commits per day (default: 2).
- `--timezone ZZZZ`: Timezone offset for commit timestamps (default: `0000`).
- `--rewrite`: Delete the existing `.git` directory and re-initialize the repository, starting history from scratch. The script will remember and restore the remote URL if present.
- `--dry_run`: Simulate all actions and print what would be done, without making any changes.

### Example

```bash
python main.py --from 2024-06-17 --to now --commit_count 3 --timezone 0000 --rewrite
```

## Rewriting Remote History

If you use `--rewrite`, your local git history will start from scratch. To ensure the remote repository matches your new local history (and does not append to the old commits), you must force-push to the remote after running the script:

```bash
git push --force origin main
```

This will overwrite the remote branch (`main`) with your new commit history. **Be careful:** this will remove all previous commits from the remote branch.

This works in both normal and dry run modes.

## License

This project is licensed under the MIT License.
