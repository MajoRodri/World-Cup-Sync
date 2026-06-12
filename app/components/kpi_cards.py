# Tarjeta KPI con pulso de color / KPI card with color-pulse animation

import solara
from app.constants import (
    COLOR_LIME, COLOR_RED, COLOR_BLUE, COLOR_WHITE,
    COLOR_NAVY, COLOR_STEEL, COLOR_MUTED,
)


@solara.component
def KPICard(icon: str, label: str, value: str, sub: str, color: str = COLOR_LIME):
    pulse_class = {
        COLOR_LIME:  "wcs-kpi-lime",
        COLOR_RED:   "wcs-kpi-red",
        COLOR_BLUE:  "wcs-kpi-blue",
        COLOR_WHITE: "wcs-kpi-white",
    }.get(color, "wcs-kpi-lime")
    solara.HTML("div", unsafe_innerHTML=f"""
        <div class="wcs-kpi {pulse_class}"
            style="background:linear-gradient(145deg,{COLOR_STEEL} 0%,#1B2A42 100%);
            border:1px solid rgba(255,255,255,.06);border-top:3px solid {color};
            border-radius:12px;padding:16px 18px 14px;text-align:center;
            min-height:110px;display:flex;flex-direction:column;
            justify-content:space-around;margin-bottom:8px;cursor:default;
            position:relative;overflow:hidden;">
            <div style="position:absolute;top:-8px;right:-8px;font-size:3rem;
                opacity:.05;pointer-events:none;">{icon}</div>
            <div style="font-size:.59rem;color:{color};font-weight:700;
                text-transform:uppercase;letter-spacing:1.5px;">{icon} {label}</div>
            <div style="font-size:1.85rem;font-weight:900;color:{COLOR_WHITE};
                line-height:1.05;">{value}</div>
            <div style="font-size:.59rem;color:{COLOR_MUTED};letter-spacing:.3px;
                overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{sub}</div>
        </div>
    """)
