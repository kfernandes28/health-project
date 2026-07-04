from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import html

BASE_DIR = Path(__file__).resolve().parents[1]

CANONICAL_PATH = BASE_DIR / "Stage 1 - Canonical" / "biomarker_results.csv"
OUT_DIR = BASE_DIR / "Stage 2 - Dashboard"
OUT_PATH = OUT_DIR / "index.html"

INTERVENTIONS_PATH = BASE_DIR / "Stage 0 - Raw" / "interventions.csv"
INTERVENTION_LINKS_PATH = BASE_DIR / "Stage 0 - Raw" / "intervention_biomarker_links.csv"

RANGES_PATH = BASE_DIR / "config" / "biomarker_ranges.csv"

ranges_df = pd.read_csv(RANGES_PATH)

ranges_df["show_as_kpi"] = (
    ranges_df["show_as_kpi"]
    .astype(str)
    .str.upper()
    .eq("TRUE")
)

kpi_biomarkers = set(
    ranges_df.loc[
        ranges_df["show_as_kpi"],
        "biomarker_code"
    ]
)

# Range bands are now plotted as traces instead of layout shapes to stop Plotly dropdown colours switching.
def has_range(pair):
    return (
        pair is not None
        and len(pair) == 2
        and pd.notna(pair[0])
        and pd.notna(pair[1])
    )

def range_bounds(biomarker_range):
    bounds = []

    for key in ["low", "normal", "optimal"]:
        pair = biomarker_range.get(key)

        if has_range(pair):
            bounds.extend(pair)

    return bounds

def get_status(value, biomarker_code):

    biomarker_range = RANGES.get(biomarker_code)

    if biomarker_range is None:
        return "Unknown"

    low = biomarker_range.get("low")
    normal = biomarker_range.get("normal")
    optimal = biomarker_range.get("optimal")

    if has_range(low):
        low_min, low_max = low
        if low_min <= value < low_max:
            return "Low"

    if has_range(normal):
        normal_min, normal_max = normal
        if normal_min <= value < normal_max:
            return "Normal"

    if has_range(optimal):
        optimal_min, optimal_max = optimal
        if optimal_min <= value <= optimal_max:
            return "Optimal"
        if value > optimal_max:
            return "High"

    # If no optimal range is defined, treat values above the normal range as high.
    if has_range(normal):
        _, normal_max = normal
        if value > normal_max:
            return "High"

    return "Unknown"

def format_status(status):
    if status == "Optimal":
        return '<span class="status-optimal">Optimal</span>'
    if status == "Normal":
        return '<span class="status-normal">Normal</span>'
    if status == "Low":
        return '<span class="status-low">Low</span>'
    if status == "High":
        return '<span class="status-high">High</span>'
    return '<span class="status-unknown">Unknown</span>'

def latest_results(df):
    df = df.sort_values(["biomarker_code", "test_date"])

    latest = (
        df.groupby("biomarker_code")
        .tail(1)
        .copy()
    )

    previous = (
        df.groupby("biomarker_code")
        .nth(-2)
        .reset_index()
    )

    previous = previous[
        ["biomarker_code", "value", "test_date"]
    ].rename(
        columns={
            "value": "previous_value",
            "test_date": "previous_test_date",
        }
    )

    latest = latest.merge(
        previous,
        on="biomarker_code",
        how="left"
    )

    latest["change"] = latest["value"] - latest["previous_value"]
    latest["change_pct"] = (latest["change"] / latest["previous_value"]) * 100

    latest = latest.sort_values("biomarker_code")

    return latest

RANGES = {}

def load_interventions():
    if not INTERVENTIONS_PATH.exists() or not INTERVENTION_LINKS_PATH.exists():
        return pd.DataFrame()

    interventions = pd.read_csv(INTERVENTIONS_PATH)
    links = pd.read_csv(INTERVENTION_LINKS_PATH)

    interventions["start_date"] = pd.to_datetime(interventions["start_date"])
    interventions["end_date"] = pd.to_datetime(interventions["end_date"], errors="coerce")

    linked = links.merge(
        interventions,
        on="intervention_id",
        how="left"
    )

    return linked

