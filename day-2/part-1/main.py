def are_close(a, b, limit = 3):
  if a == b:
    return False

  return abs(a - b) <= limit

def is_sorted(arr = []):
  if len(arr) == 2:
    return True

  if all(arr[i] <= arr[i + 1] and are_close(arr[i], arr[i + 1]) for i in range(len(arr) - 1)):
    return True

  if all(arr[i] >= arr[i + 1] and are_close(arr[i], arr[i + 1]) for i in range(len(arr) - 1)):
    return True

  return False

def process_file(file_name):
  try:
    reports = []
    with open(file_name, "r") as file:
      for line in file:
        report = [*map(int, line.split())]
        reports.append(is_sorted(report))

    print(f"Found total reports: {len(reports)}")
    print(f"Found total valid reports: {reports.count(True)}")
    print(f"Found total invalid reports: {reports.count(False)}")

  except FileNotFoundError:
      print(f"Error: File '{file_name}' not found.")
  except ValueError:
      print("Error: File contains non-integer values.")

# Specify the file name and process it
if __name__ == "__main__":
  FILE_NAME = "advent2024/day-2/data.txt"
  process_file(FILE_NAME)
