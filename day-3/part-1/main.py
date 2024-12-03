import os
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

# Specify the file name and process it
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
