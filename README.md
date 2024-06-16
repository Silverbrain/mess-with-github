# Random Git Commit Generator

This script generates random commits in a Git repository over a specified date range. It creates or modifies a file and commits the changes with random timestamps, simulating activity over time. 

## Features

- Generates random commit timestamps between two specified dates.
- Ensures commits are made in chronological order.
- Simulates weekend activity with reduced commit probability.
- Initializes a Git repository if one doesn't exist.
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

1. **Navigate to the directory containing the script:**

   ```bash
   cd mess-with-github
   ```

2. **Run the script:**

   ```bash
   python main.py
   ```

## Script Details

### Functions

- **`random_date(start, end)`**
  Generates a random datetime between two datetime objects.

- **`create_random_commit(start_date, end_date, commit_count, timezone="0000")`**
  Creates a specified number of random commits between `start_date` and `end_date`.

- **`get_random_commit_count(date)`**
  Determines the number of random commits to create for a given date, simulating reduced activity on weekends.

### Main Execution

1. Defines the start date with setting the `date` and `delta` variable accordingly to calculates the number of days to the current date.
2. Initializes a Git repository if one doesn't exist.
3. Iterates over each day in the date range, determining the number of commits for each day and creating them.

## Customization

- **Start and End Dates:**
  Modify the `date` variable in the `__main__` block to change the start date.

- **Time Zone:**
  Adjust the `TZ` variable to set a different time zone for the commit timestamps.

## License

This project is licensed under the MIT License.
