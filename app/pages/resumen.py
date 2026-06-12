# Página 1 — Resumen Ejecutivo / Page 1 — Executive Summary

import pandas as pd
import plotly.graph_objects as go
import solara

from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_MUTED, COLOR_TEXT,
    COLOR_NAVY, COLOR_BLUE, COLOR_STEEL,
    BASE_LAYOUT, play_menu,
)
from app.components import QBlock, InsightBox, plotly_iframe


_HOST_FLAGS: dict[str, str] = {
    "Uruguay":              "🇺🇾",
    "Italy":                "🇮🇹",
    "France":               "🇫🇷",
    "Brazil":               "🇧🇷",
    "Switzerland":          "🇨🇭",
    "Sweden":               "🇸🇪",
    "Chile":                "🇨🇱",
    "England":              "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "United Kingdom":       "🇬🇧",
    "Mexico":               "🇲🇽",
    "West Germany":         "🇩🇪",
    "Germany":              "🇩🇪",
    "Argentina":            "🇦🇷",
    "Spain":                "🇪🇸",
    "United States":        "🇺🇸",
    "USA":                  "🇺🇸",
    "South Korea / Japan":  "🇰🇷🇯🇵",
    "Japan":                "🇯🇵",
    "Korea Republic":       "🇰🇷",
    "South Africa":         "🇿🇦",
    "Russia":               "🇷🇺",
    "Qatar":                "🇶🇦",
}


def _host_flag(host: str) -> str:
    for key, flag in _HOST_FLAGS.items():
        if key.lower() in host.lower():
            return flag
    return "🌍"


