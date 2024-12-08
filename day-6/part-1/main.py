import os
from typing import List, Tuple, Set

# A 2D list of strings
Grid = List[List[str]]
# A tuple of (row, column)
Position = Tuple[int, int]

def simulate_guard(grid: str) -> Tuple[Set[Position], List[str]]:
  # Convert the grid into a mutable list of lists
  grid = [list(row) for row in grid.split("\n")]
  rows = len(grid)

  # Define directions and their movements
  directions = ["^", ">", "v", "<"]
  moves = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

  # Locate the guard's starting position and direction
  start_pos = None
  current_direction = None
  for r in range(rows):
    for c in range(len(grid[r])):
      if grid[r][c] in directions:
        start_pos = (r, c)
        current_direction = grid[r][c]
        break
    if start_pos:
      break

  def within_bounds(x: int, y: int) -> bool:
    # Dynamically check row and column bounds
    return 0 <= x < rows and 0 <= y < len(grid[x])

  # Simulate the guard's movement
  # Use a set to store unique positions
  path: Set[Position] = set()
  x, y = start_pos

  while True:
    # Compute the next position
    dx, dy = moves[current_direction]
    nx, ny = x + dx, y + dy

    if not within_bounds(nx, ny):
      # guard escapes the grid
      print(f"guard escaped the grid at position ({nx}, {ny}).")
      break

    if grid[nx][ny] != '#':
      # Move straight if no obstacle
      x, y = nx, ny
      # Add the new position to the path
      path.add((x, y))
      # Mark only if still within bounds
      if within_bounds(x, y):
        grid[x][y] = 'X'
    else:
      # Rotate 90 degrees to the right
      current_index = directions.index(current_direction)
      current_direction = directions[(current_index + 1) % len(directions)]

      # Check if all directions are blocked (edge case)
      blocked = True
      for d in directions:
        dx, dy = moves[d]
        nx, ny = x + dx, y + dy
        if within_bounds(nx, ny) and grid[nx][ny] != '#':
          blocked = False
          break
      if blocked:
        break

  return path, [''.join(row) for row in grid]

def find_all_X(grid: List[str]) -> List[Position]:
  coordinates = []
  for r, row in enumerate(grid):
    for c, cell in enumerate(row):
      if cell == 'X':
        coordinates.append((r, c))
  return coordinates

def process_file(file_name):
  try:
    grid = ''
    with open(file_name, "r") as file:
      # Read the file, strip trailing newlines, and join to a new grid
      grid = "\n".join(line.strip() for line in file.readlines())

    print(f"Grid template: \n{grid}")

    # Run the simulation
    path, final_grid = simulate_guard(grid)
    print(f"Path: {path}")
    print("Final grid template:")
    print("\n".join(final_grid))
    print(f"Distinct paths: {len(find_all_X(final_grid))}")

  except FileNotFoundError:
      print(f"Error: File '{file_name}' not found.")
  except ValueError:
      print("Error: File contains non-integer values.")

# Specify the file name and process it
if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
