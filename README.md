# Law-Discovery

This is an interactive web application that demonstrates the principle that physical laws are coordinate-dependent projections of simpler combinations of dimensionals inputs, outputs and suggested constants.

Live demo: [https://buckrogers1965.github.io/Law-Discovery/](https://buckrogers1965.github.io/Law-Discovery/)


## The Theory

This tool is a practical implementation of the ideas described in ["The Structure of Physical Law as a Grothendieck Fibration"](https://mystry-geek.blogspot.com/2025/06/the-structure-of-physical-law-as.html), ["The Knowledge Pattern"](https://mystry-geek.blogspot.com/2025/07/the-knowledge-pattern-computational.html) and ["The Uniformity Principle."](https://mystry-geek.blogspot.com/2025/07/the-uniformity-principle-how-consistent.html) It posits that "fundamental constants" like `c`, `G`, and `h` are not properties of reality, but artifacts of our arbitrary, human-centric measurement systems (SI units).  This is all based on work done in the project [Physics-Unit-Coordinate-System](https://github.com/BuckRogers1965/Physics-Unit-Coordinate-System).

The real laws of nature are simple proportionalities (e.g., `Energy ~ Mass`). This engine performs the basis transformation from that simple reality to the complex, constant-laden equations we see in textbooks.

This project is a web-based, interactive tool that demonstrates the power of dimensional analysis (via a combination of linear algebra to determine required powers and pattern matching suggestions that fit dimensional holes in the equations) to discover physical formulas. It is built on the principle that many complex physical laws are projections of simpler, dimensionless relationships between quantities.  This is a cross between n-dimensional tetris and unit system sudoku. 

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
