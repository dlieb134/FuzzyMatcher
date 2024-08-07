import pandas as pd
from fuzzywuzzy import fuzz, process
from multiprocessing import Pool, cpu_count
import time


def normalize_name(name: str) -> str:
    """
    Normalizes a name by stripping whitespace and converting to lowercase.

    Args:
        name (str): The name to normalize.

    Returns:
        str: The normalized name.
    """
    return name.strip().lower()


def find_matches_and_scores(args) -> tuple:
    """
    Finds matches and their scores based on a given normalized name.

    Args:
        args (tuple): A tuple containing the index, normalized name, and original data.

    Returns:
        tuple: A tuple containing the index and a string of matches.
    """
    index, normalized_name, original_data = args
    matches = []
    for idx, row in original_data.iterrows():
        score = fuzz.token_set_ratio(normalized_name, normalize_name(row['supplier_name']))
        if score > 89:
            matches.append(f"{row['supplier_name']}|{row['VENDOR_ID']}|{idx}|{score}")
    return index, ', '.join(matches)


def process_suppliers(input_file: str, output_file: str) -> None:
    """
    Processes suppliers by finding potential matches and their scores.

    Args:
        input_file (str): The path to the input file.
        output_file (str): The path to the output file.

    Returns:
        None
    """
    # Load the data
    data = pd.read_csv(input_file)
    print("Data loaded successfully.")

    # Normalize names
    data['Normalized_Name'] = data['supplier_name'].apply(normalize_name)
    print("Normalized names.")

    total_rows = data.shape[0]
    args = [(idx, row['Normalized_Name'], data) for idx, row in data.iterrows()]

    # Use multiprocessing for fuzzy matching
    results = []

    with Pool(processes=cpu_count()) as pool:
        for idx in range(total_rows):
            result = pool.apply_async(find_matches_and_scores, (args[idx],))
            results.append(result)

            # Print progress
            if (idx + 1) % 10 == 0 or (idx + 1) == total_rows:
                completed_pct = (idx + 1) / total_rows * 100
                print(f"Processing: {completed_pct:.2f}% completed.")

        # Collect results
        output = [r.get() for r in results]

    # Create output DataFrame
    result_dict = {index: match for index, match in output}
    data['Potential_Matches'] = data.index.map(result_dict)
    print("Potential matches computed.")

    # Save results to Excel
    data.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Output saved to {output_file}")


if __name__ == "__main__":
    input_file = "ARS Supplier Norm 0807.csv"
    output_file = "output_suppliers_score_90.xlsx"
    start_time = time.time()
    process_suppliers(input_file, output_file)
    end_time = time.time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")