def make_intervention_shapes_and_annotations(code, interventions):
    shapes = []
    annotations = []

    if interventions.empty:
        return shapes, annotations

    linked_interventions = interventions[
        interventions["biomarker_code"] == code
    ]

    for _, intervention in linked_interventions.iterrows():
        start_date = intervention["start_date"]
        end_date = intervention["end_date"]
        name = intervention["name"]

        shapes.append(
            dict(
                type="line",
                xref="x",
                x0=start_date,
                x1=start_date,
                yref="paper",
                y0=0,
                y1=1,
                line=dict(
                    width=2,
                    dash="dash",
                    color="black",
                ),
            )
        )

        annotations.append(
            dict(
                x=start_date,
                y=1.05,
                xref="x",
                yref="paper",
                text=f"Started: {name}",
                showarrow=False,
                font=dict(size=11),
                align="left",
            )
        )

        if pd.notna(end_date):
            shapes.append(
                dict(
                    type="line",
                    xref="x",
                    x0=end_date,
                    x1=end_date,
                    yref="paper",
                    y0=0,
                    y1=1,
                    line=dict(
                        width=2,
                        dash="dot",
                        color="black",
                    ),
                )
            )

    return shapes, annotations

for _, row in ranges_df.iterrows():
    RANGES[row["biomarker_code"]] = {
        "label": row["label"],
        "unit": row["unit"],
        "category": row["category"],
        "description": row.get("description", ""),
        "low": (row["low_min"], row["low_max"]),
        "normal": (row["normal_min"], row["normal_max"]),
        "optimal": (row["optimal_min"], row["optimal_max"]),
    }

