import plotly.graph_objects as go
from utils.constants import COLOR_PRIMARY, COLOR_SECONDARY


def radar_chart(rows: list) -> go.Figure:
    categories = [r["label"] for r in rows]
    partial    = [r["partial"] for r in rows]
    categories_loop = categories + [categories[0]]
    values_loop     = partial + [partial[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_loop,
        theta=categories_loop,
        fill="toself",
        fillcolor="rgba(0,51,102,0.12)",
        line=dict(color=COLOR_PRIMARY, width=2.5),
        name="Score partiel",
    ))
    fig.add_trace(go.Scatterpolar(
        r=[100] * (len(categories) + 1),
        theta=categories_loop,
        fill="toself",
        fillcolor="rgba(212,175,55,0.07)",
        line=dict(color=COLOR_SECONDARY, width=1.5, dash="dot"),
        name="Maximum",
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="#F8FAFC",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color="#475569"),
                gridcolor="#CBD5E1",
                linecolor="#CBD5E1",
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color="#1E293B"),
                linecolor="#CBD5E1",
                gridcolor="#CBD5E1",
            ),
        ),
        showlegend=True,
        legend=dict(
            orientation="h", y=-0.1,
            font=dict(color="#1E293B", size=11),
        ),
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        height=420,
    )
    return fig