@solara.component
def Tab1_ResumenEjecutivo(df: pd.DataFrame, wc: pd.DataFrame, year_range: tuple):
    QBlock("01", "📺 Streaming · Planificación CDN y pauta premium",
           "¿Cómo ha evolucionado el espectáculo goleador en 92 años de Mundial?",
           "Goles promedio por partido · tendencia y campeones por edición", "red")

    gby = (df.groupby("year")["total_goals"]
           .agg(["mean", "min", "max"]).reset_index().sort_values("year")
           .reset_index(drop=True))
    gby["rolling"] = gby["mean"].rolling(3, center=True, min_periods=1).mean()
    global_mean = float(df["total_goals"].mean())

    first = gby.iloc[:1]

    fig1 = go.Figure()
    # Traza 0: banda estática de rango completo / Trace 0: static full-range band
    fig1.add_trace(go.Scatter(
        x=pd.concat([gby["year"], gby["year"].iloc[::-1]]),
        y=pd.concat([gby["max"],  gby["min"].iloc[::-1]]),
        fill="toself", fillcolor="rgba(205,255,0,0.05)",
        line=dict(color="rgba(0,0,0,0)"), name="Rango Mín–Máx", hoverinfo="skip",
    ))
    # Traza 1 animada: línea de media, inicia en el primer punto / Trace 1: animated mean line, starts at first point
    fig1.add_trace(go.Scatter(
        x=first["year"].tolist(), y=first["mean"].tolist(),
        name="Goles Promedio / Partido",
        mode="lines+markers",
        line=dict(color=COLOR_LIME, width=2.5),
        marker=dict(size=8, color=COLOR_LIME, symbol="circle",
                    line=dict(color=COLOR_NAVY, width=1.5)),
        fill="tozeroy", fillcolor="rgba(205,255,0,0.07)",
        hovertemplate="<b>Mundial %{x}</b><br>Promedio: %{y:.2f} g/p<extra></extra>",
    ))
    # Traza 2 animada: tendencia MM-3, inicia en el primer punto / Trace 2: animated rolling trend, starts at first point
    fig1.add_trace(go.Scatter(
        x=first["year"].tolist(), y=first["rolling"].tolist(),
        name="Tendencia MM-3",
        mode="lines", line=dict(color=COLOR_RED, width=2.5, dash="dot"),
        hovertemplate="Tendencia: %{y:.2f}<extra></extra>",
    ))

    fig1.frames = [
        go.Frame(
            data=[
                go.Scatter(
                    x=gby.iloc[:i+1]["year"].tolist(),
                    y=gby.iloc[:i+1]["mean"].tolist(),
                    mode="lines+markers", fill="tozeroy",
                    fillcolor="rgba(205,255,0,0.07)",
                    line=dict(color=COLOR_LIME, width=2.5),
                    marker=dict(size=8, color=COLOR_LIME, symbol="circle",
                                line=dict(color=COLOR_NAVY, width=1.5)),
                ),
                go.Scatter(
                    x=gby.iloc[:i+1]["year"].tolist(),
                    y=gby.iloc[:i+1]["rolling"].tolist(),
                    mode="lines", line=dict(color=COLOR_RED, width=2.5, dash="dot"),
                ),
            ],
            traces=[1, 2],
            name=str(int(gby.iloc[i]["year"])),
        )
        for i in range(len(gby))
    ]
    fig1.add_hline(y=global_mean, line_dash="dash", line_color=COLOR_MUTED, opacity=0.4,
                   annotation_text=f"Media: {global_mean:.2f} g/p",
                   annotation_position="bottom right",
                   annotation_font=dict(color=COLOR_MUTED, size=10))

    if not wc.empty:
        for _, wc_row in wc.iterrows():
            yr  = int(wc_row["Year"])
            row = gby[gby["year"] == yr]
            if row.empty or not (year_range[0] <= yr <= year_range[1]):
                continue
            val  = float(row["mean"].values[0])
            chmp = str(wc_row.get("Champion", "")).strip()
            if chmp:
                fig1.add_annotation(
                    x=yr, y=val, text=f"🏆 {chmp}",
                    showarrow=True, arrowhead=2,
                    arrowcolor=COLOR_LIME, arrowwidth=1.2, ax=0, ay=-38,
                    font=dict(size=8, color=COLOR_LIME),
                    bgcolor="rgba(13,19,33,0.85)",
                    bordercolor=COLOR_LIME, borderwidth=0.8, borderpad=3,
                )

    fig1.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=60, b=75, l=15, r=15)},
        xaxis=dict(title="Edición del Mundial", showgrid=False,
                   tickfont=dict(size=10, color=COLOR_MUTED),
                   range=[int(gby["year"].min()) - 3, int(gby["year"].max()) + 3]),
        yaxis=dict(title="Goles Promedio / Partido",
                   showgrid=True, gridcolor="#1C2840", gridwidth=0.5,
                   tickfont=dict(size=10, color=COLOR_MUTED),
                   range=[0, float(gby["max"].max()) * 1.18]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(color=COLOR_MUTED, size=10)),
        updatemenus=[play_menu(duration=350, y=-0.16)],
        height=420, hovermode="x unified",
    )
    plotly_iframe(fig1, height=420)

    pico_yr = int(gby.loc[gby["mean"].idxmax(), "year"])
    pico_v  = float(gby["mean"].max())
    InsightBox(
        f"📺 <b>Insight CDN:</b> La media del período es <b>{global_mean:.2f} g/p</b>. "
        f"El pico histórico fue <b>{pico_yr}</b> con <b>{pico_v:.2f} g/p</b>. "
        f"Ediciones anteriores a 1966 superan consistentemente la media actual — "
        f"filtra 2010–2022 para proyecciones operativas.", "red"
    )

    solara.HTML("div", unsafe_innerHTML=f"""
        <details style="margin-top:20px;">
            <summary style="cursor:pointer;list-style:none;display:flex;align-items:center;
                gap:10px;padding:12px 16px;
                border:1px solid {COLOR_RED}50;border-radius:8px;
                background:rgba(232,0,45,0.05);user-select:none;">
                <span style="font-size:1.1rem;">⚠️</span>
                <span style="font-size:.75rem;font-weight:700;color:{COLOR_RED};
                    text-transform:uppercase;letter-spacing:1.5px;">
                    Gobernanza de Datos &amp; Sesgos Identificados
                </span>
                <span style="font-size:.62rem;color:{COLOR_MUTED};margin-left:auto;">
                    Expandir ▾
                </span>
            </summary>
            <div style="border:1px solid {COLOR_RED}40;border-top:none;border-radius:0 0 8px 8px;
                padding:16px 18px 14px;background:rgba(232,0,45,0.03);">
                <p style="font-size:.62rem;color:{COLOR_MUTED};margin:0 0 12px;">
                    Limitaciones críticas del dataset — leer antes de tomar decisiones estratégicas
                </p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">
                    <div style="background:rgba(232,0,45,0.07);border:1px solid rgba(232,0,45,0.35);
                        border-radius:8px;padding:12px 14px;">
                        <div style="font-size:.70rem;font-weight:700;color:{COLOR_RED};margin-bottom:4px;">
                            🔴 Sesgo Temporal — CRÍTICO
                        </div>
                        <div style="font-size:.61rem;color:{COLOR_MUTED};line-height:1.75;">
                            La media global (2.82 g/p) sobreestima la era streaming en
                            <b style="color:#F8FAFC">+9.9%</b>.
                            Filtrar a <b style="color:{COLOR_LIME}">2010–2022</b> para proyecciones CDN.
                        </div>
                    </div>
                    <div style="background:rgba(232,0,45,0.07);border:1px solid rgba(232,0,45,0.35);
                        border-radius:8px;padding:12px 14px;">
                        <div style="font-size:.70rem;font-weight:700;color:{COLOR_RED};margin-bottom:4px;">
                            🔴 Sesgo de Formato — CRÍTICO
                        </div>
                        <div style="font-size:.61rem;color:{COLOR_MUTED};line-height:1.75;">
                            Ediciones 1930–1950 tenían 17–22 partidos vs. 64 actuales (CV &gt; 60%).
                            Comparar solo ediciones <b style="color:{COLOR_LIME}">≥ 52 partidos (1982+)</b>.
                        </div>
                    </div>
                    <div style="background:rgba(232,0,45,0.07);border:1px solid rgba(232,0,45,0.35);
                        border-radius:8px;padding:12px 14px;">
                        <div style="font-size:.70rem;font-weight:700;color:{COLOR_RED};margin-bottom:4px;">
                            🔴 Sesgo de Asistencia — CRÍTICO
                        </div>
                        <div style="font-size:.61rem;color:{COLOR_MUTED};line-height:1.75;">
                            Datos pre-1966 sin auditoría oficial. Récord Maracanã 1950
                            (<b style="color:#F8FAFC">173,850 esp.</b>) no verificado.
                            Filtrar <b style="color:{COLOR_LIME}">post-1970</b> para Fan Zones.
                        </div>
                    </div>
                    <div style="background:rgba(205,255,0,0.04);border:1px solid rgba(205,255,0,0.25);
                        border-radius:8px;padding:12px 14px;">
                        <div style="font-size:.70rem;font-weight:700;color:{COLOR_LIME};margin-bottom:4px;">
                            🟡 Sesgo Geográfico — ALTO
                        </div>
                        <div style="font-size:.61rem;color:{COLOR_MUTED};line-height:1.75;">
                            Europa representa el <b style="color:#F8FAFC">53.4%</b> de participaciones históricas.
                            África y Asia con representación suficiente solo desde
                            <b style="color:{COLOR_LIME}">2002</b>.
                        </div>
                    </div>
                </div>
                <div style="display:flex;align-items:center;justify-content:space-between;
                    padding:8px 12px;background:{COLOR_NAVY};border-radius:6px;">
                    <span style="font-size:.59rem;color:{COLOR_MUTED};">
                        Análisis completo: 8 sesgos identificados, cuantificados y con mitigaciones
                    </span>
                    <a href="https://majorodri.github.io/World-Cup-Sync/Sesgos.html"
                       target="_blank" style="font-size:.61rem;font-weight:700;color:{COLOR_LIME};
                       text-decoration:none;white-space:nowrap;margin-left:12px;">
                       Notebook de Sesgos ↗
                    </a>
                </div>
            </div>
        </details>
    """)

    if not wc.empty:
        wc_period = (wc[wc["Year"].between(*year_range)]
                     .sort_values("Year", ascending=False))
        if not wc_period.empty:
            QBlock("02", "🏆 Inteligencia histórica · contenido y Fan Zone",
                   "¿Qué campeones, sedes y goleadores marcaron cada edición?",
                   "Contexto editorial para campañas de activación", "lime")

            records = wc_period.to_dict("records")
            for i in range(0, len(records), 3):
                chunk = records[i:i+3]
                ncols = len(chunk)
                with solara.Columns([1] * ncols):
                    for r in chunk:
                        yr    = int(r["Year"])
                        host  = str(r.get("Host", "")).strip()
                        champ = str(r.get("Champion", "")).strip()
                        runup = str(r.get("Runner-Up", "")).strip()
                        att   = r.get("Attendance", 0)
                        mtch  = r.get("Matches", "?")
                        flag  = _host_flag(host)
                        try:
                            att_f = (f"{int(att)/1e6:.1f}M"
                                     if int(att) >= 1_000_000 else f"{int(att):,}")
                        except Exception:
                            att_f = str(att)
                        solara.HTML("div", unsafe_innerHTML=f"""
                            <div class="wcs-edition-card"
                                style="background:linear-gradient(135deg,{COLOR_STEEL} 0%,#162338 100%);
                                border:1px solid {COLOR_BLUE}35;border-top:3px solid {COLOR_BLUE};
                                border-radius:10px;padding:14px 16px;font-size:.82rem;
                                line-height:1.9;margin-bottom:8px;position:relative;overflow:hidden;">
                                <div style="position:absolute;right:-6px;bottom:-10px;
                                    font-size:3.5rem;opacity:.04;pointer-events:none;">🏆</div>
                                <div style="position:absolute;top:10px;right:12px;
                                    font-size:1.55rem;line-height:1;pointer-events:none;">
                                    {flag}</div>
                                <div style="font-size:1.4rem;font-weight:900;
                                    color:{COLOR_LIME};line-height:1.1;">{yr}</div>
                                <div style="font-size:.65rem;color:{COLOR_MUTED};
                                    text-transform:uppercase;letter-spacing:1px;
                                    margin-bottom:6px;">📍 {host}</div>
                                <div>🏆 <b style="color:{COLOR_LIME};">{champ}</b></div>
                                <div>🥈 <span style="color:{COLOR_MUTED};">{runup}</span></div>
                                <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px;">
                                    <span style="background:{COLOR_BLUE}22;
                                        border:1px solid {COLOR_BLUE}55;color:#6AB0E8;
                                        border-radius:20px;padding:3px 10px;font-size:.60rem;
                                        font-weight:700;text-transform:uppercase;
                                        letter-spacing:.8px;display:inline-block;">
                                        {att_f} esp.</span>
                                    <span style="background:{COLOR_LIME}18;
                                        border:1px solid {COLOR_LIME}45;color:{COLOR_LIME};
                                        border-radius:20px;padding:3px 10px;font-size:.60rem;
                                        font-weight:700;text-transform:uppercase;
                                        letter-spacing:.8px;display:inline-block;">
                                        ⚽ {mtch} partidos</span>
                                </div>
                            </div>
                        """)
