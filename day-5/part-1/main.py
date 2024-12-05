import os
from typing import List, Tuple

def get_rules_for_update(rules: List[Tuple[int, int]], update: List[int]) -> List[Tuple[int, int]]:
  """Filter rules that are applicable to a given update."""
  return [rule for rule in rules if all(page_num in update for page_num in rule)]

def is_update_valid_by_rules(update: List[int], rules: List[Tuple[int, int]]) -> bool:
  """Check if an update respects the given rules."""
  if not rules:
    return True # No rules to validate against means the update is valid.

  for first, second in rules:
    if first in update and second in update and update.index(first) > update.index(second):
      return False # Rule violated.
  return True

def get_middle_page(update: List[int]) -> int:
  """Get the middle page from the update."""
  if not update:
    raise ValueError("Cannot determine the middle page of an empty update.")
  return update[len(update) // 2]

def parse_file(file_name: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
  """Parse the file and extract rules and updates."""
  rules = []
  updates = []
  try:
    with open(file_name, "r") as file:
      scanning_for_rules = True
      for line in file:
        line = line.strip()
        if not line:
          scanning_for_rules = False
          continue
        if scanning_for_rules:
          rules.append(tuple(map(int, line.split('|'))))
        else:
          updates.append(list(map(int, line.split(','))))
  except FileNotFoundError:
    raise FileNotFoundError(f"Error: File '{file_name}' not found.")
  except ValueError:
    raise ValueError("Error: File contains non-integer values.")
  return rules, updates

def process_file(file_name: str):
  """Process the file and print the results."""
  try:
    rules, updates = parse_file(file_name)

    valid_updates = [
      update
      for update in updates
      if is_update_valid_by_rules(update, get_rules_for_update(rules, update))
    ]

    middle_pages = [get_middle_page(update) for update in valid_updates]

    print(f"Found total valid updates: {len(valid_updates)}")
    print(f"Valid updates: {valid_updates}")
    print(f"List of middle pages: {middle_pages}")
    print(f"Sum of middle pages: {sum(middle_pages)}")

  except (FileNotFoundError, ValueError) as e:
    print(e)

if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
