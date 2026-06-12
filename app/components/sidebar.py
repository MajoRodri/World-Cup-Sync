# Sidebar con filtros de año, fase y equipo / Sidebar with year, phase, and team filters

import solara
from app.constants import (
    COLOR_LIME, COLOR_BLUE, COLOR_RED,
    COLOR_MUTED, COLOR_WHITE, COLOR_NAVY,
)


@solara.component
def AppSidebar(
    year_range: tuple,
    set_year_range,
    selected_stages: list,
    set_selected_stages,
    selected_team: str,
    set_selected_team,
    n_editions: int,
    stages_all: list,
    teams_all: list,
    years_available: list,
):
    yr0, yr1 = year_range

    with solara.Sidebar():
        solara.HTML("div", unsafe_innerHTML=f"""
            <div style="padding:20px 10px 12px;text-align:center;position:relative;">
                <div style="font-size:2.2rem;animation:float-trophy 4s ease-in-out infinite;
                    display:inline-block;margin-bottom:4px;">🏆</div>
                <h2 style="color:{COLOR_LIME};font-size:1.05rem;font-weight:900;
                    letter-spacing:3px;margin:0;animation:logo-glow 3s ease-in-out infinite;">
                    WORLD CUP</h2>
                <p style="color:{COLOR_MUTED};font-size:.60rem;letter-spacing:2px;
                    text-transform:uppercase;margin:2px 0 0;">SYNC ANALYTICS</p>
                <div style="margin-top:10px;display:flex;justify-content:center;gap:6px;">
                    <span style="font-size:1.1rem;animation:float-ball 5s ease-in-out infinite;">⚽</span>
                    <span style="font-size:1.1rem;animation:float-ball2 6s ease-in-out infinite 1s;">⚽</span>
                    <span style="font-size:1.1rem;animation:float-ball 4.5s ease-in-out infinite 2s;">⚽</span>
                </div>
            </div>
            <hr style="border:none;border-top:1px solid {COLOR_LIME}25;margin:0 0 8px;">
            <div style="margin:8px 10px;background:{COLOR_LIME}10;border:1px solid {COLOR_LIME}30;
                border-radius:8px;padding:6px 10px;display:flex;align-items:center;gap:8px;">
                <span style="width:7px;height:7px;background:{COLOR_RED};border-radius:50%;
                    display:inline-block;animation:pulse-red 1.5s ease-in-out infinite;
                    flex-shrink:0;"></span>
                <span style="font-size:.62rem;color:{COLOR_LIME};font-weight:700;
                    letter-spacing:1px;text-transform:uppercase;">LIVE ANALYTICS</span>
            </div>
        """)

        solara.HTML("div", unsafe_innerHTML=f"""
            <p style="color:{COLOR_LIME};font-size:.68rem;font-weight:700;
                text-transform:uppercase;letter-spacing:1.5px;margin:14px 0 6px;
                padding:0 10px;">📅 Edición (Año)</p>
        """)

        def _on_yr_start(v):
            v = int(v)
            set_year_range((v, year_range[1] if year_range[1] >= v else v))

        def _on_yr_end(v):
            v = int(v)
            set_year_range((year_range[0] if year_range[0] <= v else v, v))

        yr_start_opts = years_available
        yr_end_opts   = [y for y in years_available if y >= yr0]

        with solara.Columns([1, 1]):
            with solara.Column():
                solara.Select(
                    label="",
                    values=yr_start_opts,
                    value=yr0,
                    on_value=_on_yr_start,
                )
            with solara.Column():
                solara.Select(
                    label="",
                    values=yr_end_opts,
                    value=yr1,
                    on_value=_on_yr_end,
                )

        solara.HTML("div", unsafe_innerHTML=f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                padding:8px 14px;margin:6px 10px 4px;
                background:linear-gradient(90deg,{COLOR_LIME}08,{COLOR_BLUE}06);
                border:1px solid {COLOR_LIME}20;border-radius:8px;">
                <div style="text-align:center;">
                    <div style="font-size:1.15rem;font-weight:900;color:{COLOR_LIME};
                        line-height:1;">{yr0}</div>
                    <div style="font-size:.55rem;color:{COLOR_MUTED};
                        text-transform:uppercase;letter-spacing:.8px;margin-top:1px;">desde</div>
                </div>
                <div style="color:{COLOR_MUTED};font-size:.9rem;">⚽</div>
                <div style="text-align:center;">
                    <div style="font-size:1.15rem;font-weight:900;color:{COLOR_LIME};
                        line-height:1;">{yr1}</div>
                    <div style="font-size:.55rem;color:{COLOR_MUTED};
                        text-transform:uppercase;letter-spacing:.8px;margin-top:1px;">hasta</div>
                </div>
                <div style="font-size:.68rem;color:{COLOR_MUTED};text-align:center;
                    border-left:1px solid {COLOR_LIME}18;padding-left:10px;">
                    <b style="color:{COLOR_WHITE};font-size:.8rem;">{n_editions}</b><br>
                    <span style="font-size:.55rem;">ediciones</span>
                </div>
            </div>
        """)

        solara.HTML("div", unsafe_innerHTML=f"""
            <p style="color:{COLOR_LIME};font-size:.68rem;font-weight:700;
                text-transform:uppercase;letter-spacing:1.5px;margin:10px 0 4px;
                padding:0 10px;">🏅 Fase de Torneo</p>
        """)
        solara.SelectMultiple(
            label="",
            values=selected_stages,
            all_values=stages_all,
            on_value=set_selected_stages,
        )

        solara.HTML("div", unsafe_innerHTML=f"""
            <p style="color:{COLOR_LIME};font-size:.68rem;font-weight:700;
                text-transform:uppercase;letter-spacing:1.5px;margin:14px 0 4px;
                padding:0 10px;">🌍 Equipo</p>
        """)
        solara.Select(
            label="",
            value=selected_team,
            values=["— Todos —"] + teams_all,
            on_value=set_selected_team,
        )

        solara.HTML("div", unsafe_innerHTML=f"""
            <hr style="border:none;border-top:1px solid {COLOR_LIME}15;margin:16px 10px 10px;">
            <div style="padding:0 10px;">
                <div style="font-size:.58rem;color:{COLOR_MUTED};line-height:1.9;text-align:center;">
                    FIFA · Kaggle (piterfm)<br>
                    <span style="color:{COLOR_RED};font-weight:700;">USO INTERNO — CONFIDENCIAL</span>
                </div>
            </div>
        """)
