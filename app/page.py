# Orquestador principal: sidebar, hero, KPIs y tabs / Main orchestrator: sidebar, hero, KPIs, tabs

import pandas as pd
import solara
import solara.lab

from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_BLUE, COLOR_WHITE,
    COLOR_NAVY, COLOR_STEEL, COLOR_MUTED, COLOR_TEXT,
    APP_CSS,
)
from app.data import (
    df_raw, wc_df, DEMO_MODE,
    yr_min, yr_max, stages_all, teams_all, years_available,
)
from app.components.kpi_cards import KPICard
from app.components.sidebar   import AppSidebar
from app.pages.resumen    import Tab1_ResumenEjecutivo
from app.pages.fanzones   import Tab2_FanZones
from app.pages.fases      import Tab3_Fases
from app.pages.equipos    import Tab4_Equipos
from app.pages.explorer   import Tab5_Explorer
from app.pages.festivales import Tab6_Festivales


@solara.component
def Page():
    solara.Title("World Cup Sync")
    with solara.AppBarTitle():
        solara.HTML("div", unsafe_innerHTML=(
            '<div style="display:flex;align-items:center;gap:10px;">'
            '<img src="/static/public/trionda.png" '
            'style="height:30px;width:auto;" />'
            '<span style="font-size:.95rem;font-weight:800;'
            'letter-spacing:2px;color:#F8FAFC;">WORLD CUP SYNC</span>'
            '</div>'
        ))
    year_range,      set_year_range      = solara.use_state((yr_min, yr_max))
    selected_stages, set_selected_stages = solara.use_state(stages_all[:])
    selected_team,   set_selected_team   = solara.use_state("— Todos —")

    solara.Style(APP_CSS)

    yr0, yr1 = year_range

    def compute_df():
        if not selected_stages:
            return pd.DataFrame(columns=df_raw.columns)
        if df_raw.empty:
            return pd.DataFrame(columns=df_raw.columns)
        mask_team = (
            (df_raw["home_team"] == selected_team) |
            (df_raw["away_team"] == selected_team)
            if selected_team != "— Todos —"
            else pd.Series(True, index=df_raw.index)
        )
        return df_raw[
            df_raw["year"].between(yr0, yr1) &
            df_raw["stage_clean"].isin(selected_stages) &
            mask_team
        ].copy()

    df = solara.use_memo(compute_df,
                         [yr0, yr1, tuple(sorted(selected_stages)), selected_team])

    n_total    = int(df_raw["year"].nunique()) if not df_raw.empty else 0
    n_editions = int(df_raw.loc[df_raw["year"].between(yr0, yr1), "year"].nunique()
                     if not df_raw.empty else 0)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    AppSidebar(
        year_range=year_range,
        set_year_range=set_year_range,
        selected_stages=selected_stages,
        set_selected_stages=set_selected_stages,
        selected_team=selected_team,
        set_selected_team=set_selected_team,
        n_editions=n_editions,
        stages_all=stages_all,
        teams_all=teams_all,
        years_available=years_available,
    )

    # ── Contenido principal ───────────────────────────────────────────────────
    with solara.Column(style={"padding": "0 8px 40px"}):

        if DEMO_MODE:
            solara.Warning(
                "⚠️ Modo Demo — Los datos reales no están disponibles. "
                "Se muestran datos sintéticos con el mismo esquema."
            )

        if not selected_stages:
            solara.Warning("⚠️ Selecciona al menos una Fase en el panel lateral.")
            return

        if df is None or df.empty:
            solara.Warning("⚠️ Sin datos con los filtros actuales. Amplía el rango, fases o equipo.")
            return

        stages_label = (", ".join(selected_stages) if len(selected_stages) <= 3
                        else f"{len(selected_stages)} fases")
        team_label   = (f"<b style='color:{COLOR_LIME};'> · {selected_team}</b>"
                        if selected_team != "— Todos —" else "")

        # ── Hero banner ───────────────────────────────────────────────────────
        solara.HTML("div", unsafe_innerHTML=f"""
            <div class="wcs-hero" style="
                background: linear-gradient(120deg,rgba(8,14,26,.90),rgba(15,33,61,.88)),
                            linear-gradient(90deg,rgba(232,0,45,.12),rgba(205,255,0,.07),rgba(21,101,192,.14));
                border:1px solid {COLOR_LIME}28;border-left:4px solid {COLOR_LIME};
                border-radius:14px;padding:26px 32px;margin-bottom:20px;
                position:relative;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.6);">

                <div style="position:absolute;top:0;left:0;width:100%;height:100%;
                    pointer-events:none;overflow:hidden;">
                    <div style="position:absolute;width:40%;height:2px;
                        background:linear-gradient(90deg,transparent,{COLOR_LIME}18,transparent);
                        animation:shimmer-hero 5s ease-in-out infinite;top:30%;"></div>
                </div>

                <div style="position:absolute;right:28px;top:12px;font-size:3.2rem;
                    animation:float-ball 5s ease-in-out infinite;opacity:.22;
                    pointer-events:none;">⚽</div>
                <div style="position:absolute;right:90px;bottom:8px;font-size:2rem;
                    animation:float-ball2 7s ease-in-out infinite 1s;opacity:.15;
                    pointer-events:none;">🏆</div>
                <div style="position:absolute;right:55px;top:50%;font-size:1.6rem;
                    animation:float-ball 6s ease-in-out infinite 3s;opacity:.12;
                    pointer-events:none;">⚽</div>

                <p style="font-size:.65rem;font-weight:700;color:{COLOR_LIME};
                    text-transform:uppercase;letter-spacing:2.5px;margin:0 0 5px;">
                    FIFA World Cup 1930–2022 · Analytics Platform</p>
                <h1 style="font-size:1.55rem;font-weight:900;color:{COLOR_WHITE};
                    letter-spacing:-.3px;margin:0 0 7px;line-height:1.2;">
                    WORLD CUP SYNC</h1>
                <p style="color:{COLOR_MUTED};font-size:.82rem;margin:0;line-height:1.7;">
                    Inteligencia operativa para
                    <b style="color:{COLOR_RED};">Streaming</b> y
                    <b style="color:#6AB0E8;">Fan Zones Urbanas</b>
                    &nbsp;·&nbsp;
                    Ediciones <b style="color:{COLOR_WHITE};">{yr0}–{yr1}</b>
                    &nbsp;·&nbsp; {stages_label}{team_label}
                </p>

                <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;">
                    <span style="background:{COLOR_LIME}18;border:1px solid {COLOR_LIME}45;
                        color:{COLOR_LIME};border-radius:20px;padding:3px 12px;font-size:.66rem;
                        font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                        ⚽ {len(df):,} partidos</span>
                    <span style="background:{COLOR_RED}18;border:1px solid {COLOR_RED}45;
                        color:#FF6B8A;border-radius:20px;padding:3px 12px;font-size:.66rem;
                        font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                        📺 Streaming CDN</span>
                    <span style="background:{COLOR_BLUE}22;border:1px solid {COLOR_BLUE}55;
                        color:#6AB0E8;border-radius:20px;padding:3px 12px;font-size:.66rem;
                        font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                        🌆 Fan Zones</span>
                    <span style="background:rgba(255,255,255,.08);
                        border:1px solid rgba(255,255,255,.2);color:{COLOR_WHITE};
                        border-radius:20px;padding:3px 12px;font-size:.66rem;
                        font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                        🏅 {n_editions} ediciones</span>
                </div>
            </div>
        """)

        # ── KPIs ──────────────────────────────────────────────────────────────
        total_matches = len(df)
        avg_goals     = float(df["total_goals"].mean())
        att_df_kpi    = df.dropna(subset=["attendance"])

        peak_att = float(att_df_kpi["attendance"].max()) if not att_df_kpi.empty else 0
        peak_row = att_df_kpi.loc[att_df_kpi["attendance"].idxmax()] if not att_df_kpi.empty else None
        peak_fmt = f"{peak_att/1_000:.0f}K" if peak_att >= 100_000 else f"{peak_att:,.0f}"
        peak_sub = (f"{peak_row['home_team']} vs {peak_row['away_team']}, {int(peak_row['year'])}"
                    if peak_row is not None else "—")

        max_g_row   = df.loc[df["total_goals"].idxmax()]
        max_g_val   = int(max_g_row["total_goals"])
        max_g_label = (f"{max_g_row['home_team']} {int(max_g_row['home_goals'])}–"
                       f"{int(max_g_row['away_goals'])} {max_g_row['away_team']}")
        by_ed    = df.groupby("year")["total_goals"].mean()
        best_yr  = int(by_ed.idxmax())
        best_gpg = float(by_ed.max())

        with solara.Columns([1, 1, 1, 1, 1]):
            KPICard("⚽", "Partidos Analizados",    f"{total_matches:,}",
                    f"en {n_editions} ediciones",   COLOR_LIME)
            KPICard("📺", "Goles / Partido",         f"{avg_goals:.2f}",
                    "predictor CDN",                 COLOR_RED)
            KPICard("🏟️", "Pico de Afluencia",       peak_fmt,
                    peak_sub[:34],                   COLOR_BLUE)
            KPICard("🔥", "Mayor Goleada Histórica",  f"{max_g_val} goles",
                    max_g_label[:34],                COLOR_LIME)
            KPICard("🏅", "Edición Más Golera",       str(best_yr),
                    f"{best_gpg:.2f} g/p promedio",  COLOR_WHITE)

        solara.HTML("div", unsafe_innerHTML="<div style='height:16px'></div>")

        # ── Páginas principales ───────────────────────────────────────────────
        with solara.lab.Tabs():
            with solara.lab.Tab("📊 Resumen Ejecutivo"):
                Tab1_ResumenEjecutivo(df, wc_df, year_range)

            with solara.lab.Tab("🌆 Fan Zones y Venues"):
                Tab2_FanZones(df)

            with solara.lab.Tab("🏅 Análisis por Fase"):
                Tab3_Fases(df)

            with solara.lab.Tab("🌍 Equipos"):
                Tab4_Equipos(df)

            with solara.lab.Tab("🔍 Match Explorer"):
                Tab5_Explorer(df)

            with solara.lab.Tab("🗺️ Oportunidad 2026"):
                Tab6_Festivales(df)

        # ── Footer ────────────────────────────────────────────────────────────
        solara.HTML("div", unsafe_innerHTML=f"""
            <hr style="border:none;border-top:1px solid {COLOR_LIME}18;margin:32px 0 12px;">
            <div style="display:flex;align-items:center;justify-content:center;
                gap:16px;flex-wrap:wrap;padding:8px 0;">
                <span style="font-size:1.4rem;animation:float-ball 5s ease-in-out infinite;
                    display:inline-block;">⚽</span>
                <p style="text-align:center;color:{COLOR_MUTED};font-size:.66rem;
                    line-height:2;margin:0;">
                    <b style="color:{COLOR_TEXT};">World Cup Sync Analytics Platform</b>
                    &nbsp;·&nbsp; Fuente: FIFA / Kaggle (piterfm)
                    &nbsp;·&nbsp; <b>USO INTERNO — CONFIDENCIAL</b>
                </p>
                <span style="font-size:1.4rem;animation:float-ball2 6s ease-in-out infinite 1s;
                    display:inline-block;">🏆</span>
            </div>
        """)
