# comment : import des bibliothèques plotly et constants car on a besoin de plotly pour créer le graphique et constants pour la couleur primaire
import plotly.graph_objects as go
from utils.constants import COLOR_PRIMARY

# comment : ici on définit la palette de couleurs pour le graphique
PALETTE = [
    "#003366","#004488","#0055AA","#D4AF37","#C9A82C",
    "#0E9F6E","#16A34A","#F59E0B","#DC2626","#7C3AED",
    "#0891B2","#DB2777","#059669","#D97706",
]

# comment : cette fonction retourne le graphique des contributions
def donut_chart(rows: list) -> go.Figure:
    labels = [r["label"] for r in rows]
    values = [max(r["weighted"], 0.01) for r in rows]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.52,
        marker=dict(
            colors=PALETTE[:len(rows)],
            line=dict(color="#FFFFFF", width=2),
        ),
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Score pondéré: %{value:.2f}<br>Part: %{percent}<extra></extra>",
        textfont=dict(size=10, color="#FFFFFF"),
    ))
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v", x=1.02, y=0.5,
            font=dict(size=9, color="#1E293B"),
        ),
        annotations=[dict(
            text="Contributions",
            x=0.5, y=0.5,
            font=dict(size=12, color=COLOR_PRIMARY, family="Inter"),
            showarrow=False,
        )],
        margin=dict(l=20, r=140, t=20, b=20),
        paper_bgcolor="#FFFFFF",
        height=380,
    )
    return fig