def main():
    df = pd.read_csv(CANONICAL_PATH)
    df["test_date"] = pd.to_datetime(df["test_date"])

    interventions = load_interventions()

    latest = latest_results(df)

    latest["status"] = latest.apply(
        lambda row: get_status(
            row["value"],
            row["biomarker_code"]
        ),
        axis=1
    )

    latest["category"] = latest["biomarker_code"].map(
        lambda code: RANGES.get(code, {}).get("category", "Other")
    )
    latest["description"] = latest["biomarker_code"].map(
        lambda code: RANGES.get(code, {}).get("description", "")
    )

    print("\nLatest biomarker results:")
    print(latest[["biomarker_name", "value", "unit", "test_date", "provider"]])

    fig = go.Figure()

    biomarkers = sorted(df["biomarker_code"].unique())

    df_min_date = df["test_date"].min()
    df_max_date = df["test_date"].max()

    def add_range_band(y0, y1, color, visible):
        fig.add_trace(
            go.Scatter(
                x=[df_min_date, df_max_date, df_max_date, df_min_date],
                y=[y0, y0, y1, y1],
                fill="toself",
                fillcolor=color,
                line=dict(width=0),
                mode="none",
                hoverinfo="skip",
                showlegend=False,
                visible=visible,
            )
        )

    trace_groups = {}

    for i, code in enumerate(biomarkers):
        biomarker_range = RANGES.get(code, {})
        visible = i == 0
        trace_groups[code] = []

        # low band
        if has_range(biomarker_range.get("low")):
            add_range_band(
                biomarker_range["low"][0],
                biomarker_range["low"][1],
                "rgba(240, 128, 128, 0.2)",
                visible,
            )
            trace_groups[code].append(len(fig.data) - 1)

        # normal band
        if has_range(biomarker_range.get("normal")):
            add_range_band(
                biomarker_range["normal"][0],
                biomarker_range["normal"][1],
                "rgba(240, 230, 140, 0.25)",
                visible,
            )
            trace_groups[code].append(len(fig.data) - 1)

        # optimal band
        if has_range(biomarker_range.get("optimal")):
            add_range_band(
                biomarker_range["optimal"][0],
                biomarker_range["optimal"][1],
                "rgba(144, 238, 144, 0.3)",
                visible,
            )
            trace_groups[code].append(len(fig.data) - 1)

        sub = df[df["biomarker_code"] == code]

        fig.add_trace(
            go.Scatter(
                x=sub["test_date"],
                y=sub["value"],
                mode="lines+markers+text",
                text=sub["value"],
                textposition="top center",
                name=RANGES.get(code, {}).get("label", code),
                customdata=sub[["provider", "unit"]],
                hovertemplate=(
                    "Date: %{x|%Y-%m-%d}<br>"
                    "Value: %{y}<br>"
                    "Provider: %{customdata[0]}<br>"
                    "Unit: %{customdata[1]}<extra></extra>"
                ),
                visible=visible,
            )
        )
        trace_groups[code].append(len(fig.data) - 1)

    buttons = []

    for i, code in enumerate(biomarkers):
        visibility = [False] * len(fig.data)

        for trace_index in trace_groups[code]:
            visibility[trace_index] = True

        biomarker_range = RANGES.get(code, {})
        sub_values = df.loc[df["biomarker_code"] == code, "value"]

        y_values = [sub_values.min(), sub_values.max()] + range_bounds(biomarker_range)
        y_min = min(y_values)
        y_max = max(y_values)

        padding = (y_max - y_min) * 0.10

        if padding == 0:
            padding = max(abs(y_max) * 0.10, 1)

        y_axis_range = [y_min - padding, y_max + padding]

        # Range bands are now normal traces, not layout shapes.
        # Intervention lines stay as layout shapes because they are simple vertical markers.
        shapes, annotations = make_intervention_shapes_and_annotations(code, interventions)

        label = biomarker_range.get("label", code)

        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {"visible": visibility},
                    {
                        #"title": f"{label} Over Time",
                        "shapes": list(shapes),
                        "annotations": list(annotations),
                        "yaxis.title.text": biomarker_range.get("unit", "Value"),
                        "yaxis.range": y_axis_range,
                    },
                ],
            )
        )

    first_code = biomarkers[0]
    first_range = RANGES.get(first_code, {})

    first_values = df.loc[df["biomarker_code"] == first_code, "value"]

    first_y_values = [first_values.min(), first_values.max()] + range_bounds(first_range)
    first_y_min = min(first_y_values)
    first_y_max = max(first_y_values)
    first_padding = (first_y_max - first_y_min) * 0.10

    if first_padding == 0:
        first_padding = max(abs(first_y_max) * 0.10, 1)

    first_y_axis_range = [first_y_min - first_padding, first_y_max + first_padding]

    initial_shapes, initial_annotations = make_intervention_shapes_and_annotations(
        first_code,
        interventions
    )

    fig.update_layout(
        #title=f"{first_range.get('label', first_code)} Over Time",
        template="plotly_white",
        xaxis_title="Date",
        shapes=initial_shapes,
        annotations=initial_annotations,
        yaxis=dict(
            title=first_range.get("unit", "Value"),
            range=first_y_axis_range,
        ),
        updatemenus=[
            dict(
                active=0,
                buttons=buttons,
                x=0.01,
                y=1.15,
                xanchor="left",
                yanchor="top",
            )
        ],
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")

    cards_html = ""

    for _, row in latest.iterrows():
            if row["biomarker_code"] not in kpi_biomarkers:
                continue
            cards_html += f"""
            <div class="card">
                <div class="card-label">{row['biomarker_name']}</div>
                <div class="card-value">{row['value']} {row['unit']}</div>
                <div class="card-subtitle">{row['test_date'].date()} · {row['provider']}</div>
            </div>
            """
    table_view = latest[
        [
            "category",
            "biomarker_name",
            "value",
            "unit",
            "description",
            "previous_value",
            "change",
            "status",
            "change_pct",
            "test_date",
            "provider",
        ]
    ].copy()

    def format_change(row):
        if pd.isna(row["change"]):
            return "-"
        if pd.isna(row["previous_value"]):
            return '<span class="change-neutral">-</span>'

        arrow = "Up" if row["change"] > 0 else ("Down" if row["change"] < 0 else "Same")
        sign = "+" if row["change"] > 0 else ""

        if row["change"] > 0:
            return (
                f'<span class="change-up">'
                f'+ {row["change"]:.2f} (+{row["change_pct"]:.1f}%)'
                f'</span>'
            )

        elif row["change"] < 0:
            return (
                f'<span class="change-down">'
                f'{row["change"]:.2f} ({row["change_pct"]:.1f}%)'
                f'</span>'
            )

        return '<span class="change-neutral">0.00 (0%)</span>'
    
    table_view["previous_value"] = (
        table_view["previous_value"]
        .fillna("-")
    )

    table_view["change"] = table_view.apply(format_change, axis=1)

    table_view["status"] = table_view["status"].apply(format_status)

    def format_biomarker(row):
        description = row["description"]

        if pd.isna(description) or str(description).strip() == "":
            return row["biomarker_name"]

        description = str(description).strip()

        # handle double-escaped and normal escaped newlines
        description = description.replace("\\\\n", "\n")
        description = description.replace("\\n", "\n")

        lines = description.splitlines()
        description_html = "<br>".join(lines)

        biomarker_name = str(row["biomarker_name"]).strip()

        return (
            f'<span class="biomarker-name">'
            f'{biomarker_name}'
            f'<span class="info-icon">i</span>'
            f'<span class="tooltip-text">{description_html}</span>'
            f'</span>'
        )
        
    table_view["biomarker_name"] = table_view.apply(format_biomarker, axis=1)

    table_view = table_view[
        [
            "category",
            "biomarker_name",
            "value",
            "unit",
            "previous_value",
            "change",
            "status",
            "test_date",
            "provider",
        ]
    ]

    table_view = table_view.rename(
        columns={
            "category": "Category",
            "biomarker_name": "Biomarker",
            "value": "Latest",
            "unit": "Unit",
            "previous_value": "Previous",
            "change": "Change",
            "status": "Status",
            "test_date": "Last tested",
            "provider": "Provider",
        }
    )

    table_html = ""

    for category, group in table_view.groupby("Category", sort=False):
        group_html = group.drop(columns=["Category"]).to_html(
            index=False,
            classes="results-table",
            escape=False
        )

        table_html += f"""
        <details open class="category-section">
            <summary>{category} ({len(group)})</summary>
            {group_html}
        </details>
        """

    page_html = f"""
    <html>
    <head>
        <title>Life OS Health Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 24px;
                background: #f7f7f7;
            }}

            h1 {{
                margin-bottom: 20px;
            }}

            .cards {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 16px;
                margin-bottom: 24px;
            }}

            .card {{
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 14px;
                padding: 18px;
            }}

            .card-label {{
                color: #666;
                font-size: 13px;
                font-weight: bold;
            }}

            .card-value {{
                font-size: 26px;
                font-weight: bold;
                margin-top: 8px;
            }}

            .card-subtitle {{
                color: #777;
                font-size: 12px;
                margin-top: 8px;
            }}

            .panel {{
                background: white;
                border: 1px solid #e5e5e5;
                border-radius: 14px;
                padding: 16px;
            }}
            .results-table {{
                width: 100%;
                border-collapse: collapse;
            }}

            .results-table th {{
                text-align: left;
                color: #666;
                font-size: 13px;
                border-bottom: 1px solid #ddd;
                padding: 10px;
            }}

            .results-table td {{
                padding: 10px;
                border-bottom: 1px solid #eee;
            }}
            .change-up {{
                color: #16a34a;
                font-weight: 600;
            }}

            .change-down {{
                color: #dc2626;
                font-weight: 600;
            }}

            .change-neutral {{
                color: #666;
                font-weight: 600;
            }}
            .status-optimal {{
                color: #16a34a;
                font-weight: 600;
            }}

            .status-normal {{
                color: #2563eb;
                font-weight: 600;
            }}

            .status-low {{
                color: #d97706;
                font-weight: 600;
            }}

            .status-high {{
                color: #dc2626;
                font-weight: 600;
            }}

            .status-unknown {{
                color: #666;
                font-weight: 600;
            }}

            .category-section {{
                margin-bottom: 18px;
            }}

            .category-section summary {{
                cursor: pointer;
                font-size: 18px;
                font-weight: bold;
                padding: 12px 0;
                color: #222;
            }}
            .biomarker-name {{
                position: relative;
                display: inline-block;
                font-weight: normal;
            }}

            .info-icon {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 15px;
                height: 15px;
                margin-left: 6px;
                border-radius: 50%;
                background: #e5e7eb;
                color: #555;
                font-size: 11px;
                font-weight: bold;
                cursor: help;
            }}

            .tooltip-text {{
                visibility: hidden;
                width: 340px;
                background: #222;
                color: white;
                text-align: left;
                border-radius: 8px;
                padding: 12px;
                position: absolute;
                z-index: 20;
                left: 0;
                top: 24px;
                font-size: 13px;
                line-height: 1.45;
                white-space: normal;
                font-weight: normal;
            }}

            .biomarker-name:hover .tooltip-text {{
                visibility: visible;
            }}
        </style>
    </head>

    <body>
        <h1>Life OS Health Dashboard</h1>

        <div class="cards">
            {cards_html}
        </div>

        <div class="panel">
            {chart_html}
        </div>
        <div class="panel">
            <h2>Latest Results</h2>
            {table_html}
        </div>
    </body>
    </html>
    """

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(page_html)

    print(f"Read: {CANONICAL_PATH}")
    print(f"Wrote: {OUT_PATH}")

if __name__ == "__main__":
    main()