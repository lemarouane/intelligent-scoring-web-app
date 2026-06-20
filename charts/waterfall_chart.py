import plotly.graph_objects as go
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY


def waterfall_chart(rows: list, final_score: float) -> go.Figure:
    x_vals   = [r["label"] for r in rows] + ["Score Final"]
    y_vals   = [r["weighted"] for r in rows] + [None]
    measures = ["relative"] * len(rows) + ["total"]

    fig = go.Figure(go.Waterfall(
        name="Score",
        orientation="v",
        measure=measures,
        x=x_vals,
        y=y_vals,
        textposition="outside",
        text=[f"+{r['weighted']:.2f}" for r in rows] + [f"{final_score:.2f}"],
        textfont=dict(size=9, color="#1E293B"),
        connector=dict(line=dict(color="#CBD5E1", width=1)),
        increasing=dict(marker=dict(color=COLOR_PRIMARY)),
        decreasing=dict(marker=dict(color="#DC2626")),
        totals=dict(marker=dict(color=COLOR_SECONDARY)),
    ))
    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            tickangle=-40,
            tickfont=dict(size=9, color="#1E293B"),
            linecolor="#CBD5E1",
            gridcolor="#E2E8F0",
        ),
        yaxis=dict(
            title=dict(text="Score", font=dict(color="#475569")),
            showgrid=True,
            gridcolor="#E2E8F0",
            tickfont=dict(color="#475569"),
            linecolor="#CBD5E1",
        ),
        margin=dict(l=20, r=20, t=30, b=120),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        height=420,
    )
    return fig