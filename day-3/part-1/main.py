import re

def process_file(file_name):
  try:
    reports = []
    mul_pattern = r"mul\((\d+),(\d+)\)"

    with open(file_name, "r") as file:
      for line in file:
        multipliers = re.findall(mul_pattern, line)
        report = [int(x) * int(y) for x, y in multipliers]
        print(f"Report: {report}\n")
        reports.append(report)

    print(f"Found total reports: {len(reports)}")
    print(f"Sum of all reports: {sum(item for report in reports for item in report)}")

  except FileNotFoundError:
      print(f"Error: File '{file_name}' not found.")
  except ValueError:
      print("Error: File contains non-integer values.")

# Specify the file name and process it
if __name__ == "__main__":
  FILE_NAME = "advent2024/day-3/data.txt"
  process_file(FILE_NAME)
