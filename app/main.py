from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import pandas as pd

from app.calculator import (
    calculate_accuracy_rate,
    calculate_response_rate,
    calculate_error_rate,
    calculate_persistence_rate,
    calculate_consistency_rate,
    calculate_overall_performance_score,
)
from app.schemas import GameplayMetrics, DerivedRatesResponse

app = FastAPI(
    title="Fruit Ninja Cognitive Performance Calculator API",
    description=(
        "API for calculating derived performance rates and Overall Performance Scores "
        "from Fruit Ninja gameplay metrics. Used for evaluating children's cognitive performance."
    ),
    version="1.0.0",
)

# Mount the static directory to serve plots
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Welcome to the Fruit Ninja Cognitive Performance Calculator API",
        "documentation": "/docs",
        "dashboard": "/dashboard",
        "status": "healthy",
    }


@app.post(
    "/calculate",
    response_model=DerivedRatesResponse,
    tags=["Calculations"],
    summary="Calculate derived cognitive rates",
)
async def calculate_metrics(metrics: GameplayMetrics):
    # Perform core calculations using our shared formulas
    accuracy = calculate_accuracy_rate(
        fruits_sliced=metrics.fruits_sliced,
        fruits_missed=metrics.fruits_missed,
        bombs_hit=metrics.bombs_hit,
    )

    response = calculate_response_rate(
        fruits_sliced=metrics.fruits_sliced,
        bombs_dodged=metrics.bombs_dodged,
        max_combo=metrics.max_combo,
        session_duration_seconds=metrics.session_duration_seconds,
    )

    error = calculate_error_rate(
        fruits_sliced=metrics.fruits_sliced,
        fruits_missed=metrics.fruits_missed,
        bombs_hit=metrics.bombs_hit,
        bombs_dodged=metrics.bombs_dodged,
    )

    persistence = calculate_persistence_rate(
        retries=metrics.retries,
        session_duration_seconds=metrics.session_duration_seconds,
        pause_count=metrics.pause_count,
    )

    consistency = calculate_consistency_rate(
        max_combo=metrics.max_combo,
        fruits_sliced=metrics.fruits_sliced,
        error_rate=error,
        pause_count=metrics.pause_count,
    )

    overall = calculate_overall_performance_score(
        accuracy_rate=accuracy,
        response_rate=response,
        error_rate=error,
        persistence_rate=persistence,
        consistency_rate=consistency,
    )

    return DerivedRatesResponse(
        accuracy_rate=accuracy,
        response_rate=response,
        error_rate=error,
        persistence_rate=persistence,
        consistency_rate=consistency,
        overall_performance_score=overall,
    )


