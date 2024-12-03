def process_file(file_name):
  """Process the file, sort columns, and calculate differences."""
  try:
    # Read and split data into two columns
    column1, column2 = [], []
    with open(file_name, "r") as file:
      for line in file:
        values = line.split()
        if len(values) == 2:
          column1.append(int(values[0]))
          column2.append(int(values[1]))

    # Sort the columns
    column1.sort()
    column2.sort()

    # Ensure columns are comparable
    if len(column1) != len(column2):
      print(f"Cannot compare columns of different lengths: {len(column1)} vs {len(column2)}")
      return

    # Calculate the differences and their sum
    diff_list = [abs(c2 - c1) for c1, c2 in zip(column1, column2)]
    print("Sorted Column 1:", column1)
    print("\nSorted Column 2:", column2)
    print("\nDifference List:", diff_list)
    print("\nSum of Differences:", sum(diff_list))

  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
  except ValueError:
    print("Error: File contains non-integer values.")

# Specify the file name and process it
if __name__ == "__main__":
  FILE_NAME = "advent2024/day-1/data.txt"
  process_file(FILE_NAME)
