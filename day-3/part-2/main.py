import os
import re
from typing import List, Tuple

def find_commands(text: str) -> List[str]:
  pattern = r"(mul\(\d+,\d+\)|do\(\)|don't\(\))"
  return re.findall(pattern, text)

def find_multipliers(text: str) -> List[Tuple[str, str]]:
  pattern = r"mul\((\d+),(\d+)\)"
  return re.findall(pattern, text)

def find_within_do_donts(text: str) -> List[str]:
  pattern = r"do\(\)(.*?)don't\(\)"
  return re.findall(pattern, text)

def process_file(file_name) -> None:
  try:
    with open(file_name, "r") as file:
      lines = file.readlines()

    # Extract commands from all lines
    all_commands = [cmd for line in lines for cmd in find_commands(line)]

    # Append `do()` at the start and `don't()` at the end
    all_commands_list = ['do()'] + all_commands + ["don't()"]

    # Extract text between `do()` and `don't()`
    within_do_donts_list = find_within_do_donts(''.join(all_commands_list))

    # Find all multiplier pairs within the extracted text
    multipliers_list = find_multipliers(''.join(within_do_donts_list))

    # Calculate reports
    reports = [int(x) * int(y) for x, y in multipliers_list]

    # Output results
    print(f"Sum of all reports: {sum(reports)}")

  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")

# Specify the file name and process it
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
