# Hybrid-BCI-Wheelchair — Companion Code & Materials

[![Paper](https://img.shields.io/static/v1?label=Paper&message=ResearchGate&color=informational)](https://www.researchgate.net/profile/Mansi-Kambli/publication/356207033_Design_and_Implementation_of_Hybrid_BCI_based_Wheelchair/links/67bd46d2f5cb8f70d5be9f56/Design-and-Implementation-of-Hybrid-BCI-based-Wheelchair.pdf)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://github.com/NeuArv/hybrid-bci-wheelchair/actions/workflows/python-app.yml/badge.svg)](https://github.com/NeuArv/hybrid-bci-wheelchair/actions)

**Title:** Design and Implementation of Hybrid BCI based Wheelchair

**Authors / Source:** Arvind Gyandatt Mishra, Poonam Chawda, Heeral Dedhia, Arvind Sridhar, Prof. Mansi Kambli, Prof. Sushma Kadge
**PDF (source):** https://www.researchgate.net/profile/Mansi-Kambli/publication/356207033_Design_and_Implementation_of_Hybrid_BCI_based_Wheelchair/links/67bd46d2f5cb8f70d5be9f56/Design-and-Implementation-of-Hybrid-BCI-based-Wheelchair.pdf

## Description
This repository is a companion scaffold for the paper "Design and Implementation of Hybrid BCI based Wheelchair". It provides a structure for code, data, and reproducible scripts related to hybrid brain–computer interface (BCI) control of a wheelchair. The repo intentionally does not include the original PDF; use the ResearchGate link above to access the paper. Respect copyright and redistribution terms of the original publisher.

## Contents (scaffold)
- `src/hybrid_bci/` — package for core models, signal processing, and control logic 
- `scripts/` — reproducible scripts (e.g., `run_demo.py`, `process_data.py`)
- `notebooks/` — Jupyter notebooks for analysis and figures
- `data/` — small example data or metadata 
- `tests/` — pytest tests for core functionality
- `docs/` — supplementary documentation and method notes
- `CITATION.bib`, `CITATION.cff` — citation metadata
- `.github/workflows/python-app.yml` — CI (tests + lint)

## Quick start (developer)
1. Create a Python virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
```

2. Run demo script (placeholder):
```bash
python scripts/run_demo.py
```

3. Run tests:
```bash
pytest -q
```

## Citation
Please cite the original paper when using results from it. Example (bibtex) in `CITATION.bib`. If you use code from this repository, cite this repo as well.

## License & Notices
- Code in this repository is MIT licensed (see LICENSE).  
- The paper PDF is hosted on ResearchGate; check copyright and reuse permissions before redistribution. See `NOTICES.md` for guidance.

## Contact / Maintainer
Arvind Gyandatt Mishra — https://www.linkedin.com/in/arvind-gyandatt-mishra-a6760a16b/
