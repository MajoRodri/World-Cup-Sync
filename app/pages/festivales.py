# Página 6 — Fan Festivals 2026 / Page 6 — Fan Festivals 2026

import pandas as pd
import plotly.graph_objects as go
import solara
import solara.lab

from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_BLUE, COLOR_WHITE,
    COLOR_NAVY, COLOR_STEEL, COLOR_MUTED, COLOR_TEXT,
    BASE_LAYOUT, play_menu,
)
from app.components import QBlock, InsightBox, plotly_iframe
from app.data import df_raw

FESTIVALS = [
    dict(
        ciudad="Ciudad de México", pais="México", flag="🇲🇽",
        ubicacion="Zócalo · Plaza de la Constitución",
        fechas="11 jun – 19 jul 2026",
        acceso="Gratuito", registro=False, vip=False,
        capacidad_est=150_000,
        highlights="Banda El Recodo · K-Tigers · Frida: The Musical · Pantallas gigantes",
        restricciones="Sin mochilas grandes · Bolsas transparentes recomendadas",
        lat=19.4326, lon=-99.1332,
        csv_aliases=["Mexico City", "Ciudad de México", "Ciudad de Mexico"],
    ),
    dict(
        ciudad="Guadalajara", pais="México", flag="🇲🇽",
        ubicacion="Plaza Liberación · Centro Histórico",
        fechas="11 jun – 19 jul 2026 (días de partido)",
        acceso="Gratuito · Requiere pase digital FIFA", registro=True, vip=False,
        capacidad_est=40_000,
        highlights="Tacos y tortas ahogadas · Activaciones FIFA · Tienda oficial",
        restricciones="Cupo limitado · Registro obligatorio en plataforma FIFA",
        lat=20.6767, lon=-103.3475,
        csv_aliases=["Guadalajara"],
    ),
    dict(
        ciudad="Monterrey", pais="México", flag="🇲🇽",
        ubicacion="Parque Fundidora",
        fechas="11 jun – 19 jul 2026",
        acceso="Gratuito + Zonas VIP / Conciertos de pago", registro=False, vip=True,
        capacidad_est=80_000,
        highlights="Espacio industrial recuperado · Canchas recreativas · Gastronomía regia",
        restricciones="VIP y conciertos especiales requieren ticket (Ticketmaster)",
        lat=25.6714, lon=-100.2846,
        csv_aliases=["Monterrey"],
    ),
    dict(
        ciudad="Toronto", pais="Canadá", flag="🇨🇦",
        ubicacion="Fort York National Historic Site · The Bentway",
        fechas="11 jun – 19 jul 2026",
        acceso="Gratuito", registro=False, vip=False,
        capacidad_est=50_000,
        highlights="'El Mundo en una Ciudad' · Conciertos diarios · Diversidad multicultural",
        restricciones="Sin mochilas grandes ni equipaje de mano grande",
        lat=43.6386, lon=-79.4014,
        csv_aliases=["Toronto"],
    ),
    dict(
        ciudad="Vancouver", pais="Canadá", flag="🇨🇦",
        ubicacion="PNE Grounds · Hastings Park",
        fechas="11 jun – 19 jul 2026",
        acceso="Gratuito + Hospitalidad Premium de pago", registro=False, vip=True,
        capacidad_est=45_000,
        highlights="Freedom Mobile Amphitheatre · Vista a montañas · Food trucks internacionales",
        restricciones="Zonas Premium/VIP con ticket adicional",
        lat=49.2827, lon=-123.1207,
        csv_aliases=["Vancouver"],
    ),
    dict(
        ciudad="Atlanta", pais="EE.UU.", flag="🇺🇸",
        ubicacion="Centennial Olympic Park",
        fechas="11 jun – 19 jul 2026",
        acceso="GA Gratuito + Zona GA+ mejorada", registro=False, vip=True,
        capacidad_est=70_000,
        highlights="Summer Walker · Ludacris · CeeLo Green · EARTHGANG",
        restricciones="GA+ requiere acceso diferenciado · Política de bolsas estándar FIFA",
        lat=33.7595, lon=-84.3921,
        csv_aliases=["Atlanta"],
    ),
    dict(
        ciudad="Boston", pais="EE.UU.", flag="🇺🇸",
        ubicacion="City Hall Plaza",
        fechas="16 días (días de partido asignados)",
        acceso="Gratuito", registro=False, vip=False,
        capacidad_est=35_000,
        highlights="Acceso MBTA · Ambiente comunitario local · Orientado al fan local",
        restricciones="Activo exclusivamente en días de partido programados",
        lat=42.3601, lon=-71.0589,
        csv_aliases=["Boston", "Foxborough", "Foxboro"],
    ),
    dict(
        ciudad="Houston", pais="EE.UU.", flag="🇺🇸",
        ubicacion="EaDo · East Downtown",
        fechas="11 jun – 19 jul 2026",
        acceso="Gratuito", registro=False, vip=False,
        capacidad_est=60_000,
        highlights="Football Fiesta Houston · Música latina · Torneos Fútbol 5 · Fusión tejano-mexicana",
        restricciones="Protocolo estándar FIFA de seguridad",
        lat=29.7604, lon=-95.3595,
        csv_aliases=["Houston"],
    ),
    dict(
        ciudad="Kansas City", pais="EE.UU.", flag="🇺🇸",
        ubicacion="National WWI Museum and Memorial",
        fechas="18 días seleccionados del torneo",
        acceso="Gratuito · Requiere registro digital previo", registro=True, vip=False,
        capacidad_est=30_000,
        highlights="Vista panorámica al skyline KC · Pantalla gigante · Activaciones patrocinadores",
        restricciones="Registro digital obligatorio · Regulaciones estrictas del memorial · Aforo controlado",
        lat=39.0997, lon=-94.5786,
        csv_aliases=["Kansas City"],
    ),
    dict(
        ciudad="Los Ángeles", pais="EE.UU.", flag="🇺🇸",
        ubicacion="LA Memorial Coliseum + Fan Zones satélite",
        fechas="11–15 jun centralizado · luego distribución metropolitana",
        acceso="Gratuito", registro=False, vip=False,
        capacidad_est=100_000,
        highlights="Semana inaugural centralizada · Zonas satélite costeras y plazas urbanas",
        restricciones="Post-15 jun: múltiples ubicaciones — verificar cada zona satélite",
        lat=34.0141, lon=-118.2879,
        csv_aliases=["Los Angeles", "Pasadena"],
    ),
    dict(
        ciudad="Miami", pais="EE.UU.", flag="🇺🇸",
        ubicacion="Bayfront Park · Downtown Miami",
        fechas="13 jun – 5 jul 2026",
        acceso="Gratuito · Sin registro", registro=False, vip=False,
        capacidad_est=30_000,
        highlights="Frente al mar · Música urbana, caribeña y electrónica · ~30K personas/día",
        restricciones="Sin pase previo requerido · Acceso directo",
        lat=25.7743, lon=-80.1870,
        csv_aliases=["Miami", "Miami Gardens"],
    ),
    dict(
        ciudad="Filadelfia", pais="EE.UU.", flag="🇺🇸",
        ubicacion="Lemon Hill · Fairmount Park",
        fechas="11 jun – 19 jul 2026",
        acceso="GA Gratuito · Conciertos sin partido con ticket", registro=False, vip=True,
        capacidad_est=50_000,
        highlights="Acceso general gratuito en días de partido · Festivales de música adicionales",
        restricciones="Días sin partido: eventos de pago con ticket independiente",
        lat=39.9526, lon=-75.1652,
        csv_aliases=["Philadelphia"],
    ),
    dict(
        ciudad="Nueva York", pais="EE.UU.", flag="🇺🇸",
        ubicacion="Queens · Manhattan · Bronx · Brooklyn · Staten Island",
        fechas="11 jun – 19 jul 2026 (rotación por fase)",
        acceso="Gratuito", registro=False, vip=False,
        capacidad_est=80_000,
        highlights="USTA Queens (grupos) · Rockefeller Center (eliminatorias/final) · Brooklyn Bridge Park",
        restricciones="Formato satélite: zona activa varía por fase del torneo",
        lat=40.7128, lon=-74.0060,
        csv_aliases=["New York/New Jersey"],
    ),
]

