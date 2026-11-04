# AGENTS

## Repo shape
- This repo is notebook-only: `00_intro.ipynb` through `05_td.ipynb` plus images in `pics/`; there is no package/module layout, no CI, and no build/test/lint config.
- `06_mf.ipynb` exists but is currently empty (0 lines).
- Several notebooks include `Open in Colab` links pointing to `juansensio/axr`; treat this repo as local educational copies of those notebooks.

## Working conventions for edits
- Keep changes narrowly scoped to the target notebook; avoid broad reformatting of `.ipynb` JSON.
- Preserve notebook metadata (`kernelspec`, `language_info`) unless the task explicitly asks to update runtime details.
- Do not remove committed outputs by default; these notebooks intentionally contain saved outputs/figures.
- Content is written in Spanish; keep language/style consistent when editing markdown cells.

## Runtime assumptions (inferred from notebook code)
- Use Python 3 with an IPython/Jupyter kernel (`python3`); notebook metadata shows Python 3.9.x to 3.10.6 across files.
- Common imports used across notebooks: `numpy`, `matplotlib`, `tqdm`, plus occasional `pandas` and `pickle`.
- Some experiments set random seeds (for example `np.random.seed(42)` in `01_bandits.ipynb`); preserve seeded behavior when modifying experiment logic.

## Quick verification
- Preferred check is notebook execution for only the modified notebook (Run All in Jupyter/Colab) and confirm cells complete without errors.
- If plotting/training cells are expensive, run only affected sections and verify key outputs still render.
