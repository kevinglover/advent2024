import os
from multiprocessing import Pool, cpu_count
from typing import List, Tuple, Dict, Set, Union

# Global debug flag
debug: bool = False  # Set this to `True` to enable more detailed logs

Grid = List[List[str]]  # A 2D list of strings
Position = Tuple[int, int]  # A tuple of (row, column)
Path = Dict[Position, str]  # A dictionary mapping positions to movement symbols
SimulationResult = Tuple[bool, Path] # A tuple representing the outcome of the guard simulation


def simulate_guard_no_grid_update(grid: str) -> SimulationResult:
  grid: Grid = [list(row) for row in grid.split("\n")]
  rows: int = len(grid)

  directions: List[str] = ["^", ">", "v", "<"]
  moves: Dict[str, Tuple[int, int]] = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

  start_pos: Union[Position, None] = None
  current_direction: Union[str, None] = None

  for r in range(rows):
    for c in range(len(grid[r])):
      if grid[r][c] in directions:
        start_pos = (r, c)
        current_direction = grid[r][c]
        break
    if start_pos:
      break

  def within_bounds(x: int, y: int) -> bool:
    return 0 <= x < rows and 0 <= y < len(grid[x])

  path: Path = {}
  visited: Set[Tuple[int, int, str]] = set()
  x, y = start_pos

  while True:
    state = (x, y, current_direction)
    if state in visited:
      if debug:
        print(f"Infinite loop detected at: {state}")
      # Infinite loop detected
      return False, path
    visited.add(state)

    dx, dy = moves[current_direction]
    nx, ny = x + dx, y + dy

    if not within_bounds(nx, ny):
      if debug:
        print(f"Guard escapes at: ({x}, {y})")
      # Guard escapes
      return True, path

    if grid[nx][ny] != '#':
      x, y = nx, ny
      if (x, y) in path:
        path[(x, y)] = '+'
      elif dx != 0:
        path[(x, y)] = '|'
      elif dy != 0:
        path[(x, y)] = '-'
    else:
      current_index = directions.index(current_direction)
      current_direction = directions[(current_index + 1) % len(directions)]

      blocked = True
      for d in directions:
        dx, dy = moves[d]
        nx, ny = x + dx, y + dy
        if within_bounds(nx, ny) and grid[nx][ny] != '#':
          blocked = False
          break
      if blocked:
        if debug:
          print(f"Guard is trapped at: ({x}, {y})")
        # Guard is trapped
        return False, path


def simulate_with_obstacle(grid: str, obstacle_pos: Position) -> Tuple[bool, Position, Path]:
  original_grid: Grid = [list(row) for row in grid.split("\n")]
  x, y = obstacle_pos
  test_grid: Grid = [row[:] for row in original_grid]
  test_grid[x][y] = '#'
  test_grid_str = "\n".join("".join(row) for row in test_grid)
  escaped, path = simulate_guard_no_grid_update(test_grid_str)
  return not escaped, obstacle_pos, path


def visualize_grid(grid: str, new_obstruction: Position, path: Path) -> str:
  grid: Grid = [list(row) for row in grid.split("\n")]
  x, y = new_obstruction
  grid[x][y] = 'O'
  for (px, py), symbol in path.items():
    grid[px][py] = symbol
  return "\n".join("".join(row) for row in grid)


def count_trapping_options_parallel(grid: str) -> Tuple[int, List[Position], List[str]]:
  original_grid: Grid = [list(row) for row in grid.split("\n")]
  rows: int = len(original_grid)

  candidates: List[Position] = [
    (r, c)
    for r in range(rows)
    for c in range(len(original_grid[r]))
    if original_grid[r][c] == '.'
  ]

  with Pool(cpu_count()) as pool:
    results = pool.starmap(simulate_with_obstacle, [(grid, pos) for pos in candidates])

  trapping_positions: List[Position] = []
  visualizations: List[str] = []

  for is_trapping, position, path in results:
    if is_trapping:
      trapping_positions.append(position)
      visualization = visualize_grid(grid, position, path)
      visualizations.append(visualization)

  return len(trapping_positions), trapping_positions, visualizations


def process_file(file_name: str) -> None:
  try:
    with open(file_name, "r") as file:
      grid = "\n".join(line.rstrip() for line in file.readlines())

    if debug:
      print(f"Grid template:\n{grid}")

    trapping_count, trapping_positions, visualizations = count_trapping_options_parallel(grid)
    print(f"Number of trapping options: {trapping_count}")
    if debug:
      print(f"Trapping positions: {trapping_positions}")
      for i, visualization in enumerate(visualizations, 1):
        print(f"\n======== Option {i} ========\n{visualization}")

  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
  except ValueError:
    print("Error: File contains invalid values.")


if __name__ == "__main__":
  script_dir = os.path.dirname(os.path.realpath(__file__))
  file_path = os.path.join(script_dir, "../data.txt")
  process_file(file_path)
