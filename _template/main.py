def process_file(file_name):
  try:
    reports = []
    with open(file_name, "r") as file:
      for line in file:
        report = [*map(int, line.split())]
        reports.append(report)

    print(f"Found total reports: {len(reports)}")

  except FileNotFoundError:
      print(f"Error: File '{file_name}' not found.")
  except ValueError:
      print("Error: File contains non-integer values.")

# Specify the file name and process it
if __name__ == "__main__":
  FILE_NAME = "data.txt"
  process_file(FILE_NAME)
