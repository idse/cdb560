# CDB560 Quantitative Cell Biology

This is the repository for a course in which biologists learn to analyze real
microscopy data in Python. Most users have little or no coding experience.
Help them do real analysis *and* understand it.

## Working with students
- Explain what the code does in plain language, briefly, especially anything new.
- Prefer simple, readable code over clever or compact code.
- Show intermediate results (images, masks, plots) so steps can be checked by eye.
- If a result looks biologically implausible or a step is questionable, say so.
- Don't claim results you haven't checked by running the code.

## Environment
- uv project. Add packages with `uv add`, run with `uv run`. No conda, no pip,
  never activate environments manually.
- If the environment seems broken: `rm -rf .venv && uv sync`.

## Notebooks
- Plain `.py` files with `# %%` cell markers, run in VS Code's Interactive Window.
  Markdown cells use `# %% [markdown]` with the text as `#` comment lines.
- Each lecture has its own folder in `lectures/`.
- Data lives outside the repo; never copy data into it. Each notebook sets
  `DATA_DIR = Path("...")` once, in its first code cell, and builds all paths from it.
- Every notebook must run top to bottom without errors as a plain script.

## Style
- Short cells, one idea each, with a markdown cell explaining what and why.
- Descriptive variable names; comments for anything non-obvious.
- Plots: labeled axes with units, readable font sizes, grayscale for single channels.
- Stick to numpy, matplotlib, scikit-image and tifffile unless something else is
  really needed (cellpose for segmentation).

## Checking
- Run `MPLBACKEND=Agg uv run python <notebook>.py` to check a notebook runs top to bottom.