@app.get("/dashboard", response_class=HTMLResponse, tags=["General"])
async def get_dashboard():
    # Read the Excel file to calculate dynamic KPIs for the entire dataset
    excel_path = "Copy of Task 1 Dataset.xlsx"
    kpis = {
        "accuracy_mean": 79.94, "accuracy_min": 38.96, "accuracy_max": 100.0,
        "response_mean": 42.93, "response_min": 7.34, "response_max": 100.0,
        "error_mean": 26.18, "error_min": 0.0, "error_max": 80.56,
        "persistence_mean": 43.58, "persistence_min": 0.0, "persistence_max": 99.67,
        "consistency_mean": 41.19, "consistency_min": 0.18, "consistency_max": 89.72,
        "overall_mean": 58.51, "overall_min": 25.84, "overall_max": 82.26
    }
    
    if os.path.exists(excel_path):
        try:
            df = pd.read_excel(excel_path)
            # Fetch dynamically calculated summary metrics from the updated Excel
            kpis["accuracy_mean"] = float(df["Accuracy Rate"].mean())
            kpis["accuracy_min"] = float(df["Accuracy Rate"].min())
            kpis["accuracy_max"] = float(df["Accuracy Rate"].max())
            
            kpis["response_mean"] = float(df["Response Rate"].mean())
            kpis["response_min"] = float(df["Response Rate"].min())
            kpis["response_max"] = float(df["Response Rate"].max())
            
            kpis["error_mean"] = float(df["Error Rate"].mean())
            kpis["error_min"] = float(df["Error Rate"].min())
            kpis["error_max"] = float(df["Error Rate"].max())
            
            kpis["persistence_mean"] = float(df["Persistence Rate"].mean())
            kpis["persistence_min"] = float(df["Persistence Rate"].min())
            kpis["persistence_max"] = float(df["Persistence Rate"].max())
            
            kpis["consistency_mean"] = float(df["Consistency Rate"].mean())
            kpis["consistency_min"] = float(df["Consistency Rate"].min())
            kpis["consistency_max"] = float(df["Consistency Rate"].max())
            
            kpis["overall_mean"] = float(df["Overall Performance Score"].mean())
            kpis["overall_min"] = float(df["Overall Performance Score"].min())
            kpis["overall_max"] = float(df["Overall Performance Score"].max())
        except Exception as e:
            # Fallback to hardcoded pre-computed stats if sheet is locked or empty
            print(f"Error reading Excel for dynamic KPIs: {e}")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Fruit Ninja Cognitive Performance Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-primary: #0d1117;
                --bg-secondary: #161b22;
                --border-color: #30363d;
                --text-primary: #c9d1d9;
                --text-secondary: #8b949e;
                --accent-blue: #58a6ff;
                --accent-green: #3fb950;
                --accent-red: #f85149;
                --accent-orange: #f0883e;
                --accent-purple: #d2a8ff;
            }}

            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                font-family: 'Inter', sans-serif;
                background-color: var(--bg-primary);
                color: var(--text-primary);
                line-height: 1.6;
                padding: 2rem;
            }}

            header {{
                max-width: 1400px;
                margin: 0 auto 1.5rem auto;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 1.5rem;
            }}

            h1 {{
                font-size: 2.2rem;
                font-weight: 700;
                color: #f0f6fc;
                margin-bottom: 0.5rem;
            }}

            .subtitle {{
                color: var(--text-secondary);
                font-size: 1.1rem;
            }}

            /* KPI Summary Section */
            .kpi-section {{
                max-width: 1400px;
                margin: 0 auto 2rem auto;
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }}

            @media (min-width: 768px) {{
                .kpi-section {{
                    grid-template-columns: repeat(3, 1fr);
                }}
            }}

            @media (min-width: 1200px) {{
                .kpi-section {{
                    grid-template-columns: repeat(6, 1fr);
                }}
            }}

            .kpi-card {{
                background-color: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: center;
                transition: border-color 0.2s;
            }}

            .kpi-card:hover {{
                border-color: var(--text-secondary);
            }}

            .kpi-label {{
                font-size: 0.75rem;
                font-weight: 600;
                color: var(--text-secondary);
                text-transform: uppercase;
                margin-bottom: 0.5rem;
                letter-spacing: 0.05em;
            }}

            .kpi-value {{
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 0.25rem;
            }}

            .kpi-range {{
                font-size: 0.7rem;
                color: var(--text-secondary);
            }}

            /* Layout Grid */
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 1fr;
                gap: 2rem;
            }}

            @media (min-width: 1024px) {{
                .container {{
                    grid-template-columns: 450px 1fr;
                }}
            }}

            .card {{
                background-color: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1.8rem;
                height: fit-content;
            }}

            .card-title {{
                font-size: 1.25rem;
                font-weight: 600;
                color: #f0f6fc;
                margin-bottom: 1.5rem;
                border-bottom: 1px solid var(--border-color);
                padding-bottom: 0.75rem;
            }}

            .form-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }}

            .form-group {{
                margin-bottom: 1.2rem;
            }}

            .form-group.full-width {{
                grid-column: span 2;
            }}

            label {{
                display: block;
                font-size: 0.85rem;
                color: var(--text-secondary);
                margin-bottom: 0.4rem;
                font-weight: 500;
            }}

            input {{
                width: 100%;
                background-color: var(--bg-primary);
                border: 1px solid var(--border-color);
                color: var(--text-primary);
                padding: 0.6rem 0.8rem;
                border-radius: 6px;
                font-size: 0.95rem;
                transition: border-color 0.2s;
            }}

            input:focus {{
                outline: none;
                border-color: var(--accent-blue);
            }}

            button {{
                width: 100%;
                background-color: var(--accent-blue);
                color: #ffffff;
                border: none;
                padding: 0.8rem 1.5rem;
                border-radius: 6px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: opacity 0.2s;
                margin-top: 1rem;
            }}

            button:hover {{
                opacity: 0.9;
            }}

            .results-section {{
                margin-top: 2rem;
                padding-top: 1.5rem;
                border-top: 1px dashed var(--border-color);
                display: none;
            }}

            .overall-score-card {{
                background: linear-gradient(135deg, #1f2937, #111827);
                border: 1px solid var(--accent-blue);
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                margin-bottom: 1.5rem;
            }}

            .overall-score-value {{
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--accent-blue);
            }}

            .metric-bar-group {{
                margin-bottom: 1rem;
            }}

            .metric-info {{
                display: flex;
                justify-content: space-between;
                font-size: 0.85rem;
                margin-bottom: 0.3rem;
            }}

            .progress-bg {{
                background-color: var(--bg-primary);
                height: 10px;
                border-radius: 5px;
                overflow: hidden;
            }}

            .progress-fill {{
                height: 100%;
                width: 0%;
                border-radius: 5px;
                transition: width 0.6s ease-out;
            }}

            .plots-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }}

            @media (min-width: 768px) {{
                .plots-grid {{
                    grid-template-columns: 1fr 1fr;
                }}
            }}

            .plot-container {{
                background-color: var(--bg-secondary);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                cursor: pointer;
                transition: transform 0.2s, border-color 0.2s;
            }}

            .plot-container:hover {{
                transform: scale(1.02);
                border-color: var(--accent-blue);
            }}

            .plot-container img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
            }}

            .plot-title {{
                font-size: 0.95rem;
                font-weight: 600;
                margin-top: 0.75rem;
                color: var(--text-primary);
            }}

            /* Lightbox modal styling */
            .modal {{
                display: none;
                position: fixed;
                z-index: 1000;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(13, 17, 23, 0.95);
                justify-content: center;
                align-items: center;
                padding: 2rem;
            }}

            .modal-content {{
                max-width: 90%;
                max-height: 90%;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                border: 1px solid var(--border-color);
            }}

            .modal-close {{
                position: absolute;
                top: 20px;
                right: 30px;
                color: var(--text-primary);
                font-size: 2rem;
                font-weight: bold;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Fruit Ninja Performance Dashboard</h1>
            <p class="subtitle">Cognitive Metrics Simulator & Gameplay Data Visualization</p>
        </header>

        <!-- Dynamic KPI summary boxes -->
        <div class="kpi-section">
            <div class="kpi-card" style="border-top: 3px solid var(--accent-blue);">
                <div class="kpi-label">Avg Accuracy</div>
                <div class="kpi-value" style="color: var(--accent-blue);">{kpis['accuracy_mean']:.2f}%</div>
                <div class="kpi-range">Range: {kpis['accuracy_min']:.1f}% - {kpis['accuracy_max']:.1f}%</div>
            </div>
            
            <div class="kpi-card" style="border-top: 3px solid var(--accent-green);">
                <div class="kpi-label">Avg Response</div>
                <div class="kpi-value" style="color: var(--accent-green);">{kpis['response_mean']:.2f}%</div>
                <div class="kpi-range">Range: {kpis['response_min']:.1f}% - {kpis['response_max']:.1f}%</div>
            </div>
            
            <div class="kpi-card" style="border-top: 3px solid var(--accent-red);">
                <div class="kpi-label">Avg Error Rate</div>
                <div class="kpi-value" style="color: var(--accent-red);">{kpis['error_mean']:.2f}%</div>
                <div class="kpi-range">Range: {kpis['error_min']:.1f}% - {kpis['error_max']:.1f}%</div>
            </div>
            
            <div class="kpi-card" style="border-top: 3px solid var(--accent-orange);">
                <div class="kpi-label">Avg Persistence</div>
                <div class="kpi-value" style="color: var(--accent-orange);">{kpis['persistence_mean']:.2f}%</div>
                <div class="kpi-range">Range: {kpis['persistence_min']:.1f}% - {kpis['persistence_max']:.1f}%</div>
            </div>
            
            <div class="kpi-card" style="border-top: 3px solid var(--accent-purple);">
                <div class="kpi-label">Avg Consistency</div>
                <div class="kpi-value" style="color: var(--accent-purple);">{kpis['consistency_mean']:.2f}%</div>
                <div class="kpi-range">Range: {kpis['consistency_min']:.1f}% - {kpis['consistency_max']:.1f}%</div>
            </div>
            
            <div class="kpi-card" style="border-top: 3px solid #ff79c6;">
                <div class="kpi-label">Avg Overall Score</div>
                <div class="kpi-value" style="color: #ff79c6;">{kpis['overall_mean']:.2f}</div>
                <div class="kpi-range">Range: {kpis['overall_min']:.1f} - {kpis['overall_max']:.1f}</div>
            </div>
        </div>

        <div class="container">
            <!-- Left Column: Simulator -->
            <div class="card">
                <h2 class="card-title">Formula Simulator</h2>
                <form id="simulator-form" onsubmit="event.preventDefault(); calculateRates();">
                    <div class="form-grid">
                        <div class="form-group full-width">
                            <label for="gameplay_duration_seconds">Gameplay Duration (Seconds)</label>
                            <input type="number" id="gameplay_duration_seconds" value="147" min="1" required>
                        </div>
                        <div class="form-group">
                            <label for="fruits_sliced">Fruits Sliced</label>
                            <input type="number" id="fruits_sliced" value="122" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="fruits_missed">Fruits Missed</label>
                            <input type="number" id="fruits_missed" value="25" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="bombs_hit">Bombs Hit</label>
                            <input type="number" id="bombs_hit" value="2" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="bombs_dodged">Bombs Dodged</label>
                            <input type="number" id="bombs_dodged" value="12" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="max_combo">Max Combo</label>
                            <input type="number" id="max_combo" value="35" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="pause_count">Pause Count</label>
                            <input type="number" id="pause_count" value="2" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="retries">Retries</label>
                            <input type="number" id="retries" value="2" min="0" required>
                        </div>
                        <div class="form-group">
                            <label for="overall_score">Raw Score</label>
                            <input type="number" id="overall_score" value="1002" min="0" required>
                        </div>
                    </div>
                    <button type="submit">Run Formula Pipeline</button>
                </form>

                <!-- Results Display -->
                <div class="results-section" id="results-box">
                    <div class="overall-score-card">
                        <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.2rem;">OVERALL PERFORMANCE SCORE</div>
                        <div class="overall-score-value" id="res-overall">0.0</div>
                    </div>

                    <div class="metric-bar-group">
                        <div class="metric-info">
                            <span>Accuracy Rate</span>
                            <span id="txt-accuracy">0.0%</span>
                        </div>
                        <div class="progress-bg">
                            <div class="progress-fill" id="fill-accuracy" style="background-color: var(--accent-blue);"></div>
                        </div>
                    </div>

                    <div class="metric-bar-group">
                        <div class="metric-info">
                            <span>Response Rate</span>
                            <span id="txt-response">0.0%</span>
                        </div>
                        <div class="progress-bg">
                            <div class="progress-fill" id="fill-response" style="background-color: var(--accent-green);"></div>
                        </div>
                    </div>

                    <div class="metric-bar-group">
                        <div class="metric-info">
                            <span>Error Rate (Lower is Better)</span>
                            <span id="txt-error">0.0%</span>
                        </div>
                        <div class="progress-bg">
                            <div class="progress-fill" id="fill-error" style="background-color: var(--accent-red);"></div>
                        </div>
                    </div>

                    <div class="metric-bar-group">
                        <div class="metric-info">
                            <span>Persistence Rate</span>
                            <span id="txt-persistence">0.0%</span>
                        </div>
                        <div class="progress-bg">
                            <div class="progress-fill" id="fill-persistence" style="background-color: var(--accent-orange);"></div>
                        </div>
                    </div>

                    <div class="metric-bar-group">
                        <div class="metric-info">
                            <span>Consistency Rate</span>
                            <span id="txt-consistency">0.0%</span>
                        </div>
                        <div class="progress-bg">
                            <div class="progress-fill" id="fill-consistency" style="background-color: var(--accent-purple);"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Visualizations -->
            <div>
                <div class="plots-grid">
                    <div class="plot-container" onclick="openModal('/static/plots/rate_distributions.png')">
                        <img src="/static/plots/rate_distributions.png" alt="Rate Distributions" onerror="this.onerror=null; this.src='https://placehold.co/600x400/161b22/8b949e?text=Run+generate_visualizations.py+first';">
                        <div class="plot-title">Rate Distributions (900 sessions)</div>
                    </div>
                    <div class="plot-container" onclick="openModal('/static/plots/correlation_matrix.png')">
                        <img src="/static/plots/correlation_matrix.png" alt="Correlation Matrix" onerror="this.onerror=null; this.src='https://placehold.co/600x400/161b22/8b949e?text=Run+generate_visualizations.py+first';">
                        <div class="plot-title">Cognitive Metrics Correlation Heatmap</div>
                    </div>
                    <div class="plot-container" onclick="openModal('/static/plots/performance_boxplots.png')">
                        <img src="/static/plots/performance_boxplots.png" alt="Performance Boxplots" onerror="this.onerror=null; this.src='https://placehold.co/600x400/161b22/8b949e?text=Run+generate_visualizations.py+first';">
                        <div class="plot-title">Quartile Performance Comparison</div>
                    </div>
                    <div class="plot-container" onclick="openModal('/static/plots/tradeoff_scatter.png')">
                        <img src="/static/plots/tradeoff_scatter.png" alt="Tradeoff Scatter" onerror="this.onerror=null; this.src='https://placehold.co/600x400/161b22/8b949e?text=Run+generate_visualizations.py+first';">
                        <div class="plot-title">Response vs. Persistence Trade-off</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Lightbox Modal -->
        <div id="imageModal" class="modal" onclick="closeModal()">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <img class="modal-content" id="modalImg">
        </div>

        <script>
            async function calculateRates() {{
                const payload = {{
                    gameplay_duration_seconds: parseInt(document.getElementById('gameplay_duration_seconds').value),
                    fruits_sliced: parseInt(document.getElementById('fruits_sliced').value),
                    fruits_missed: parseInt(document.getElementById('fruits_missed').value),
                    bombs_hit: parseInt(document.getElementById('bombs_hit').value),
                    bombs_dodged: parseInt(document.getElementById('bombs_dodged').value),
                    max_combo: parseInt(document.getElementById('max_combo').value),
                    pause_count: parseInt(document.getElementById('pause_count').value),
                    retries: parseInt(document.getElementById('retries').value),
                    overall_score: parseInt(document.getElementById('overall_score').value)
                }};

                try {{
                    const response = await fetch('/calculate', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});

                    if (!response.ok) {{
                        alert('API Error: ' + response.statusText);
                        return;
                    }}

                    const data = await response.json();

                    // Display results box
                    document.getElementById('results-box').style.display = 'block';

                    // Set scores
                    document.getElementById('res-overall').innerText = data.overall_performance_score.toFixed(2);
                    
                    document.getElementById('txt-accuracy').innerText = data.accuracy_rate.toFixed(2) + '%';
                    document.getElementById('fill-accuracy').style.width = data.accuracy_rate + '%';
                    
                    document.getElementById('txt-response').innerText = data.response_rate.toFixed(2) + '%';
                    document.getElementById('fill-response').style.width = data.response_rate + '%';
                    
                    document.getElementById('txt-error').innerText = data.error_rate.toFixed(2) + '%';
                    document.getElementById('fill-error').style.width = data.error_rate + '%';
                    
                    document.getElementById('txt-persistence').innerText = data.persistence_rate.toFixed(2) + '%';
                    document.getElementById('fill-persistence').style.width = data.persistence_rate + '%';
                    
                    document.getElementById('txt-consistency').innerText = data.consistency_rate.toFixed(2) + '%';
                    document.getElementById('fill-consistency').style.width = data.consistency_rate + '%';

                }} catch (err) {{
                    alert('Request failed: ' + err.message);
                }}
            }}

            function openModal(imgSrc) {{
                document.getElementById('imageModal').style.display = 'flex';
                document.getElementById('modalImg').src = imgSrc;
            }}

            function closeModal() {{
                document.getElementById('imageModal').style.display = 'none';
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
