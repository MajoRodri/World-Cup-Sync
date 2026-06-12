# Página 3 — Análisis por Fase / Page 3 — Analysis by Phase

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import solara

from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_BLUE,
    COLOR_NAVY, COLOR_MUTED, COLOR_TEXT,
    BASE_LAYOUT, STAGE_ORDER,
)
from app.components import QBlock, InsightBox


@solara.component
def Tab3_Fases(df: pd.DataFrame):
    QBlock("01", "⚡ Riesgo simultáneo · saturación digital y logística",
           "¿Qué fases del torneo generan más espectáculo y más público simultáneamente?",
           "Goles promedio vs. afluencia promedio por fase · eje dual")

    sagg = (df.groupby("stage_clean")
            .agg(avg_goals=("total_goals", "mean"), avg_att=("attendance", "mean"),
                 n=("total_goals", "count")).reset_index())
    sagg["_o"] = sagg["stage_clean"].map(
        {s: i for i, s in enumerate(STAGE_ORDER)}).fillna(99)
    sagg = sagg.sort_values("_o").drop(columns=["_o"])

    if sagg.empty:
        InsightBox("⚠️ Sin datos para las fases seleccionadas.")
        return

    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    fig4.add_trace(go.Bar(
        x=sagg["stage_clean"], y=sagg["avg_goals"], name="Goles Promedio",
        marker=dict(color=sagg["avg_goals"],
                    colorscale=[[0, "#1D2436"], [.5, COLOR_LIME], [1, "#FFE090"]],
                    showscale=False, line=dict(color=COLOR_NAVY, width=.8)),
        text=sagg["avg_goals"].apply(lambda v: f"{v:.2f}"), textposition="outside",
        customdata=sagg["n"],
        hovertemplate="<b>%{x}</b><br>Goles prom: %{y:.2f}<br>Partidos: %{customdata}<extra></extra>",
    ), secondary_y=False)
    fig4.add_trace(go.Scatter(
        x=sagg["stage_clean"], y=sagg["avg_att"], name="Afluencia Promedio",
        mode="lines+markers",
        line=dict(color=COLOR_BLUE, width=2.5),
        marker=dict(size=12, color=COLOR_BLUE, symbol="diamond",
                    line=dict(color=COLOR_NAVY, width=1.5)),
        hovertemplate="<b>%{x}</b><br>Afluencia prom: %{y:,.0f}<extra></extra>",
    ), secondary_y=True)
    fig4.update_layout(**BASE_LAYOUT,
        xaxis=dict(title="Fase de Torneo", showgrid=False,
                   tickfont=dict(size=11, color=COLOR_TEXT)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(color=COLOR_MUTED, size=10)),
        height=400, barmode="group")
    fig4.update_yaxes(title_text="Goles Promedio", secondary_y=False,
                      showgrid=True, gridcolor="#1C2840",
                      tickfont=dict(color=COLOR_LIME), title_font=dict(color=COLOR_LIME))
    fig4.update_yaxes(title_text="Afluencia Promedio", secondary_y=True,
                      showgrid=False, tickformat=",",
                      tickfont=dict(color=COLOR_BLUE), title_font=dict(color=COLOR_BLUE))
    solara.FigurePlotly(fig4)

    fase_max_g = sagg.loc[sagg["avg_goals"].idxmax(), "stage_clean"]
    sagg_att   = sagg.dropna(subset=["avg_att"])
    fase_max_a = (sagg_att.loc[sagg_att["avg_att"].idxmax(), "stage_clean"]
                  if not sagg_att.empty else "—")
    InsightBox(
        f"⚡ <b>Mayor espectáculo goleador:</b> <b>{fase_max_g}</b> · "
        f"<b>Mayor presión de afluencia:</b> <b>{fase_max_a}</b>. "
        f"Cuando coinciden en la misma jornada, el riesgo de saturación simultánea es máximo."
    )

    QBlock("02", "🗺️ Mapa de calor · pauta publicitaria premium",
           "¿En qué año y fase se concentró el mayor rendimiento goleador?",
           "Combinaciones edición × fase con mayor potencial de espectáculo", "red")

    pivot = df.pivot_table(values="total_goals", index="year",
                           columns="stage_clean", aggfunc="mean").round(2)
    pivot.columns = pivot.columns.astype(str)

    pivot_cols = [c for c in STAGE_ORDER if c in pivot.columns.tolist()]
    if not pivot_cols or pivot.empty:
        InsightBox("⚠️ Sin datos suficientes para el mapa de calor.", "red")
        return

    pivot = pivot[pivot_cols]
    x_labels = [str(c) for c in pivot.columns.tolist()]
    y_labels  = [str(int(y)) for y in pivot.index.tolist()]

    if not x_labels or not y_labels:
        InsightBox("⚠️ Sin datos suficientes para el mapa de calor.", "red")
        return

    zvals_np = pivot.values.copy().astype(float)
    zmin  = float(np.nanmin(zvals_np)) if not np.all(np.isnan(zvals_np)) else 0
    zmax  = float(np.nanmax(zvals_np)) if not np.all(np.isnan(zvals_np)) else 10

    # Plotly 6 serializa arrays numpy como bdata binario; Solara no lo soporta / Plotly 6 serializes numpy as binary bdata unsupported by Solara — convert to Python lists
    zvals = [[None if np.isnan(v) else float(v) for v in row] for row in zvals_np]

    text_grid = [
        [f"<b>{v:.1f}</b>" if not np.isnan(v) else "" for v in row]
        for row in zvals_np
    ]

    fig_heat = go.Figure(go.Heatmap(
        z=zvals,
        x=x_labels,
        y=y_labels,
        zmin=zmin, zmax=zmax,
        colorscale=[
            [0.00, "#0E2040"],
            [0.25, "#1A4A80"],
            [0.55, COLOR_BLUE],
            [0.78, COLOR_LIME],
            [1.00, COLOR_RED],
        ],
        text=text_grid,
        texttemplate="%{text}",
        textfont=dict(size=11, color="#FFFFFF"),
        hovertemplate="<b>%{y} · %{x}</b><br>Goles promedio: %{z:.2f}<extra></extra>",
        xgap=2, ygap=2,
        showscale=True,
        colorbar=dict(
            title=dict(text="g/p", font=dict(color=COLOR_MUTED, size=10)),
            tickfont=dict(color=COLOR_MUTED, size=9),
            thickness=14,
            bgcolor="rgba(13,19,33,0.8)",
            bordercolor="rgba(205,255,0,0.12)",
            borderwidth=1,
        ),
    ))
    row_h  = max(22, min(38, 560 // max(len(pivot), 1)))
    height = max(380, min(740, len(pivot) * row_h + 120))
    heat_layout = {**BASE_LAYOUT, "margin": dict(t=50, b=50, l=55, r=80)}
    fig_heat.update_layout(
        **heat_layout,
        xaxis=dict(
            title="Fase", showgrid=False,
            tickfont=dict(size=11, color=COLOR_TEXT),
            side="bottom",
        ),
        yaxis=dict(
            title="Edición", showgrid=False,
            tickfont=dict(size=10, color=COLOR_MUTED),
            autorange="reversed",
        ),
        height=height,
    )
    solara.FigurePlotly(fig_heat)
