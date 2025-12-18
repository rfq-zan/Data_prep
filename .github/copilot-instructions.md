<!-- .github/copilot-instructions.md for Data_prep workspace -->
# Copilot / AI agent instructions — Data_prep

Purpose: help an AI coding assistant be productive in this small Streamlit data-prep project.

- **Big picture**: This repo is a lightweight Streamlit app for agricultural production analysis. Two top-level apps:
  - `Data_prep.py` — the primary interactive app that loads `data/data_asia.csv`, runs cleaning, transforms (adds `ln*` columns), visualizations, and PCA-based outlier detection.
  - `data_understanding.py` — a simpler Streamlit page that reads a CSV from Google Sheets and shows overview/plots.

- **Where code lives**: supporting logic is in `modules/`:
  - `modules/data_loader.py` — `load_data()` reads `data/data_asia.csv` and strips any columns beginning with `ln`.
  - `modules/preprocessing.py` — helpers: `summary_statistics()`, `handle_missing_values()` (numeric-only fill), `iqr_outlier_removal()`.
  - `modules/visualization.py` — plotting helpers return matplotlib `plt` objects: `histogram()`, `boxplot()`, `lineplot()`.
  - `modules/export_utils.py` — UI helpers; `download_csv()` works; PDF export functions are stubs.

- **Why some design choices matter (discoverable from code)**:
  - `Data_prep.py` adds the `modules` folder to `sys.path` at runtime (`sys.path.append(...)`) rather than using a package install. Keep relative imports intact when refactoring.
  - Data operations deliberately target numeric columns only (e.g., `select_dtypes(include=['number'])` and `handle_missing_values` fills numeric columns only). Be careful when changing this — non-numeric columns aren't included in these flows.
  - Log-transformed columns are prefixed with `ln` (e.g., `lnProduction`). `data_loader.load_data()` proactively removes existing `ln*` columns; maintain that invariant if you add new transforms.
  - Outlier detection in `Data_prep.py` uses PCA -> Euclidean distance -> 95th percentile threshold. If you change outlier logic, update UI text and any downstream assumptions.

- **Run / dev workflows** (practical commands):
  - Create an environment and install dependencies from `requirements.txt`.
    - Windows PowerShell example:
      ```powershell
      python -m venv .venv
      .\.venv\Scripts\Activate.ps1
      pip install -r requirements.txt
      ```
  - Launch apps:
    - `streamlit run Data_prep.py`
    - `streamlit run data_understanding.py`

- **Project-specific conventions & gotchas**:
  - Plots: visualization helpers return `matplotlib.pyplot` objects (not `Figure` objects). The Streamlit pages call `st.pyplot(plt)` directly with that returned `plt`.
  - Missing-value handling only fills numeric columns; categorical missing-value strategies are not implemented. Avoid changing `handle_missing_values` semantics without updating callers.
  - `export_utils.export_data_pdf` and `export_fig_to_pdf` are intentionally placeholder stubs — updates here should also update UI text so users aren't promised a working PDF export.
  - `data_understanding.py` pulls from a Google Sheets CSV URL — tests or offline runs should replace that URL with a local CSV or mock.

- **Integration / external dependencies**:
  - Data: `data/data_asia.csv` is the canonical local dataset. `data_understanding.py` additionally uses a Google Sheets export CSV URL.
  - Third-party libs: Streamlit, pandas, numpy, scikit-learn, seaborn, matplotlib. See `requirements.txt` for exact versions.

- **Safe small change checklist for PRs** (useful guardrails for AI edits):
  1. If you change `load_data()` path or behavior, update both apps that call it.
 2. If you modify `handle_missing_values()` ensure it still returns the full DataFrame and only mutates numeric columns, or update callers/tests.
 3. If you replace plotting return values (e.g., switching to `Figure` objects), update Streamlit call sites (`st.pyplot(fig)` vs `st.pyplot()` with global plt).
 4. If you implement PDF export, remove the placeholder writes in `export_utils.py` and test UX in Streamlit because `st.write` output differs from an actual file download.

- **Examples to reference in edits**:
  - Removing `ln` columns: `modules/data_loader.py: load_data()`
  - Missing value behavior: `modules/preprocessing.py: handle_missing_values()`
  - PCA outlier flow: `Data_prep.py` (standardize -> PCA -> distance -> 95th percentile)

If anything above is unclear or you'd like me to expand sections (for example, adding sample unit tests or converting `modules` into a package), tell me which area to iterate on next.
