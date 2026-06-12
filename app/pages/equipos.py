# Página 4 — Equipos / Page 4 — Teams

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import solara

from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_BLUE,
    COLOR_NAVY, COLOR_MUTED, COLOR_TEXT,
    BASE_LAYOUT, play_menu,
)
from app.components import QBlock, InsightBox, plotly_iframe


@solara.component
def Tab4_Equipos(df: pd.DataFrame):
    hs  = df[["year", "home_team", "home_goals", "away_goals"]].copy()
    hs.columns  = ["year", "team", "scored", "conceded"]
    aws = df[["year", "away_team", "away_goals", "home_goals"]].copy()
    aws.columns = ["year", "team", "scored", "conceded"]
    tall = pd.concat([hs, aws], ignore_index=True)
    tall["win"]  = tall["scored"] > tall["conceded"]
    tall["draw"] = tall["scored"] == tall["conceded"]
    tall["loss"] = tall["scored"] < tall["conceded"]

    tagg = (tall.groupby("team").agg(
        partidos=("scored",   "count"),
        gf=("scored",         "sum"),
        gc=("conceded",       "sum"),
        avg_gf=("scored",     "mean"),
        avg_gc=("conceded",   "mean"),
        victorias=("win",     "sum"),
        empates=("draw",      "sum"),
        derrotas=("loss",     "sum"),
    ).reset_index())
    tagg["diff"]    = tagg["gf"] - tagg["gc"]
    tagg["win_pct"] = (tagg["victorias"] / tagg["partidos"] * 100).round(1)

    min_p = max(3, len(df) // 80)
    tfilt = tagg[tagg["partidos"] >= min_p]

    if tfilt.empty:
        InsightBox(f"⚠️ Amplía los filtros para ver estadísticas de equipos (mín. {min_p} partidos).")
        return

    with solara.Columns([3, 2]):
        with solara.Column():
            QBlock("01", "🥇 Ranking ofensivo histórico",
                   "¿Qué selecciones han dominado el ataque en el Mundial?",
                   f"Top 15 · goles anotados por partido · mín. {min_p} encuentros")

            top15 = tfilt.nlargest(15, "avg_gf").sort_values("avg_gf", ascending=True).reset_index(drop=True)
            q80   = top15["avg_gf"].quantile(.80)
            q50   = top15["avg_gf"].quantile(.50)
            bc    = [COLOR_LIME if v >= q80 else COLOR_RED if v >= q50 else COLOR_BLUE
                     for v in top15["avg_gf"]]

            ht = ("<b>%{y}</b><br>Goles/partido: <b>%{x:.2f}</b><br>"
                  "Partidos: %{customdata[0]}<br>Total GF: %{customdata[1]}<br>"
                  "% Victorias: %{customdata[2]:.1f}%<br>"
                  "Dif. goles: %{customdata[3]:+d}<extra></extra>")

            def _bar_trace(sub, colors):
                return go.Bar(
                    x=sub["avg_gf"].tolist(), y=sub["team"].tolist(),
                    orientation="h",
                    marker=dict(color=colors, line=dict(color=COLOR_NAVY, width=.5)),
                    customdata=np.column_stack([sub["partidos"], sub["gf"],
                                               sub["win_pct"], sub["diff"]]),
                    hovertemplate=ht,
                    text=sub["avg_gf"].apply(lambda v: f"{v:.2f}").tolist(),
                    textposition="outside", textfont=dict(color=COLOR_MUTED, size=9),
                )

            fig_t = go.Figure(_bar_trace(top15.iloc[:1], [bc[0]]))

            fig_t.frames = [
                go.Frame(
                    data=[_bar_trace(top15.iloc[:i+1], bc[:i+1])],
                    traces=[0],
                    name=str(i+1),
                )
                for i in range(len(top15))
            ]

            fig_t.update_layout(**{**BASE_LAYOUT, "margin": dict(t=60, b=70, l=15, r=15)},
                xaxis=dict(title="Goles Anotados / Partido", showgrid=True,
                           gridcolor="#1C2840", tickfont=dict(size=9, color=COLOR_MUTED),
                           range=[0, float(top15["avg_gf"].max()) * 1.18]),
                yaxis=dict(title="", tickfont=dict(size=10, color=COLOR_TEXT),
                           categoryarray=top15["team"].tolist(),
                           categoryorder="array",
                           range=[-0.5, len(top15) - 0.5]),
                updatemenus=[play_menu(duration=200, y=-0.14)],
                height=500, showlegend=False)
            plotly_iframe(fig_t, height=500)

            best_team = top15.iloc[-1]
            InsightBox(
                f"🥇 Líder ofensivo: <b>{best_team['team']}</b> con "
                f"<b>{best_team['avg_gf']:.2f} g/p</b> en "
                f"{int(best_team['partidos'])} partidos · "
                f"<b>{best_team['win_pct']:.0f}% de victorias</b>."
            )

        with solara.Column():
            QBlock("02", "⚔️ Posicionamiento táctico histórico",
                   "¿Cómo se posicionan las selecciones entre ataque y defensa?",
                   "GF/PJ vs GC/PJ · tamaño = partidos · color = diferencia", "red")

            mx = float(tfilt["partidos"].clip(upper=80).max())
            fig_sc = go.Figure()
            fig_sc.add_hline(y=float(tfilt["avg_gc"].median()), line_dash="dot",
                             line_color=COLOR_MUTED, opacity=.3)
            fig_sc.add_vline(x=float(tfilt["avg_gf"].median()), line_dash="dot",
                             line_color=COLOR_MUTED, opacity=.3)
            fig_sc.add_trace(go.Scatter(
                x=tfilt["avg_gf"], y=tfilt["avg_gc"],
                mode="markers+text",
                marker=dict(
                    size=tfilt["partidos"].clip(upper=80) / mx * 30 + 6,
                    color=tfilt["diff"],
                    colorscale=[[0, COLOR_RED], [.5, COLOR_BLUE], [1, COLOR_LIME]],
                    cmid=0, showscale=True,
                    colorbar=dict(title=dict(text="Dif.",
                                            font=dict(color=COLOR_MUTED, size=9)),
                                  tickfont=dict(color=COLOR_MUTED, size=8),
                                  thickness=10, x=1.02),
                    line=dict(color=COLOR_NAVY, width=1),
                ),
                text=tfilt["team"],
                textposition="top center",
                textfont=dict(size=7, color=COLOR_MUTED),
                customdata=np.column_stack([tfilt["partidos"], tfilt["win_pct"], tfilt["diff"]]),
                hovertemplate=(
                    "<b>%{text}</b><br>GF/PJ: %{x:.2f}<br>GC/PJ: %{y:.2f}<br>"
                    "Partidos: %{customdata[0]}<br>% Vict.: %{customdata[1]:.1f}%<br>"
                    "Dif: %{customdata[2]:+d}<extra></extra>"
                ),
            ))
            fig_sc.update_layout(**BASE_LAYOUT,
                xaxis=dict(title="Goles Anotados / Partido", showgrid=True,
                           gridcolor="#1C2840", tickfont=dict(size=9, color=COLOR_MUTED)),
                yaxis=dict(title="Goles Recibidos / Partido", showgrid=True,
                           gridcolor="#1C2840", tickfont=dict(size=9, color=COLOR_MUTED)),
                height=480, showlegend=False)
            solara.FigurePlotly(fig_sc)

    QBlock("03", "📋 Tabla completa de rendimiento",
           "Ranking completo — todos los indicadores por selección",
           f"Ordenable · solo equipos con ≥{min_p} partidos en el período")

    disp = (tfilt[["team", "partidos", "victorias", "empates", "derrotas",
                    "gf", "gc", "diff", "avg_gf", "avg_gc", "win_pct"]]
            .sort_values("avg_gf", ascending=False)
            .rename(columns={
                "team": "Equipo", "partidos": "PJ",
                "victorias": "G", "empates": "E", "derrotas": "P",
                "gf": "GF", "gc": "GC", "diff": "+/-",
                "avg_gf": "GF/PJ", "avg_gc": "GC/PJ", "win_pct": "% Vict.",
            }))
    disp["GF/PJ"] = disp["GF/PJ"].round(2)
    disp["GC/PJ"] = disp["GC/PJ"].round(2)
    solara.DataFrame(disp.reset_index(drop=True), items_per_page=20)