PAIS_COLOR = {
    "México": COLOR_LIME,
    "Canadá": "#FF4040",
    "EE.UU.": COLOR_BLUE,
}

PAIS_SYMBOL = {
    "México": "circle",
    "Canadá": "diamond",
    "EE.UU.": "star",
}


def _hex_alpha(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _city_history(info: dict) -> dict:
    if df_raw.empty:
        return {}
    sub = df_raw[df_raw["city"].isin(info["csv_aliases"])].dropna(subset=["attendance"])
    if sub.empty:
        return {}
    return {
        "avg":   float(sub["attendance"].mean()),
        "max":   float(sub["attendance"].max()),
        "count": int(len(sub)),
        "years": sorted(sub["year"].dropna().unique().astype(int).tolist()),
    }


@solara.component
def Tab6_Festivales(df: pd.DataFrame):
    selected_city,  set_selected_city  = solara.use_state("Ciudad de México")
    filter_country, set_filter_country = solara.use_state("Todos")

    city_lookup = {f["ciudad"]: f for f in FESTIVALS}
    sel  = city_lookup.get(selected_city, FESTIVALS[0])
    hist = _city_history(sel)
    pais_color = PAIS_COLOR.get(sel["pais"], COLOR_LIME)

    solara.HTML("div", unsafe_innerHTML=f"""
        <div style="background:linear-gradient(120deg,rgba(8,14,26,.96),rgba(0,25,55,.90));
            border:1px solid {COLOR_LIME}30;border-left:4px solid {COLOR_LIME};
            border-radius:14px;padding:24px 32px;margin-bottom:20px;
            position:relative;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,.55);">
            <div style="position:absolute;right:28px;top:14px;font-size:3rem;opacity:.10;
                pointer-events:none;">🗺️</div>
            <p style="font-size:.62rem;font-weight:700;text-transform:uppercase;
                letter-spacing:2.5px;color:{COLOR_LIME};margin:0 0 6px;">
                Análisis Prospectivo · FIFA World Cup 2026</p>
            <h2 style="font-size:1.4rem;font-weight:900;color:{COLOR_WHITE};margin:0 0 8px;">
                La Oportunidad Presencial 2026</h2>
            <p style="color:{COLOR_MUTED};font-size:.82rem;line-height:1.8;margin:0 0 14px;
                max-width:720px;">
                13 puntos de concentración masiva de fans en Norteamérica. El análisis histórico
                identifica la <b style="color:{COLOR_LIME};">demanda comprobada</b> por ciudad —
                la base cuantitativa sobre la que se construye la oportunidad comercial del
                <b style="color:{COLOR_WHITE};">Mundial más grande de la historia.</b>
            </p>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
                <span style="background:{COLOR_LIME}18;border:1px solid {COLOR_LIME}45;
                    color:{COLOR_LIME};border-radius:20px;padding:3px 12px;font-size:.66rem;
                    font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                    🗺️ 13 Fan Festivals</span>
                <span style="background:{COLOR_LIME}10;border:1px solid {COLOR_LIME}30;
                    color:{COLOR_LIME}CC;border-radius:20px;padding:3px 12px;font-size:.66rem;
                    font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                    🇲🇽 3 México</span>
                <span style="background:rgba(255,64,64,.10);border:1px solid rgba(255,64,64,.30);
                    color:#FF8080;border-radius:20px;padding:3px 12px;font-size:.66rem;
                    font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                    🇨🇦 2 Canadá</span>
                <span style="background:{COLOR_BLUE}18;border:1px solid {COLOR_BLUE}45;
                    color:#6AB0E8;border-radius:20px;padding:3px 12px;font-size:.66rem;
                    font-weight:700;text-transform:uppercase;letter-spacing:.8px;">
                    🇺🇸 8 EE.UU.</span>
            </div>
        </div>
    """)

    def handle_country(v):
        set_filter_country(v)
        if v != "Todos":
            current_pais = city_lookup.get(selected_city, {}).get("pais")
            if current_pais != v:
                first = next((f["ciudad"] for f in FESTIVALS if f["pais"] == v), None)
                if first:
                    set_selected_city(first)

    with solara.Columns([3, 1]):
        with solara.Column():
            solara.ToggleButtonsSingle(
                value=filter_country,
                values=["Todos", "México", "Canadá", "EE.UU."],
                on_value=handle_country,
            )
        with solara.Column():
            solara.Select(
                label="🏙 Ciudad",
                value=selected_city,
                values=[f["ciudad"] for f in FESTIVALS],
                on_value=set_selected_city,
            )

    visible = [
        f for f in FESTIVALS
        if filter_country == "Todos" or f["pais"] == filter_country
    ]

    fig_map = go.Figure()
    for pais, color, symbol in [
        ("México", COLOR_LIME,  "circle"),
        ("Canadá", "#FF4040",   "diamond"),
        ("EE.UU.", COLOR_BLUE,  "star"),
    ]:
        group = [f for f in visible if f["pais"] == pais]
        if not group:
            continue
        is_sel = [f["ciudad"] == selected_city for f in group]
        fig_map.add_trace(go.Scattergeo(
            lon=[f["lon"] for f in group],
            lat=[f["lat"] for f in group],
            mode="markers+text",
            name=f"{group[0]['flag']} {pais}",
            marker=dict(
                symbol=symbol,
                size=[20 if s else 13 for s in is_sel],
                color=[color] * len(group),
                line=dict(
                    color=[COLOR_WHITE if s else "rgba(255,255,255,0.25)" for s in is_sel],
                    width=[2.5 if s else 0.8 for s in is_sel],
                ),
            ),
            text=[f["ciudad"] for f in group],
            textposition="top center",
            textfont=dict(
                size=[11 if s else 9 for s in is_sel],
                color=[COLOR_WHITE if s else COLOR_MUTED for s in is_sel],
                family="Inter, sans-serif",
            ),
            customdata=[f["ciudad"] for f in group],
            hovertemplate=(
                "<b>%{customdata}</b><br>"
                "Haz clic para explorar<extra></extra>"
            ),
        ))

    fig_map.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=10, b=10, l=0, r=0)},
        geo=dict(
            scope="north america",
            bgcolor="rgba(0,0,0,0)",
            landcolor="#0D1B2E",
            oceancolor="#050B14",
            showocean=True,
            lakecolor="#050B14",
            showlakes=True,
            countrycolor="#1D2E4A",
            showcountries=True,
            showcoastlines=True,
            coastlinecolor="#1D3050",
            projection_type="natural earth",
            lonaxis=dict(range=[-142, -58]),
            lataxis=dict(range=[14, 63]),
        ),
        height=400,
        showlegend=True,
        legend=dict(
            bgcolor="rgba(13,19,33,0.85)",
            bordercolor="rgba(205,255,0,0.15)",
            borderwidth=1,
            font=dict(color=COLOR_TEXT, size=10),
            x=0.01, y=0.99, xanchor="left", yanchor="top",
        ),
    )

    def on_map_click(click_data):
        try:
            pts = click_data.get("points", []) if isinstance(click_data, dict) else []
            if pts:
                city = pts[0].get("customdata")
                if city and city in city_lookup:
                    set_selected_city(city)
        except Exception:
            pass

    solara.FigurePlotly(fig_map, on_click=on_map_click)

    reg_tag = "· 📋 Registro requerido" if sel.get("registro") else "· ✅ Acceso libre"
    vip_tag = " · 💎 Zona VIP disponible" if sel.get("vip") else ""
    InsightBox(
        f"🗺️ Haz clic en un punto del mapa o usa el selector para explorar cada ciudad. "
        f"Seleccionada: <b style='color:{COLOR_LIME};'>{selected_city}</b> "
        f"<span style='color:{COLOR_MUTED};'>{reg_tag}{vip_tag}</span>",
        "lime",
    )

    reg_badge = (
        f"<span style='background:rgba(232,0,45,.15);border:1px solid {COLOR_RED}50;"
        f"color:{COLOR_RED};border-radius:12px;padding:2px 10px;font-size:.62rem;"
        f"font-weight:700;letter-spacing:.5px;'>📋 Registro requerido</span>"
        if sel.get("registro") else
        f"<span style='background:{COLOR_LIME}12;border:1px solid {COLOR_LIME}40;"
        f"color:{COLOR_LIME};border-radius:12px;padding:2px 10px;font-size:.62rem;"
        f"font-weight:700;letter-spacing:.5px;'>✅ Acceso libre</span>"
    )
    vip_badge = (
        f"<span style='background:rgba(255,215,0,.10);border:1px solid rgba(255,215,0,.35);"
        f"color:#FFD700;border-radius:12px;padding:2px 10px;font-size:.62rem;"
        f"font-weight:700;letter-spacing:.5px;'>💎 Zona VIP</span>"
        if sel.get("vip") else ""
    )

    with solara.Columns([1, 1]):
        with solara.Column():
            QBlock("01", f"{sel['flag']} Fan Festival · {sel['pais']}",
                   sel["ciudad"], sel["ubicacion"], "lime")
            solara.HTML("div", unsafe_innerHTML=f"""
                <div style="background:{COLOR_STEEL};border:1px solid {pais_color}22;
                    border-radius:12px;padding:20px 22px;margin-bottom:12px;
                    position:relative;overflow:hidden;">
                    <div style="position:absolute;top:12px;right:16px;font-size:3rem;
                        line-height:1;pointer-events:none;">{sel['flag']}</div>

                    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px;">
                        {reg_badge}
                        {vip_badge}
                    </div>

                    <div style="display:grid;grid-template-columns:1fr 1fr;
                        gap:14px 20px;margin-bottom:18px;">
                        <div>
                            <p style="font-size:.58rem;text-transform:uppercase;
                                letter-spacing:1.5px;color:{COLOR_MUTED};margin:0 0 4px;">
                                📅 Fechas operativas</p>
                            <p style="font-size:.80rem;color:{COLOR_TEXT};
                                margin:0;font-weight:600;line-height:1.5;">
                                {sel['fechas']}</p>
                        </div>
                        <div>
                            <p style="font-size:.58rem;text-transform:uppercase;
                                letter-spacing:1.5px;color:{COLOR_MUTED};margin:0 0 4px;">
                                👥 Cap. estimada/día</p>
                            <p style="font-size:1.1rem;color:{pais_color};
                                margin:0;font-weight:900;">
                                {sel['capacidad_est'] // 1000}K</p>
                        </div>
                        <div style="grid-column:1/-1;">
                            <p style="font-size:.58rem;text-transform:uppercase;
                                letter-spacing:1.5px;color:{COLOR_MUTED};margin:0 0 4px;">
                                📍 Ubicación</p>
                            <p style="font-size:.80rem;color:{COLOR_TEXT};
                                margin:0;font-weight:600;">
                                {sel['ubicacion']}</p>
                        </div>
                    </div>

                    <div style="background:{pais_color}08;
                        border-left:3px solid {pais_color}55;
                        border-radius:0 8px 8px 0;padding:10px 14px;margin-bottom:12px;">
                        <p style="font-size:.58rem;text-transform:uppercase;
                            letter-spacing:1.5px;color:{pais_color};margin:0 0 5px;">
                            🎤 Highlights</p>
                        <p style="font-size:.80rem;color:{COLOR_TEXT};
                            margin:0;line-height:1.65;">
                            {sel['highlights']}</p>
                    </div>

                    <div style="background:rgba(232,0,45,.05);
                        border-left:3px solid {COLOR_RED}38;
                        border-radius:0 8px 8px 0;padding:10px 14px;">
                        <p style="font-size:.58rem;text-transform:uppercase;
                            letter-spacing:1.5px;color:{COLOR_RED};margin:0 0 5px;">
                            ⚠️ Restricciones de acceso</p>
                        <p style="font-size:.78rem;color:{COLOR_MUTED};
                            margin:0;line-height:1.65;">
                            {sel['restricciones']}</p>
                    </div>
                </div>
            """)

        with solara.Column():
            if hist:
                years_str = (
                    f"{hist['years'][0]}" if len(hist["years"]) == 1
                    else f"{hist['years'][0]}–{hist['years'][-1]}"
                )
                QBlock("02", "📊 Demanda Histórica Comprobada",
                       f"Legado mundialista de {sel['ciudad']}",
                       f"{hist['count']} partidos FIFA · ediciones {years_str}", "blue")

                solara.HTML("div", unsafe_innerHTML=f"""
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
                        gap:10px;margin-bottom:14px;">
                        <div style="background:{COLOR_STEEL};border:1px solid {COLOR_BLUE}35;
                            border-radius:10px;padding:14px;text-align:center;">
                            <p style="font-size:1.4rem;font-weight:900;color:{COLOR_BLUE};
                                margin:0;line-height:1;">{hist['avg'] / 1000:.0f}K</p>
                            <p style="font-size:.58rem;color:{COLOR_MUTED};margin:5px 0 0;
                                text-transform:uppercase;letter-spacing:1px;">Prom. histór.</p>
                        </div>
                        <div style="background:{COLOR_STEEL};border:1px solid {COLOR_LIME}35;
                            border-radius:10px;padding:14px;text-align:center;">
                            <p style="font-size:1.4rem;font-weight:900;color:{COLOR_LIME};
                                margin:0;line-height:1;">{hist['max'] / 1000:.0f}K</p>
                            <p style="font-size:.58rem;color:{COLOR_MUTED};margin:5px 0 0;
                                text-transform:uppercase;letter-spacing:1px;">Pico histórico</p>
                        </div>
                        <div style="background:{COLOR_STEEL};
                            border:1px solid rgba(248,250,252,.12);
                            border-radius:10px;padding:14px;text-align:center;">
                            <p style="font-size:1.4rem;font-weight:900;color:{COLOR_WHITE};
                                margin:0;line-height:1;">{hist['count']}</p>
                            <p style="font-size:.58rem;color:{COLOR_MUTED};margin:5px 0 0;
                                text-transform:uppercase;letter-spacing:1px;">Partidos FIFA</p>
                        </div>
                    </div>
                """)

                city_yr = (
                    df_raw[df_raw["city"].isin(sel["csv_aliases"])]
                    .dropna(subset=["attendance"])
                    .groupby("year")["attendance"]
                    .mean()
                    .reset_index()
                    .sort_values("year")
                )

                if not city_yr.empty:
                    n_cit = len(city_yr)
                    att_vals = city_yr["attendance"].tolist()
                    att_colors = [
                        f"rgba({int(21 + (205-21)*v/max(max(att_vals)-min(att_vals),1))},"
                        f"{int(101 + (255-101)*v/max(max(att_vals)-min(att_vals),1))},"
                        f"{int(192 + (0-192)*v/max(max(att_vals)-min(att_vals),1))},0.88)"
                        for v in [a - min(att_vals) for a in att_vals]
                    ]

                    def _cit_bar(sub, cols):
                        return go.Bar(
                            x=sub["year"].astype(str).tolist(),
                            y=sub["attendance"].tolist(),
                            marker=dict(
                                color=cols,
                                line=dict(color=COLOR_NAVY, width=0.5),
                            ),
                            hovertemplate=(
                                "<b>%{x}</b><br>Afluencia promedio: "
                                "%{y:,.0f}<extra></extra>"
                            ),
                        )

                    fig_cit = go.Figure(_cit_bar(city_yr.iloc[:1], [att_colors[0]]))
                    fig_cit.frames = [
                        go.Frame(
                            data=[_cit_bar(city_yr.iloc[:i+1], att_colors[:i+1])],
                            traces=[0],
                            name=str(i+1),
                        )
                        for i in range(n_cit)
                    ]
                    fig_cit.update_layout(
                        **{**BASE_LAYOUT, "margin": dict(t=8, b=50, l=15, r=10)},
                        xaxis=dict(
                            title="",
                            tickfont=dict(size=9, color=COLOR_MUTED),
                            categoryarray=city_yr["year"].astype(str).tolist(),
                            categoryorder="array",
                        ),
                        yaxis=dict(
                            title="Espectadores",
                            showgrid=True, gridcolor="#1C2840",
                            tickformat=",", tickfont=dict(size=9, color=COLOR_MUTED),
                            range=[0, max(att_vals) * 1.2],
                        ),
                        height=240, showlegend=False,
                        updatemenus=[play_menu(duration=320, y=-0.20)],
                    )
                    plotly_iframe(fig_cit, height=240)

                cap = sel["capacidad_est"]
                ratio = cap / hist["avg"] if hist["avg"] > 0 else 0
                if ratio > 1.5:
                    insight = (
                        f"🚀 <b>Amplificación x{ratio:.1f}:</b> La capacidad estimada del Festival "
                        f"<b>({cap // 1000}K)</b> supera el promedio histórico de afluencia en estadio "
                        f"<b>({hist['avg'] / 1000:.0f}K)</b> — la escala de impacto es masivamente mayor."
                    )
                else:
                    insight = (
                        f"🏟️ <b>Demanda validada:</b> {sel['ciudad']} registró hasta "
                        f"<b>{hist['max'] / 1000:.0f}K</b> espectadores por partido en el Mundial — "
                        f"la base de fans está comprobada históricamente."
                    )
                InsightBox(insight, "blue")

            else:
                QBlock("02", "🆕 Mercado Virgen 2026",
                       "Primera vez sede mundialista",
                       f"{sel['ciudad']} debuta en FIFA · sin benchmark histórico en el dataset",
                       "red")
                solara.HTML("div", unsafe_innerHTML=f"""
                    <div style="background:{COLOR_STEEL};border:1px solid {COLOR_RED}22;
                        border-radius:12px;padding:28px 24px;text-align:center;
                        margin-bottom:12px;">
                        <div style="font-size:3rem;margin-bottom:14px;opacity:.65;">🆕</div>
                        <p style="color:{COLOR_WHITE};font-size:.95rem;font-weight:800;
                            margin:0 0 10px;">Sin historial FIFA previo</p>
                        <p style="color:{COLOR_MUTED};font-size:.78rem;
                            line-height:1.75;margin:0;">
                            {sel['ciudad']} debuta como sede en 2026.<br>
                            <b style="color:{COLOR_LIME};">Sin benchmark histórico
                            = sin competencia de referencia.</b><br>
                            Mercado virgen con afición local sin cuantificar.
                        </p>
                    </div>
                """)
                InsightBox(
                    f"💡 <b>Ventaja de primer movedor:</b> Sin referencias FIFA previas, "
                    f"<b>{sel['ciudad']}</b> representa un mercado de captura pura. "
                    f"La capacidad estimada de <b>{sel['capacidad_est'] // 1000}K personas/día</b> "
                    f"establece el nuevo benchmark desde cero.",
                    "red",
                )

    QBlock(
        "03",
        "📊 Benchmark Integral · Demanda Histórica vs Capacidad 2026",
        "¿Qué ciudades tienen mayor potencial de activación?",
        "Afluencia FIFA histórica (barras) vs capacidad estimada Fan Festival 2026 (marcador) · por ciudad",
        "lime",
    )

    comp_rows = []
    for f in FESTIVALS:
        h = _city_history(f)
        comp_rows.append({
            "ciudad":    f["ciudad"],
            "label":     f"{f['flag']} {f['ciudad']}",
            "pais":      f["pais"],
            "hist_avg":  h.get("avg", 0),
            "cap_est":   f["capacidad_est"],
            "has_hist":  bool(h),
        })
    comp_df = pd.DataFrame(comp_rows).sort_values("hist_avg", ascending=True)

    hist_df  = comp_df[comp_df["hist_avg"] > 0].reset_index(drop=True)
    n_comp   = len(hist_df)
    all_cities = comp_df["label"].tolist()

    bar_colors = [
        _hex_alpha(PAIS_COLOR.get(p, COLOR_MUTED), 0.60)
        for p in hist_df["pais"]
    ]

    def _comp_bar(sub, cols):
        return go.Bar(
            y=sub["label"].tolist(),
            x=sub["hist_avg"].tolist(),
            orientation="h",
            name="Afluencia histórica (promedio FIFA)",
            marker=dict(
                color=cols,
                line=dict(color=COLOR_NAVY, width=0.5),
            ),
            hovertemplate="<b>%{y}</b><br>Prom. histórico: %{x:,.0f} esp.<extra></extra>",
        )

    # Traza 0 animada, inicia con primera ciudad / Trace 0: animated bar, starts with first city
    # Traza 1 estática con marcadores de capacidad / Trace 1: static capacity markers, all cities
    if n_comp > 0:
        fig_comp = go.Figure(_comp_bar(hist_df.iloc[:1], [bar_colors[0]]))
    else:
        fig_comp = go.Figure()

    fig_comp.add_trace(go.Scatter(
        y=comp_df["label"].tolist(),
        x=comp_df["cap_est"].tolist(),
        mode="markers",
        name="Capacidad estimada Festival 2026",
        marker=dict(
            symbol="line-ew",
            size=16,
            color=COLOR_LIME,
            line=dict(color=COLOR_LIME, width=3),
        ),
        hovertemplate="<b>%{y}</b><br>Cap. Festival 2026: %{x:,.0f} est.<extra></extra>",
    ))

    if n_comp > 0:
        fig_comp.frames = [
            go.Frame(
                data=[_comp_bar(hist_df.iloc[:i+1], bar_colors[:i+1])],
                traces=[0],
                name=str(i+1),
            )
            for i in range(n_comp)
        ]

    fig_comp.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=20, b=55, l=10, r=10)},
        xaxis=dict(
            title="Espectadores",
            showgrid=True, gridcolor="#1C2840",
            tickformat=",", tickfont=dict(size=9, color=COLOR_MUTED),
            range=[0, max(comp_df["cap_est"].max(), hist_df["hist_avg"].max()
                          if n_comp > 0 else 0) * 1.15],
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=9, color=COLOR_TEXT),
            categoryarray=all_cities,
            categoryorder="array",
            range=[-0.5, len(all_cities) - 0.5],
        ),
        height=530,
        legend=dict(
            bgcolor="rgba(13,19,33,0.85)",
            bordercolor="rgba(205,255,0,0.15)",
            borderwidth=1,
            font=dict(color=COLOR_TEXT, size=10),
            x=0.50, y=0.02, xanchor="left", yanchor="bottom",
        ),
        barmode="overlay",
        updatemenus=[play_menu(duration=260, y=-0.10)],
    )
    plotly_iframe(fig_comp, height=530)

    n_hist   = int(comp_df["has_hist"].sum())
    n_virgin = len(FESTIVALS) - n_hist
    InsightBox(
        f"📊 <b>{n_hist} ciudades</b> tienen demanda FIFA comprobada — benchmarks sólidos "
        f"para proyecciones. Las <b>{n_virgin} ciudades sin historial</b> "
        f"(principalmente Canadá y nuevas sedes de EE.UU.) representan mercados vírgenes: "
        f"mayor incertidumbre pero también <b style='color:{COLOR_LIME};'>mayor oportunidad "
        f"de captura sin competencia establecida.</b>",
        "lime",
    )

    QBlock(
        "04",
        "🎟️ Fricción de Acceso · Oportunidades de Monetización",
        "¿Cuánto esfuerzo necesita el fan para asistir?",
        "Registro previo, zonas VIP y tipo de acceso por ciudad · indicadores de fricción y captación",
        "blue",
    )

    rows_html = ""
    for f in FESTIVALS:
        reg_icon  = "📋 Sí" if f.get("registro") else "✅ No"
        reg_color = COLOR_RED if f.get("registro") else COLOR_LIME
        vip_icon  = "💎 Sí" if f.get("vip") else "—"
        vip_color = "#FFD700" if f.get("vip") else COLOR_MUTED
        cap_str   = f"{f['capacidad_est'] // 1000}K"
        p_color   = PAIS_COLOR.get(f["pais"], COLOR_MUTED)
        acceso_short = f["acceso"][:52] + ("…" if len(f["acceso"]) > 52 else "")
        rows_html += f"""
            <tr style="border-bottom:1px solid rgba(255,255,255,.04);">
                <td style="padding:9px 12px;font-weight:700;
                    color:{COLOR_TEXT};font-size:.78rem;">
                    {f['flag']} {f['ciudad']}</td>
                <td style="padding:9px 12px;color:{p_color};
                    font-size:.72rem;font-weight:600;">{f['pais']}</td>
                <td style="padding:9px 12px;color:{reg_color};
                    font-size:.72rem;font-weight:700;">{reg_icon}</td>
                <td style="padding:9px 12px;color:{vip_color};
                    font-size:.72rem;font-weight:700;">{vip_icon}</td>
                <td style="padding:9px 12px;color:{COLOR_LIME};
                    font-size:.78rem;font-weight:800;text-align:right;">
                    {cap_str}</td>
                <td style="padding:9px 12px;color:{COLOR_MUTED};
                    font-size:.70rem;">{acceso_short}</td>
            </tr>
        """

    solara.HTML("div", unsafe_innerHTML=f"""
        <div style="overflow-x:auto;border-radius:10px;
            border:1px solid {COLOR_LIME}15;margin-bottom:12px;">
            <table style="width:100%;border-collapse:collapse;
                background:{COLOR_STEEL};border-radius:10px;">
                <thead>
                    <tr style="background:{COLOR_NAVY};">
                        <th style="padding:10px 12px;text-align:left;color:{COLOR_LIME};
                            font-size:.60rem;text-transform:uppercase;letter-spacing:1.5px;">
                            Ciudad</th>
                        <th style="padding:10px 12px;text-align:left;color:{COLOR_LIME};
                            font-size:.60rem;text-transform:uppercase;letter-spacing:1.5px;">
                            País</th>
                        <th style="padding:10px 12px;text-align:left;color:{COLOR_LIME};
                            font-size:.60rem;text-transform:uppercase;letter-spacing:1.5px;">
                            Registro</th>
                        <th style="padding:10px 12px;text-align:left;color:{COLOR_LIME};
                            font-size:.60rem;text-transform:uppercase;letter-spacing:1.5px;">
                            Zona VIP</th>
                        <th style="padding:10px 12px;text-align:right;color:{COLOR_LIME};
                            font-size:.60rem;text-transform:uppercase;letter-spacing:1.5px;">
                            Cap. /día</th>
                        <th style="padding:10px 12px;text-align:left;color:{COLOR_LIME};
                            font-size:.60rem;text-transform:uppercase;letter-spacing:1.5px;">
                            Tipo de acceso</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
    """)

    n_reg = sum(1 for f in FESTIVALS if f.get("registro"))
    n_vip = sum(1 for f in FESTIVALS if f.get("vip"))
    InsightBox(
        f"💡 Solo <b>{n_reg} de 13 ciudades</b> (Guadalajara y Kansas City) requieren registro "
        f"previo — fricción de entrada muy baja en el 85% de los festivales. "
        f"Las <b>{n_vip} ciudades con Zona VIP</b> (Atlanta, Monterrey, Vancouver, Filadelfia) "
        f"concentran el mayor potencial de <b>monetización premium directa.</b>",
        "blue",
    )
