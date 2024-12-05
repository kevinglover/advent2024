from collections import defaultdict, deque
import os
from typing import List, Tuple

def get_rules_for_update(rules: List[Tuple[int, int]], update: List[int]) -> List[Tuple[int, int]]:
  """Filter rules applicable to a given update."""
  return [rule for rule in rules if all(page_num in update for page_num in rule)]

def is_update_valid_by_rules(update: List[int], rules: List[Tuple[int, int]]) -> bool:
  """Check if an update respects all applicable rules."""
  if not rules:
    return True

  for first, second in rules:
    if first in update and second in update and update.index(first) > update.index(second):
      return False
  return True

def correct_invalid_update(update: List[int], rules: List[Tuple[int, int]]) -> List[int]:
  """Correct an invalid update by reordering it to satisfy the rules."""
  graph = defaultdict(list)
  in_degree = {num: 0 for num in update}

  for a, b in rules:
    if a in update and b in update:
      graph[a].append(b)
      in_degree[b] += 1

  queue = deque([num for num in update if in_degree[num] == 0])
  sorted_list = []

  while queue:
    current = queue.popleft()
    sorted_list.append(current)
    for neighbor in graph[current]:
      in_degree[neighbor] -= 1
      if in_degree[neighbor] == 0:
        queue.append(neighbor)

  if len(sorted_list) != len(update):
    raise ValueError("The rules result in a cycle, so the list cannot be corrected.")

  return sorted_list

def get_middle_page(update: List[int]) -> int:
  """Get the middle element of a list."""
  if not update:
    raise ValueError("Cannot determine the middle page of an empty update.")
  return update[len(update) // 2]

def parse_file(file_name: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
  """Parse the file and return rules and updates."""
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
    return rules, updates
  except FileNotFoundError:
    raise FileNotFoundError(f"Error: File '{file_name}' not found.")
  except ValueError:
    raise ValueError("Error: File contains non-integer values.")

def process_updates(file_name: str):
  """Process updates from a file and print the results."""
  try:
    rules, updates = parse_file(file_name)
    invalid_updates = []
    corrected_updates = []

    for update in updates:
      applicable_rules = get_rules_for_update(rules, update)
      if not is_update_valid_by_rules(update, applicable_rules):
        invalid_updates.append(update)
        corrected_updates.append(correct_invalid_update(update, applicable_rules))

    print(f"Found total invalid updates: {len(invalid_updates)}")
    print(f"Invalid updates: {invalid_updates}")
    print(f"Corrected updates: {corrected_updates}")

    middle_pages = [get_middle_page(update) for update in corrected_updates]
    print(f"List of middle pages: {middle_pages}")
    print(f"Sum of middle pages: {sum(middle_pages)}")

  except (FileNotFoundError, ValueError) as e:
    print(e)

if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_updates(file_path)
