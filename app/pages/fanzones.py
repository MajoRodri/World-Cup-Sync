# Página 2 — Fan Zones y Venues / Page 2 — Fan Zones and Venues

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import solara
import solara.lab

from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_BLUE,
    COLOR_NAVY, COLOR_MUTED, COLOR_TEXT,
    BASE_LAYOUT, play_menu,
)
from app.components import QBlock, InsightBox, plotly_iframe


def _kde(data: np.ndarray, n_pts: int = 250):
    """Gaussian KDE using Silverman's bandwidth rule (no scipy dependency)."""
    data = np.asarray(data, dtype=float)
    n = len(data)
    if n < 5:
        return np.array([]), np.array([])
    h = 1.06 * data.std() * n ** (-0.2)
    if h == 0:
        return np.array([]), np.array([])
    x = np.linspace(data.min() - h, data.max() + h, n_pts)
    kde = (np.exp(-0.5 * ((x[:, None] - data[None, :]) / h) ** 2)
           .sum(axis=1)) / (n * h * np.sqrt(2 * np.pi))
    return x, kde


@solara.component
def Tab2_FanZones(df: pd.DataFrame):
    with solara.Columns([1, 1]):
        with solara.Column():
            QBlock("01", "🌆 Fan Zones · Seguridad y logística",
                   "¿Qué ciudades concentran mayor presión de afluencia?",
                   "Top 12 sedes · dimensionamiento de accesos y zonas de servicio", "blue")

            city_df = (df.dropna(subset=["attendance"])
                       .groupby("city")["attendance"]
                       .agg(["mean", "count", "max"]).reset_index()
                       .rename(columns={"mean": "avg", "count": "n", "max": "pk"})
                       .nlargest(12, "avg").sort_values("avg", ascending=True))

            if city_df.empty:
                InsightBox("⚠️ Sin datos de afluencia para las ciudades seleccionadas.", "blue")
            else:
                city_df = city_df.reset_index(drop=True)
                n = len(city_df)
                bar_cols = [
                    f"rgba({int(21+(255-21)*i/max(n-1,1))},"
                    f"{int(101+(199-101)*i/max(n-1,1))},"
                    f"{int(192+(44-192)*i/max(n-1,1))},0.88)"
                    for i in range(n)
                ]
                ht2 = ("<b>%{y}</b><br>Afluencia promedio: <b>%{x:,.0f}</b><br>"
                       "Partidos: %{customdata[0]}<br>Pico: %{customdata[1]:,.0f}<extra></extra>")

                def _city_bar(sub, colors):
                    return go.Bar(
                        x=sub["avg"].tolist(), y=sub["city"].tolist(),
                        orientation="h",
                        marker=dict(color=colors, line=dict(color=COLOR_NAVY, width=0.5)),
                        customdata=np.column_stack([sub["n"], sub["pk"]]),
                        hovertemplate=ht2,
                    )

                fig2 = go.Figure(_city_bar(city_df.iloc[:1], [bar_cols[0]]))

                fig2.frames = [
                    go.Frame(
                        data=[_city_bar(city_df.iloc[:i+1], bar_cols[:i+1])],
                        traces=[0],
                        name=str(i+1),
                    )
                    for i in range(n)
                ]

                fig2.update_layout(
                    **{**BASE_LAYOUT, "margin": dict(t=60, b=70, l=15, r=15)},
                    xaxis=dict(title="Afluencia Promedio", showgrid=True, gridcolor="#1C2840",
                               tickformat=",", tickfont=dict(size=9, color=COLOR_MUTED),
                               range=[0, float(city_df["avg"].max()) * 1.18]),
                    yaxis=dict(title="", tickfont=dict(size=10, color=COLOR_TEXT),
                               categoryarray=city_df["city"].tolist(),
                               categoryorder="array",
                               range=[-0.5, n - 0.5]),
                    updatemenus=[play_menu(duration=220, y=-0.14)],
                    height=440, showlegend=False,
                )
                plotly_iframe(fig2, height=440)
                top_city = city_df.iloc[-1]
                InsightBox(
                    f"🌆 <b>Alerta Fan Zone:</b> <b>{top_city['city']}</b> encabeza con "
                    f"<b>{top_city['avg']:,.0f}</b> espectadores promedio y pico de "
                    f"<b>{top_city['pk']:,.0f}</b>. Priorizar dimensionamiento de seguridad.", "blue"
                )

        with solara.Column():
            QBlock("02", "📊 Probabilidad de saturación",
                   "¿Cuán probable es una saturación en streaming o Fan Zone?",
                   "Distribución estadística · percentiles P75 y P90 como umbrales operativos", "red")

            subtab_idx, set_subtab_idx = solara.use_state(0)

            with solara.lab.Tabs(value=subtab_idx, on_value=set_subtab_idx):
                with solara.lab.Tab("📺 Streaming"):
                    m_g   = float(df["total_goals"].mean())
                    std_g = float(df["total_goals"].std())
                    q75g  = float(df["total_goals"].quantile(.75))
                    q90g  = float(df["total_goals"].quantile(.90))
                    psat  = float((df["total_goals"] >= m_g + std_g).mean() * 100)

                    fig3a = go.Figure(go.Histogram(
                        x=df["total_goals"], nbinsx=18,
                        histnorm="probability density",
                        name="Distribución histórica",
                        marker=dict(color=COLOR_RED, opacity=.72,
                                    line=dict(color=COLOR_NAVY, width=.8)),
                        hovertemplate="Goles/partido: %{x}<br>Densidad: %{y:.4f}<extra></extra>",
                    ))
                    kde_x, kde_y = _kde(df["total_goals"].dropna().values)
                    if len(kde_x):
                        fig3a.add_trace(go.Scatter(
                            x=kde_x, y=kde_y, mode="lines",
                            name="Curva de Densidad KDE",
                            line=dict(color=COLOR_LIME, width=2.5),
                            hovertemplate="Densidad KDE: %{y:.4f}<extra></extra>",
                        ))
                    for xv, lbl, col in [(m_g,  f"Media: {m_g:.1f}",  "#F8FAFC"),
                                          (q75g, f"P75: {q75g:.0f}",  COLOR_MUTED),
                                          (q90g, f"P90: {q90g:.0f}",  COLOR_LIME)]:
                        fig3a.add_vline(x=xv, line_dash="dash", line_color=col, line_width=2,
                                        annotation_text=lbl, annotation_position="top right",
                                        annotation_font=dict(color=col, size=10))
                    fig3a.update_layout(**BASE_LAYOUT,
                        xaxis=dict(title="Goles por Partido", showgrid=False, dtick=1,
                                   tickfont=dict(size=9, color=COLOR_MUTED)),
                        yaxis=dict(title="Densidad de Probabilidad", showgrid=True,
                                   gridcolor="#1C2840",
                                   tickfont=dict(size=10, color=COLOR_MUTED)),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                    xanchor="right", x=1,
                                    bgcolor="rgba(0,0,0,0)",
                                    font=dict(color=COLOR_MUTED, size=9)),
                        showlegend=True, height=300, bargap=.08)
                    solara.FigurePlotly(fig3a)
                    InsightBox(
                        f"📺 <b>{psat:.1f}%</b> de partidos superan media+1σ "
                        f"({m_g+std_g:.1f} g) → escenario de pico CDN.", "red"
                    )

                with solara.lab.Tab("🌆 Fan Zones"):
                    dfa  = df.dropna(subset=["attendance"])
                    if dfa.empty:
                        InsightBox("⚠️ Sin datos de afluencia disponibles.", "blue")
                    else:
                        m_a  = float(dfa["attendance"].mean())
                        q75a = float(dfa["attendance"].quantile(.75))
                        q90a = float(dfa["attendance"].quantile(.90))
                        psta = float((dfa["attendance"] >= q75a).mean() * 100)

                        fig3b = go.Figure(go.Histogram(
                            x=dfa["attendance"], nbinsx=22,
                            histnorm="probability density",
                            name="Distribución histórica",
                            marker=dict(color=COLOR_BLUE, opacity=.72,
                                        line=dict(color=COLOR_NAVY, width=.8)),
                            hovertemplate="Espectadores: %{x:,.0f}<br>Densidad: %{y:.2e}<extra></extra>",
                        ))
                        kde_xa, kde_ya = _kde(dfa["attendance"].values)
                        if len(kde_xa):
                            fig3b.add_trace(go.Scatter(
                                x=kde_xa, y=kde_ya, mode="lines",
                                name="Curva de Densidad KDE",
                                line=dict(color=COLOR_LIME, width=2.5),
                                hovertemplate="Densidad KDE: %{y:.2e}<extra></extra>",
                            ))
                        for xv, lbl, col in [(m_a,  f"Media: {m_a:,.0f}",  "#F8FAFC"),
                                              (q75a, f"P75: {q75a:,.0f}",  COLOR_MUTED),
                                              (q90a, f"P90: {q90a:,.0f}",  COLOR_LIME)]:
                            fig3b.add_vline(x=xv, line_dash="dash", line_color=col, line_width=2,
                                            annotation_text=lbl, annotation_position="top right",
                                            annotation_font=dict(color=col, size=10))
                        fig3b.update_layout(**BASE_LAYOUT,
                            xaxis=dict(title="Espectadores", showgrid=False, tickformat=",",
                                       tickfont=dict(size=9, color=COLOR_MUTED)),
                            yaxis=dict(title="Densidad de Probabilidad", showgrid=True,
                                       gridcolor="#1C2840",
                                       tickfont=dict(size=10, color=COLOR_MUTED)),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                        xanchor="right", x=1,
                                        bgcolor="rgba(0,0,0,0)",
                                        font=dict(color=COLOR_MUTED, size=9)),
                            showlegend=True, height=300, bargap=.08)
                        solara.FigurePlotly(fig3b)
                        InsightBox(
                            f"🌆 <b>{psta:.1f}%</b> de partidos superan P75 "
                            f"({q75a:,.0f} esp.) → umbral de alerta Fan Zone.", "blue"
                        )

    QBlock("03", "🏟️ Infraestructura · Fan Zones de alta densidad",
           "¿Qué estadios son los verdaderos templos del fútbol mundial?",
           "Top 10 recintos por afluencia promedio · benchmarks de capacidad", "blue")

    stad = (df.dropna(subset=["attendance"])
            .groupby(["stadium", "city"])["attendance"]
            .agg(["mean", "count", "max"]).reset_index()
            .rename(columns={"mean": "avg", "count": "n", "max": "pk"})
            .nlargest(10, "avg").sort_values("avg", ascending=True))

    if stad.empty:
        InsightBox("⚠️ Sin datos de estadios para los filtros actuales.", "blue")
        return

    stad["label"] = stad["stadium"] + "  ·  " + stad["city"]
    fig_s = go.Figure(go.Bar(
        x=stad["avg"], y=stad["label"], orientation="h",
        marker=dict(color=stad["avg"],
                    colorscale=[[0, "#1D2436"], [.5, COLOR_BLUE], [1, COLOR_LIME]],
                    showscale=False, line=dict(color=COLOR_NAVY, width=.5)),
        customdata=np.column_stack([stad["n"], stad["pk"]]),
        hovertemplate=(
            "<b>%{y}</b><br>Promedio: %{x:,.0f}<br>"
            "Partidos: %{customdata[0]}<br>Récord: %{customdata[1]:,.0f}<extra></extra>"
        ),
        text=stad["avg"].apply(lambda v: f"{v/1000:.0f}K"),
        textposition="outside", textfont=dict(color=COLOR_MUTED, size=9),
    ))
    fig_s.update_layout(**BASE_LAYOUT,
        xaxis=dict(title="Afluencia Promedio", showgrid=True, gridcolor="#1C2840",
                   tickformat=",", tickfont=dict(size=9, color=COLOR_MUTED)),
        yaxis=dict(title="", tickfont=dict(size=9, color=COLOR_TEXT)),
        height=380, showlegend=False)
    solara.FigurePlotly(fig_s)
