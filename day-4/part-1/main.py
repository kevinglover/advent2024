import os
import re
from typing import List

def find_xmas(text: str) -> List[str]:
  # Lookahead for overlapping matches
  pattern = r"(?=(XMAS|SAMX))"
  return re.findall(pattern, text)

def rotate_rows(rows: List[str]) -> List[str]:
  return [''.join(row) for row in zip(*rows)]

def shift_columns(rows: List[str]) -> List[str]:
  result = []
  max_len = max(len(row) for row in rows)

  # Iterate over all rows and "shift" characters column by column
  for i in range(max_len):
    for j in range(len(rows)):
      if i < len(rows[j]):
        # Append characters in the staggered order to the result list
        if i + j < len(result):
          result[i + j] += rows[j][i]
        else:
          result.append(rows[j][i])

  return result

def process_file(file_name):
  try:
    rows = []
    matches = []
    with open(file_name, "r") as file:
      for row in file:
        # Find matches for the row
        matches.append(find_xmas(row))

        # Collect rows
        rows.append(row.strip())

    # Find matches for the columns
    columns = rotate_rows(rows)
    for line in columns:
      matches.append(find_xmas(line))

    # Find matches left-diagonal
    shifted_left = shift_columns(columns)
    for line in shifted_left:
      matches.append(find_xmas(line))

    # Find matches right-diagonal
    shifted_right = shift_columns([line[::-1] for line in columns])
    for line in shifted_right:
      matches.append(find_xmas(line))

    print(f"Found total number of xmas-es: {sum(len(matched) for matched in matches)}")

  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
  except ValueError:
    print("Error: File contains non-integer values.")

# Specify the file name and process it
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
