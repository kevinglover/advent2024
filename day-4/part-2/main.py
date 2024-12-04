import os
from typing import List

def check_letter(letter: str) -> bool:
  """Check if the letter is M or S."""
  return letter == 'M' or letter == 'S'

def get_pair_letter(letter: str) -> str:
  """Return the paired letter (M <-> S)."""
  if letter == 'M':
    return 'S'
  elif letter == 'S':
    return 'M'
  return ''

def find_xmas_crossing(rows: List[str]) -> int:
  count = 0
  num_rows = len(rows)

  # Iterate through each row and column (excluding the edges)
  # Skip first and last row
  for row_idx in range(1, num_rows - 1):
    row = rows[row_idx]
    upper_row = rows[row_idx - 1]
    lower_row = rows[row_idx + 1]

    # Skip first and last column
    for col_idx in range(1, len(row) - 1):
      # Check if we have an 'A' in the middle
      if row[col_idx] == 'A':
        # Check the row above and row below for valid pairs
        upper_left = upper_row[col_idx - 1]
        upper_right = upper_row[col_idx + 1]
        lower_left = lower_row[col_idx - 1]
        lower_right = lower_row[col_idx + 1]

        # Check for valid pairings:
        if check_letter(upper_left) and check_letter(upper_right) and (
            lower_right == get_pair_letter(upper_left) and lower_left == get_pair_letter(upper_right)):
          count += 1

  return count

def process_file(file_name: str):
  try:
    rows = []
    with open(file_name, "r") as file:
      for row in file:
        # Collect rows
        rows.append(row.strip())

    # Count the number of valid 'MAS' patterns crossing at 'A'
    total_matches = find_xmas_crossing(rows)

    print(f"Found total number of xmas-es: {total_matches}")

  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
  except ValueError:
    print("Error: File contains non-integer values.")


# Specify the file name and process it
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
