import os

def are_close(a, b, limit=3):
  if a == b:
    return False
  return abs(a - b) <= limit

def is_sorted(arr):
  ascending = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
  descending = all(arr[i] >= arr[i + 1] for i in range(len(arr) - 1))
  return ascending or descending

def are_close_and_sorted(arr):
  are_close_list = [are_close(arr[i], arr[i + 1]) for i in range(len(arr) - 1)]
  return is_sorted(arr) and are_close_list.count(False) == 0

def can_pass_by_removing_one(arr):
  if are_close_and_sorted(arr):
    return True

  for i in range(len(arr)):
    modified_arr = arr[:i] + arr[i + 1:]
    if are_close_and_sorted(modified_arr):
      return True

  return False

def process_file(file_name):
  try:
    reports = []
    with open(file_name, "r") as file:
      for line in file:
        report = [*map(int, line.split())]
        reports.append(can_pass_by_removing_one(report))

    print(f"Found total reports: {len(reports)}")
    print(f"Found total valid reports: {reports.count(True)}")
    print(f"Found total invalid reports: {reports.count(False)}")

  except FileNotFoundError:
      print(f"Error: File '{file_name}' not found.")
  except ValueError:
      print("Error: File contains non-integer values.")

if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
