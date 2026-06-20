import plotly.graph_objects as go
from utils.constants import COLOR_PRIMARY, COLOR_SUCCESS, COLOR_DANGER


def _score_color(score: int) -> str:
    if score >= 80: return COLOR_SUCCESS
    if score >= 60: return "#16A34A"
    if score >= 40: return "#F59E0B"
    return COLOR_DANGER


def weighted_bar_chart(rows: list) -> go.Figure:
    labels   = [r["label"] for r in rows]
    weighted = [r["weighted"] for r in rows]
    colors_  = [_score_color(r["partial"]) for r in rows]

    fig = go.Figure(go.Bar(
        x=weighted,
        y=labels,
        orientation="h",
        marker=dict(color=colors_, line=dict(color="rgba(0,0,0,0.08)", width=1)),
        text=[f"{w:.2f}" for w in weighted],
        textposition="outside",
        textfont=dict(size=10, color="#1E293B"),
        hovertemplate="<b>%{y}</b><br>Score pondéré: %{x:.2f}<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(
            range=[0, max(r["poids"] for r in rows) + 2],
            title=dict(text="Score pondéré", font=dict(color="#475569")),
            showgrid=True,
            gridcolor="#E2E8F0",
            tickfont=dict(color="#475569"),
            linecolor="#CBD5E1",
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=10, color="#1E293B"),
            linecolor="#CBD5E1",
        ),
        margin=dict(l=20, r=60, t=20, b=40),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        height=max(300, len(rows) * 34),
    )
    return fig


def partial_bar_chart(rows: list) -> go.Figure:
    labels  = [r["label"] for r in rows]
    partial = [r["partial"] for r in rows]
    colors_ = [_score_color(s) for s in partial]

    fig = go.Figure(go.Bar(
        x=labels,
        y=partial,
        marker=dict(color=colors_, line=dict(color="rgba(0,0,0,0.08)", width=1)),
        text=[f"{s}" for s in partial],
        textposition="outside",
        textfont=dict(size=10, color="#1E293B"),
        hovertemplate="<b>%{x}</b><br>Score: %{y}/100<extra></extra>",
    ))
    fig.update_layout(
        yaxis=dict(
            range=[0, 115],
            title=dict(text="Score partiel (/100)", font=dict(color="#475569")),
            showgrid=True,
            gridcolor="#E2E8F0",
            tickfont=dict(color="#475569"),
            linecolor="#CBD5E1",
        ),
        xaxis=dict(
            tickangle=-35,
            tickfont=dict(size=9, color="#1E293B"),
            linecolor="#CBD5E1",
        ),
        margin=dict(l=20, r=20, t=20, b=100),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        height=380,
    )
    return fig