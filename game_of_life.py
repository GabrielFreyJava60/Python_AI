import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from PIL import Image


@dataclass(frozen=True)
class LifeConfig:
    rows: int = 50
    cols: int = 50
    alive_probability: float = 0.2
    cell_size: int = 10
    alive_color: Tuple[int, int, int] = (0, 0, 0)
    dead_color: Tuple[int, int, int] = (255, 255, 255)
    max_generations: int = 500
    output_dir: Path = Path("life_frames")
    gif_filename: Optional[Path] = Path("life_simulation.gif")
    gif_duration_ms: int = 300


Grid = List[List[int]]


def create_random_grid(rows: int, cols: int, alive_probability: float, seed: Optional[int] = None) -> Grid:
    if not 0.0 <= alive_probability <= 1.0:
        raise ValueError("alive_probability must be between 0 and 1")

    rng = random.Random(seed)
    return [[1 if rng.random() < alive_probability else 0 for _ in range(cols)] for _ in range(rows)]


def count_neighbors(grid: Grid, row: int, col: int) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r = row + dr
            c = col + dc
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 1:
                count += 1
    return count


def tick(grid: Grid) -> Grid:
    rows = len(grid)
    cols = len(grid[0])
    next_grid: Grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            neighbors = count_neighbors(grid, r, c)
            cell_alive = grid[r][c] == 1
            if cell_alive and neighbors in (2, 3):
                next_grid[r][c] = 1
            elif not cell_alive and neighbors == 3:
                next_grid[r][c] = 1
            else:
                next_grid[r][c] = 0
    return next_grid


def grid_to_image(grid: Grid, config: LifeConfig) -> Image.Image:
    rows = len(grid)
    cols = len(grid[0])
    width = cols * config.cell_size
    height = rows * config.cell_size

    img = Image.new("RGB", (width, height), color=config.dead_color)
    pixels = img.load()

    for r in range(rows):
        for c in range(cols):
            color = config.alive_color if grid[r][c] == 1 else config.dead_color
            top = r * config.cell_size
            left = c * config.cell_size
            for y in range(top, top + config.cell_size):
                for x in range(left, left + config.cell_size):
                    pixels[x, y] = color
    return img


def grids_equal(a: Grid, b: Grid) -> bool:
    return all(cell_a == cell_b for row_a, row_b in zip(a, b) for cell_a, cell_b in zip(row_a, row_b))


def grid_key(grid: Grid) -> Tuple[Tuple[int, ...], ...]:
    return tuple(tuple(row) for row in grid)


def run_simulation(config: LifeConfig, seed: Optional[int] = None) -> Tuple[Grid, int]:
    grid = create_random_grid(config.rows, config.cols, config.alive_probability, seed=seed)
    seen_states = {grid_key(grid)}

    frames: List[Image.Image] = []
    config.output_dir.mkdir(parents=True, exist_ok=True)

    generation = 0
    final_generation = config.max_generations

    while generation <= config.max_generations:
        # Render and persist current generation
        image = grid_to_image(grid, config)
        frame_path = config.output_dir / f"generation_{generation:04d}.png"
        image.save(frame_path)
        frames.append(image)

        next_grid = tick(grid)

        if grids_equal(grid, next_grid):
            final_generation = generation
            break

        next_key = grid_key(next_grid)
        if next_key in seen_states:
            generation += 1
            grid = next_grid
            image = grid_to_image(grid, config)
            frame_path = config.output_dir / f"generation_{generation:04d}.png"
            image.save(frame_path)
            frames.append(image)
            final_generation = generation
            break

        seen_states.add(next_key)
        grid = next_grid
        generation += 1
    else:
        final_generation = config.max_generations

    if config.gif_filename and frames:
        gif_path = Path(config.gif_filename)
        gif_path.parent.mkdir(parents=True, exist_ok=True)
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=config.gif_duration_ms,
            loop=0,
        )

    return grid, final_generation


def life_to_text(grid: Grid) -> str:
    return "\n".join("".join("█" if cell else "·" for cell in row) for row in grid)


def main(args: Optional[Sequence[str]] = None) -> None:
    config = LifeConfig()
    final_grid, generations = run_simulation(config)
    print(f"Simulation finished after {generations} generations")
    print("Final grid:")
    print(life_to_text(final_grid))


if __name__ == "__main__":
    main()
