import plotly.graph_objects as go


def gauge_chart(score: float, risk_class: str) -> go.Figure:
    color_map = {"A": "#0E9F6E", "B": "#16A34A", "C": "#F59E0B", "D": "#DC2626"}
    needle_color = color_map.get(risk_class, "#003366")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={
            "reference": 65,
            "increasing": {"color": "#0E9F6E"},
            "decreasing": {"color": "#DC2626"},
        },
        number={"suffix": "/100", "font": {"size": 36, "color": "#003366", "family": "Inter"}},
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickwidth=1,
                tickcolor="#475569",
                tickfont=dict(size=10, color="#475569"),
            ),
            bar=dict(color=needle_color, thickness=0.25),
            bgcolor="#F8FAFC",
            borderwidth=2,
            bordercolor="#CBD5E1",
            steps=[
                {"range": [0,  50], "color": "#FEE2E2"},
                {"range": [50, 65], "color": "#FEF3C7"},
                {"range": [65, 80], "color": "#D1FAE5"},
                {"range": [80,100], "color": "#A7F3D0"},
            ],
            threshold=dict(
                line=dict(color="#003366", width=4),
                thickness=0.8,
                value=score,
            ),
        ),
        title={"text": f"Score Final – Classe {risk_class}", "font": {"size": 14, "color": "#003366"}},
    ))
    fig.update_layout(
        margin=dict(l=30, r=30, t=50, b=20),
        paper_bgcolor="#FFFFFF",
        height=300,
    )
    return fig