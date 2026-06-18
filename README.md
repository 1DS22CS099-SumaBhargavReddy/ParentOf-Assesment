# Fruit Ninja Gameplay Performance Assessment

This repository contains the analysis, metric formulas, processing scripts, and a FastAPI endpoint designed to evaluate children's cognitive performance based on Fruit Ninja gameplay data.

---

## 📋 Table of Contents
1. [Theoretical Framework & Formulas](#-theoretical-framework--formulas)
2. [Data Analysis & Statistical Insights](#-data-analysis--statistical-insights)
3. [Repository Structure](#-repository-structure)
4. [Installation & Setup](#-installation--setup)
5. [How to Run Scripts](#-how-to-run-scripts)
6. [API Usage & Swagger Documentation](#-api-usage--swagger-documentation)
7. [AI Tools Used](#-ai-tools-used)

---

## 🧠 Theoretical Framework & Formulas

To translate raw gameplay metrics into cognitive performance indicators, we designed five normalized rates (scaled to `0 - 100`) and a holistic **Overall Performance Score**. To ensure universal rendering across all markdown viewers, all formulas are presented in plain-text code blocks.

---

### 1. Accuracy Rate (0–100)

```
Accuracy Rate = 100 * fruits_sliced / (fruits_sliced + fruits_missed + bombs_hit)
```

#### 📝 Formula Parameter Guide
*   `fruits_sliced`: Successful hits on valid targets (True Positives).
*   `fruits_missed`: Missed valid targets (False Negatives).
*   `bombs_hit`: Hits on hazardous obstacles (False Positives).

#### 💡 Cognitive Explanation & Justification
*   **Cognitive Dimension**: Precision, Target Selection, and Attention Focus.
*   **Justification**: This is modeled after the **Jaccard Index (Threat Score)**. In reaction-based assessments, a player's accuracy isn't just about how many targets they hit, but how well they avoid mistakes. Slicing a bomb or letting a fruit fall are both errors. This formula evaluates the player's ability to focus attention on valid targets (fruits) while filtering out noise (bombs) and staying responsive.
*   **Boundary Handling**: If a session contains no interactions (`total_target = 0`), the formula safely defaults to `0.0` to avoid division-by-zero errors.

---

### 2. Response Rate (0–100)

```
Action Speed = (fruits_sliced + bombs_dodged) / session_duration_seconds
Speed Score = min(100.0, 100.0 * Action Speed / 2.5)
Combo Score = min(100.0, 100.0 * max_combo / 50.0)

Response Rate = 0.6 * Speed Score + 0.4 * Combo Score
```

#### 📝 Formula Parameter Guide
*   `Action Speed`: The number of correct decisions (slices + dodges) made per second.
*   `Speed Score`: Speed normalized against a high-performance benchmark of `2.5` actions per second.
*   `Combo Score`: Highest streak achieved, normalized against a maximum benchmark of `50`.

#### 💡 Cognitive Explanation & Justification
*   **Cognitive Dimension**: Processing Speed, Motor Reflexes, and Sequence Planning.
*   **Justification**: Speed alone can result in chaotic, error-prone play. By combining **physical response speed** (actions/second, 60% weight) with **coordinated accuracy** (max combo, 40% weight), we measure how *effectively* the child responds. Combos represent the ability to execute sequential responses rapidly without making mistakes.
*   **Boundary Handling**: Normalized values are capped at `100.0` to prevent outliers from distorting the scale. Non-positive durations default to a speed score of `0.0`.

---

### 3. Error Rate (0–100)

```
Weighted Errors = fruits_missed + 3.0 * bombs_hit
Total Objects   = fruits_sliced + fruits_missed + bombs_hit + bombs_dodged

Error Rate = min(100.0, 100.0 * Weighted Errors / Total Objects)
```

#### 📝 Formula Parameter Guide
*   `Weighted Errors`: Sum of mistakes, penalizing severe errors (bomb hits) three times more than standard mistakes (missed fruits).
*   `Total Objects`: The sum of all active gameplay objects spawned during the session.

#### 💡 Cognitive Explanation & Justification
*   **Cognitive Dimension**: Inhibition Control and Risk Avoidance.
*   **Justification**: Hitting a bomb in Fruit Ninja represents a **critical failure of inhibitory control** (failing to stop a motor action in response to a negative stimulus). Letting a fruit drop is a minor lapse in attention. Thus, bomb hits are weighted $3\times$ heavier. We divide this by the total spawned objects to reflect the frequency of errors relative to the total opportunities they had to make them.
*   **Boundary Handling**: Capped at `100.0` to maintain scale integrity. Defaults to `0.0` if no objects are spawned.

---

### 4. Persistence Rate (0–100)

```
Retries Score  = 100.0 * retries / 3.0
Duration Score = 100.0 * session_duration_seconds / 300.0
Pause Penalty  = 20.0 * pause_count / 5.0

Persistence Rate = max(0.0, min(100.0, 0.5 * Retries Score + 0.5 * Duration Score - Pause Penalty))
```

#### 📝 Formula Parameter Guide
*   `retries`: Number of times the player restarted the session (maximum of `3`).
*   `session_duration_seconds`: Total active gameplay duration, scaled against a maximum of `300` seconds (5 minutes).
*   `pause_count`: Number of times the user paused, penalizing the score by up to `20` points.

#### 💡 Cognitive Explanation & Justification
*   **Cognitive Dimension**: Task Engagement, Grit, and Attention Span.
*   **Justification**: Children who retry the game after failing and play for longer sessions demonstrate **higher persistence and intrinsic motivation**. In contrast, frequent pausing suggests a disruption in focus, distraction, or fatigue. Therefore, retries and duration are rewarded (50% weight each), while pauses incur a penalty.
*   **Boundary Handling**: Bounded strictly within `[0.0, 100.0]` using clipping functions.

---

### 5. Consistency Rate (0–100)

```
Combo Consistency = min(100.0, 100.0 * max_combo / fruits_sliced)
Stability Score   = 100.0 - Error Rate
Pause Penalty     = 20.0 * pause_count / 5.0

Consistency Rate = max(0.0, min(100.0, 0.5 * Combo Consistency + 0.5 * Stability Score - Pause Penalty))
```

#### 📝 Formula Parameter Guide
*   `Combo Consistency`: Ratio of the longest streak to total successful slices.
*   `Stability Score`: The inverse of the error rate, representing overall error avoidance.
*   `pause_count`: Pausing frequency, representing a break in flow consistency.

#### 💡 Cognitive Explanation & Justification
*   **Cognitive Dimension**: Sustained Focus and Cognitive Stability.
*   **Justification**: Consistency evaluates the stability of the player's performance. A player who maintains a high combo relative to their total slices is in a **steady flow state**, slicing continuously without interruption. A player who hits bombs or pauses frequently is exhibiting unstable, erratic behavior. 
*   **Boundary Handling**: If `fruits_sliced` is 0, the combo consistency defaults to `0.0`. The final score is clipped between `0` and `100`.

---

### 6. Overall Performance Score (0–100)

```
Overall Score = 0.30 * Accuracy Rate + 0.25 * Response Rate + 0.15 * (100.0 - Error Rate) + 0.15 * Persistence Rate + 0.15 * Consistency Rate
```

#### 💡 Cognitive Explanation & Justification
*   **Justification**: Calculates a single holistic index of the child's gameplay performance. Weighting prioritizes core cognitive indicators: Precision/Attention (Accuracy: 30%) and Speed/Timing (Response: 25%), while giving equal weight (15% each) to error avoidance, persistence, and flow consistency.
*   **Statistical Note**: In practice, a score of `100` represents a theoretical perfect play across all dimensions (0 errors, maximum speed, 3 retries, and no pauses). Due to natural trade-offs (e.g., retrying and playing longer reduces average speed), the maximum empirical score observed in the dataset is `82.26`.

---

## 📊 Data Analysis & Statistical Insights

### Summary Statistics of Calculated Metrics (900 Sessions)

| Metric | Mean | Std Dev | Min | Median | Max |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Accuracy Rate** | 79.94 | 11.95 | 38.96 | 81.92 | 100.00 |
| **Response Rate** | 42.93 | 17.87 | 7.34 | 41.56 | 100.00 |
| **Error Rate** | 26.18 | 14.42 | 0.00 | 23.34 | 80.56 |
| **Persistence Rate** | 43.58 | 22.61 | 0.00 | 43.67 | 99.67 |
| **Consistency Rate** | 41.19 | 11.74 | 0.18 | 40.25 | 89.72 |
| **Overall Performance Score** | **58.51** | **9.05** | **25.84** | **59.59** | **82.26** |

### Key Correlation Matrix Observations

1. **Accuracy vs. Error Rate ($r = -0.92$)**: Strong negative correlation. Accuracy measures hits out of total slices and drops, while Error Rate measures penalty weight out of all spawns. They validate each other as inverse metrics of precision.
2. **Response vs. Persistence ($r = -0.27$)**: A minor negative correlation exists. This represents a natural gameplay trade-off: players who play for a very long duration (increasing persistence) often have slower, more methodical slice rates, lowering their actions/second.
3. **Consistency vs. Others**: Consistency maintains low correlations with raw Accuracy ($r = 0.08$) and Error Rate ($r = -0.13$), showing that consistency captures a unique **flow state** (combo length relative to sliced count) rather than just raw precision.

### Logging Discovery: Max Combo Anomaly
In $23$ of the $900$ sessions, `max_combo` was strictly greater than `fruits_sliced` (e.g., `fruits_sliced = 30`, `max_combo = 50`). This represents a logging quirk where `max_combo` tracks the total streak including multi-hit events or counts across retries, whereas `fruits_sliced` might reflect the final attempt. Our calculation scripts robustly handle this by clipping the `max_combo / fruits_sliced` ratio to `1.0` (100%) to ensure consistency rates remain bounded within $[0, 100]$.

---

## 📂 Repository Structure & Architectural Guide

The codebase is organized into a modular structure that separates raw data processing, REST API endpoints, business logic formulas, and test assertions.

### File Hierarchy and Purpose

```
ParentOf Assessment/
│
├── Copy of Task 1 Dataset.xlsx   # Processed gameplay workbook containing row-by-row calculated metrics.
├── process_data.py               # Batch processor script that applies math logic to the Excel sheet.
├── validate_data.py              # Automated data quality checker for boundary and null-value constraints.
├── pack_submission.py            # Packaging script to compile the workspace into a clean ZIP archive.
├── README.md                     # Comprehensive framework, architectural guide, and usage instructions.
│
├── app/                         # Core API module
│   ├── __init__.py               # Marks the folder as a Python package.
│   ├── calculator.py             # Pure business logic containing raw mathematical formulas and comments.
│   ├── main.py                   # FastAPI routing, endpoints, and middleware initialization.
│   └── schemas.py                # Pydantic V2 schemas for validating API input/output JSON payloads.
│
└── tests/                       # Automated QA module
    ├── __init__.py               # Marks the folder as a Python package.
    ├── test_calculator.py        # Edge-case assertions for the calculator's pure functions.
    └── test_api.py               # Request-response integration tests for the FastAPI web router.
```

---

### 🔗 Inter-File Linkages & Dependency Tree

The diagram below illustrates how components import, depend upon, and interact with each other:

```mermaid
graph TD
    %% Imports & Core Dependents
    subgraph Core Module [app/ Directory]
        CALC[calculator.py]
        SCHEMAS[schemas.py]
        MAIN[main.py]
        MAIN -->|imports| CALC
        MAIN -->|imports| SCHEMAS
    end

    %% Processor Script
    PROC[process_data.py] -->|imports| CALC
    PROC -->|reads/writes| EXCEL[Copy of Task 1 Dataset.xlsx]

    %% Validation Script
    VALID[validate_data.py] -->|inspects & asserts| EXCEL

    %% Testing Framework
    subgraph QA Module [tests/ Directory]
        T_CALC[test_calculator.py] -->|imports & tests| CALC
        T_API[test_api.py] -->|imports & tests Client| MAIN
    end

    %% Packaging script
    PACK[pack_submission.py] -->|zips all workspace files| ZIP[K_Bhargav_Reddy_Assessment.zip]
```

---

### 💡 Architectural Choices & Rationale

1. **Isolation of Business Logic (`app/calculator.py`)**:
   * *Why*: We isolated the mathematical formulas from the data layer (pandas/excel) and the web layer (FastAPI). This makes the formulas **highly reusable** and **easily unit-testable** without mocking external interfaces.
2. **Declarative Validation (`app/schemas.py`)**:
   * *Why*: Instead of manual check-logic inside the endpoints, we used `pydantic` schemas. It enforces structural bounds (e.g. preventing negative values using `ge=0`) and type coerces values at the entrance door, keeping the router code clean.
3. **Decoupled Data Processing (`process_data.py`)**:
   * *Why*: This script is completely separate from the API server. This ensures that batch-processing the offline Excel sheet doesn't block or require running the online API server. It uses `pandas` for reading/writing and `openpyxl` as the spreadsheet engine for in-place updates.
4. **Independent Quality Control (`validate_data.py`)**:
   * *Why*: In data pipelines, validation should run after write operations. By separating this into a dedicated script, we can run data quality checks on the output spreadsheet independently in a CI/CD environment or pre-commit hook.
5. **Separate Testing Modules (`tests/` directory)**:
   * *Why*: Keeps test code and mock clients out of the production runtime build, preventing dependencies like `pytest` and `httpx` from bloating production deployments.
6. **Automation-first Packaging (`pack_submission.py`)**:
   * *Why*: Avoids manual packaging mistakes. Automatically filters out temporary folders (such as `__pycache__`, `.pytest_cache`, `.venv`, and `.git`) to produce a clean, minimal deployment ZIP.

---

## ⚙️ Installation & Setup

Ensure Python 3.8+ is installed.

1. **Clone/extract the files** and navigate to the directory.
2. **Install dependencies**:
   ```bash
   pip install pandas openpyxl fastapi uvicorn pydantic pytest httpx
   ```

---

## 🚀 How to Run Scripts

### 1. Process Gameplay Data
To recalculate metrics and write them back into the columns of the Excel workbook:
```bash
python process_data.py
```

### 2. Generate Performance Visualizations
To generate the four diagnostic charts (distributions, boxplots, heatmaps, and tradeoffs) and place them in the static assets folder:
```bash
python generate_visualizations.py
```

### 3. Verify and Validate Data Integrity
To verify that no NaN values exist in calculated columns and that all rates reside inside $[0, 100]$:
```bash
python validate_data.py
```

### 4. Run Test Suite
To execute the unit tests for formulas and integration tests for FastAPI endpoints:
```bash
python -m pytest tests/
```

### 5. Create ZIP Submission
To compress all assessment files (excluding caches and virtual environments) into `K_Bhargav_Reddy_Assessment.zip`:
```bash
python pack_submission.py
```

---

## 🌐 API Usage & Swagger Documentation

### Start the FastAPI Server
Run the following command to boot the development server:
```bash
python -m uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

### Access the Interactive Dashboard
Open your web browser and go to:
*   **`http://127.0.0.1:8000/dashboard`**

This is an interactive dashboard that contains:
1.  **Analytical Reports**: Renders the generated matplotlib charts (distributions, boxplots, heatmaps, and tradeoffs) in a responsive grid. Click on any chart to enlarge it in a full-screen lightbox.
2.  **Live Formula Simulator**: Enter raw gameplay metrics (such as sliced fruit, missed fruit, duration, and retries), click "Run Formula Pipeline", and see the computed cognitive rates update instantly in a card interface with progress bars and color-coded statuses.

### Access Swagger API Docs
Go to `http://127.0.0.1:8000/docs` in your browser to view the interactive **Swagger UI** or `http://127.0.0.1:8000/redoc` for **ReDoc**.

### Endpoint: POST `/calculate`
* **Request URL**: `http://127.0.0.1:8000/calculate`
* **Sample Request Payload**:
  ```json
  {
    "gameplay_duration_seconds": 147,
    "fruits_sliced": 122,
    "fruits_missed": 25,
    "bombs_hit": 2,
    "bombs_dodged": 12,
    "max_combo": 35,
    "pause_count": 2,
    "retries": 2,
    "overall_score": 1002
  }
  ```
* **Sample JSON Response**:
  ```json
  {
    "accuracy_rate": 81.8792,
    "response_rate": 60.8,
    "error_rate": 19.4969,
    "persistence_rate": 49.5,
    "consistency_rate": 45.419,
    "overall_performance_score": 58.7303
  }
  ```

---

## 🛠️ AI Tools Used

This project was developed with assistance from **Antigravity**, an agentic AI coder developed by Google DeepMind.
* **Assistance Provided**:
  * Structured the modular architecture (`app/`, `tests/` design).
  * Programmed formula logic, Pydantic data schemas, and FastAPI endpoints.
  * Automated dataset processing and wrote test suites to verify math and API reliability.
  * Authored packaging and validation pipelines.
