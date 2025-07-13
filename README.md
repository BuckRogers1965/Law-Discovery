# Law-Discovery

An AI-Assisted Discovery Engine for Discovering Fundamental Physical Laws


This project is a web-based, interactive tool that demonstrates the power of dimensional analysis (via the Buckingham Pi theorem) to discover physical formulas. It is built on the principle that many complex physical laws are projections of simpler, dimensionless relationships between quantities.  This is a cross between n-dimensional tetris and unit system sudoku. 

This engine is not just a calculator; it's a research assistant. If a proposed relationship between quantities is incomplete, it uses a heuristic AI to **suggest missing physical constants** and can **auto-search** for a valid formula by recursively testing its own suggestions.

**[Live Demo Link Here After You Deploy]**

## Features

-   **Intuitive Interface:** Enter an output quantity and its inputs to discover the relationship.
-   **Intelligent Auto-Search:** Automatically adds necessary physical constants (like `c`, `h`, `G`, `k_B`) to find a valid formula.
-   **Rich Diagnostics:** Provides clear, actionable error messages if a formula is dimensionally inconsistent or underdetermined.
-   **Physical Validation:** Discovered formulas are checked for reasonableness (e.g., flagging unusually large exponents) and given a confidence score.
-   **Client-Side Power:** Runs a full Python scientific stack (SymPy) directly in your browser using **Pyodide**. No server backend required.
-   **Extensive Library:** Comes with a built-in library of dozens of physical quantities and constants.

## How It Works

The engine implements the **Buckingham Pi theorem**. It constructs a dimensional matrix from the user-provided quantities and solves the resulting system of linear equations to find the exponents that make the relationship dimensionless.

The "AI" component comes from its ability to diagnose a failed system and intelligently suggest which constants are most likely to resolve the dimensional inconsistency or underdetermination, then recursively re-running the analysis.

## Technology Stack

-   **Python Engine:** The core logic is a powerful Python script using the `SymPy` library for symbolic mathematics.
-   **In-Browser Execution:** **Pyodide** is used to run the entire Python stack and `SymPy` within the user's web browser.
-   **User Interface:** Built with standard HTML, CSS, and vanilla JavaScript.

## How to Deploy Your Own

This project is designed to be easily deployed for free on **GitHub Pages**.

1.  **Create a new repository** on GitHub.
2.  **Upload the files:**
    -   `index.html`
    -   `style.css`
    -   `main.js`
    -   `law_discovery.py`
3.  **Enable GitHub Pages:**
    -   In your repository, go to `Settings` -> `Pages`.
    -   Under "Build and deployment," select the source as `Deploy from a branch`.
    -   Choose the `main` (or `master`) branch and the `/ (root)` folder.
    -   Click `Save`.
4.  **Done!** Your site will be live at `https://your-username.github.io/your-repo-name/` in a few minutes.
