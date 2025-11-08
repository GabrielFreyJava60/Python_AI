# HW #31 — Game of Life Simulator

This repository contains a Python implementation of Conway’s Game of Life that follows the ruleset described in the [Game of Life Lexicon](https://playgameoflife.com/lexicon/) (see the *Explanation* tab) and the algorithm section of the Seeking Alpha interview task. The simulation evolves a 50×50 grid of cells and halts automatically once the image state stops changing (either a steady state or a discovered loop).

## Features

- **Random initial state**: Grid initialised with configurable alive probability (default 0.2).
- **Standard Game of Life rules**: Survival on 2–3 neighbours, birth on exactly 3.
- **Automatic termination**: Stops when the next generation equals the current one or a previously seen state (loop detection).
- **Image export**: Saves each generation as a PNG in `life_frames/` and optionally compiles the run into an animated GIF.
- **Configurable parameters**: Grid size, colours, cell size, generation cap, GIF timing, and random seed.

## Project Structure

- `game_of_life.py` — main module with configuration dataclass, simulation engine, rendering helpers, and CLI entry point.
- `requirements.txt` — runtime dependencies (Pillow, Plotly, Kaleido, ipywidgets for notebook integration if required).
- `.gitignore` — ignores generated media directories and binaries.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

> **Note:** Kaleido is used by Plotly for static image export. If you only need the CLI simulation and GIF generation, Pillow is sufficient.

## Usage

Run the simulation from the command line:

```bash
python3 game_of_life.py
```

After execution you will see:

- Console summary with number of generations simulated and ASCII representation of the final grid.
- PNG frames inside `life_frames/`.
- `life_simulation.gif` (if GIF output enabled in `LifeConfig`).

To customise behaviour, edit `LifeConfig` in `game_of_life.py` or pass alternative values when calling `run_simulation`.

## Verification Checklist

- Rules match the official Game of Life specification and the Seeking Alpha task description.
- Grid dimensions default to 50×50 and can be adjusted.
- Simulation halts when successive frames repeat (steady state) or a loop is detected.
- Image output reflects the cell grid exactly.

## References

- Game of Life Lexicon — [https://playgameoflife.com/lexicon/](https://playgameoflife.com/lexicon/)
- Seeking Alpha Interview Task — algorithm section (client-side React assignment reused for Python implementation requirements)
