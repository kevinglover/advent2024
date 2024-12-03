def process_file(file_name):
  """Process the file to compute a frequency list and its sum."""
  try:
    # Read and split data into two columns
    with open(file_name, "r") as file:
      column1, column2 = zip(*[map(int, line.split()) for line in file if len(line.split()) == 2])

    # Sort the columns
    column1 = sorted(column1)
    column2 = sorted(column2)

    # Calculate the frequency list
    frequency_list = [
      value * column2.count(value) for value in column1 if value in column2
    ]

    # Output results
    print("\nFrequency List:", frequency_list)
    print("\nSum of Frequency Scores:", sum(frequency_list))

  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
  except ValueError:
    print("Error: File contains non-integer or improperly formatted values.")

# Specify the file name and process it
if __name__ == "__main__":
  FILE_NAME = "advent2024/day-1/data.txt"
  process_file(FILE_NAME)
