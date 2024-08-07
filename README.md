# Fuzzy Supplier Matcher

## Overview

This Python script processes a CSV file containing supplier information and finds potential matches using fuzzy string matching. It's designed to handle large datasets efficiently using multiprocessing.

## Features

- Normalizes supplier names for consistent comparison
- Uses fuzzy string matching to find potential duplicates
- Employs multiprocessing for improved performance
- Provides progress updates during processing
- Outputs results to an Excel file

## Requirements

- Python 3.x
- pandas
- fuzzywuzzy
- openpyxl

Install the required packages using:

## Usage

1. Place your input CSV file (named `supps.csv`) in the same directory as the script.
2. Run the script: `python main.py`
3. The script will process the data and save the results to `output_suppliers_score_90.xlsx`.

## How it works

1. **Data Loading**: The script reads the input CSV file using pandas.

2. **Name Normalization**: Supplier names are normalized by converting to lowercase and removing leading/trailing whitespace.

3. **Fuzzy Matching**: The script uses the `fuzzywuzzy` library to compare normalized names. It calculates a similarity score using the token set ratio algorithm.

4. **Multiprocessing**: To improve performance, the script utilizes Python's multiprocessing capabilities, distributing the workload across available CPU cores.

5. **Match Filtering**: Only matches with a similarity score above 89 are considered potential matches.

6. **Progress Tracking**: The script provides progress updates every 10 rows processed.

7. **Result Compilation**: Matches are compiled into a new column in the DataFrame.

8. **Output**: Results are saved to an Excel file, including all original data and the new "Potential_Matches" column.

## Customization

- Adjust the similarity score threshold (currently set to 89) in the `find_matches_and_scores` function.
- Modify input and output file names in the `__main__` section.

## Performance

The script uses multiprocessing to leverage multiple CPU cores, significantly improving processing speed for large datasets. The total processing time is printed upon completion.

## Note

This script is designed for large datasets. For smaller datasets, consider removing the multiprocessing logic to simplify the code.