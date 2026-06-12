# Constantes globales: colores, layout, CSS / Global constants: colors, layout, CSS

COLOR_RED   = "#E8002D"
COLOR_LIME  = "#CDFF00"
COLOR_BLUE  = "#1565C0"
COLOR_WHITE = "#F8FAFC"
COLOR_NAVY  = "#0D1321"
COLOR_STEEL = "#1D2436"
COLOR_MUTED = "#8899B0"
COLOR_TEXT  = "#C8D8E8"

PLOT_BG  = "rgba(13,19,33,0.92)"
PAPER_BG = "rgba(0,0,0,0)"

STAGE_ORDER = ["Fase de Grupos", "Eliminatorias", "Cuartos de Final", "Semifinal", "Final"]


def play_menu(duration=300, y=-0.14):
    # Controles para animaciones basadas en frames de Plotly / Controls for Plotly frame-based animations
    return dict(
        type="buttons", showactive=False, direction="left",
        x=0.0, y=y, xanchor="left", yanchor="top",
        bgcolor=COLOR_NAVY,
        bordercolor="rgba(205,255,0,0.35)",
        font=dict(color=COLOR_LIME, size=12, family="Inter, sans-serif"),
        buttons=[
            dict(label="▶",
                 method="animate",
                 args=[None, {"frame": {"duration": duration, "redraw": True},
                              "fromcurrent": True,
                              "transition": {"duration": int(duration * 0.6),
                                             "easing": "cubic-in-out"}}]),
            dict(label="⏸",
                 method="animate",
                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0}}]),
        ],
    )

BASE_LAYOUT = dict(
    paper_bgcolor=PAPER_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(color=COLOR_TEXT, family="'Segoe UI', Arial, sans-serif"),
    margin=dict(t=60, b=45, l=15, r=15),
)

APP_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

@keyframes float-ball {{
    0%,100% {{ transform: translateY(0px) rotate(0deg); opacity:.35; }}
    33%      {{ transform: translateY(-16px) rotate(120deg); opacity:.6; }}
    66%      {{ transform: translateY(-8px) rotate(240deg); opacity:.45; }}
}}
@keyframes float-ball2 {{
    0%,100% {{ transform: translateY(0px) rotate(0deg); opacity:.2; }}
    50%      {{ transform: translateY(-22px) rotate(180deg); opacity:.5; }}
}}
@keyframes float-trophy {{
    0%,100% {{ transform: translateY(0px) scale(1); opacity:.18; }}
    50%      {{ transform: translateY(-10px) scale(1.1); opacity:.35; }}
}}
@keyframes pulse-lime {{
    0%,100% {{ box-shadow: 0 0 0px {COLOR_LIME}00, 0 6px 24px rgba(0,0,0,.5); }}
    50%      {{ box-shadow: 0 0 22px {COLOR_LIME}44, 0 0 44px {COLOR_LIME}18, 0 6px 24px rgba(0,0,0,.5); }}
}}
@keyframes pulse-red {{
    0%,100% {{ box-shadow: 0 0 0px {COLOR_RED}00; }}
    50%      {{ box-shadow: 0 0 18px {COLOR_RED}40, 0 0 36px {COLOR_RED}15; }}
}}
@keyframes pulse-blue {{
    0%,100% {{ box-shadow: 0 0 0px {COLOR_BLUE}00; }}
    50%      {{ box-shadow: 0 0 18px {COLOR_BLUE}50, 0 0 36px {COLOR_BLUE}20; }}
}}
@keyframes shimmer-hero {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(250%); }}
}}
@keyframes scan-line {{
    0%   {{ top: -4px; opacity:0; }}
    5%   {{ opacity:1; }}
    95%  {{ opacity:1; }}
    100% {{ top: 100%; opacity:0; }}
}}
@keyframes fadeInUp {{
    from {{ opacity:0; transform:translateY(18px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
@keyframes fadeInLeft {{
    from {{ opacity:0; transform:translateX(-14px); }}
    to   {{ opacity:1; transform:translateX(0); }}
}}
@keyframes border-breathe {{
    0%,100% {{ border-color: {COLOR_LIME}28; }}
    50%      {{ border-color: {COLOR_LIME}65; }}
}}
@keyframes logo-glow {{
    0%,100% {{ text-shadow: 0 0 8px {COLOR_LIME}30; }}
    50%      {{ text-shadow: 0 0 22px {COLOR_LIME}90, 0 0 40px {COLOR_LIME}40; }}
}}
@keyframes bar-fill {{
    from {{ width: 0; }}
    to   {{ width: 100%; }}
}}
@keyframes wcs-tab-in {{
    0%   {{ opacity: 0; transform: translateY(18px) scale(0.985); filter: blur(5px); }}
    55%  {{ filter: blur(0px); }}
    100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }}
}}
@keyframes wcs-ball-kick {{
    0%   {{ transform: translateX(-24px) rotate(-30deg); opacity: 0; }}
    60%  {{ transform: translateX(4px) rotate(10deg); opacity: 1; }}
    80%  {{ transform: translateX(-2px) rotate(-5deg); }}
    100% {{ transform: translateX(0) rotate(0deg); opacity: 1; }}
}}

html, body {{
    overflow-y: auto !important;
    height: auto !important;
}}
body, .v-application, .v-application--wrap {{
    background: radial-gradient(ellipse at 20% 0%, #142240 0%, {COLOR_NAVY} 40%, #090F1C 100%) !important;
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif !important;
}}
.v-application--wrap {{
    min-height: 100vh !important;
    height: auto !important;
    overflow-y: auto !important;
}}
.v-navigation-drawer, .v-navigation-drawer__content {{
    background: linear-gradient(180deg, #07090F 0%, {COLOR_NAVY} 100%) !important;
    border-right: 1px solid {COLOR_LIME}22 !important;
}}
.v-main {{
    background: transparent !important;
    overflow-y: auto !important;
    height: auto !important;
}}
.v-main__wrap {{
    background: transparent !important;
    overflow-y: auto !important;
    height: auto !important;
    min-height: 100vh !important;
}}
.v-app-bar {{
    background: linear-gradient(90deg, #07090F 0%, #0D1321 100%) !important;
    border-bottom: 1px solid {COLOR_LIME}20 !important;
}}

.v-window, .v-window__container, .v-window-item {{
    background: transparent !important;
}}
.v-window-item--active {{
    animation: wcs-tab-in 0.48s cubic-bezier(0.16, 1, 0.3, 1) both !important;
}}
.v-window__container {{
    transition: none !important;
}}
.v-tabs-items {{
    overflow: visible !important;
    height: auto !important;
}}
.v-sheet, .v-sheet--outlined {{
    background: transparent !important;
    color: {COLOR_TEXT} !important;
}}
.v-card, .v-card__text, .v-card__title, .v-card__subtitle, .v-card__actions {{
    background: transparent !important;
    color: {COLOR_TEXT} !important;
}}
.v-list, .v-list-item, .v-list__tile {{
    background: transparent !important;
    color: {COLOR_TEXT} !important;
}}
.v-data-table, .v-data-table__wrapper, .v-data-table > .v-data-table__wrapper > table {{
    background: {COLOR_STEEL} !important;
    color: {COLOR_TEXT} !important;
}}
.v-data-table thead th {{
    background: {COLOR_NAVY} !important;
    color: {COLOR_LIME} !important;
    font-weight: 700 !important;
    font-size: .78rem !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid {COLOR_LIME}30 !important;
}}
.v-data-table tbody tr {{ background: transparent !important; }}
.v-data-table tbody tr:hover {{ background: rgba(205,255,0,.04) !important; }}
.v-data-table tbody td {{
    color: {COLOR_TEXT} !important;
    border-bottom: 1px solid rgba(255,255,255,.05) !important;
    font-size: .80rem !important;
}}
.v-data-footer {{
    background: {COLOR_NAVY} !important;
    color: {COLOR_MUTED} !important;
    border-top: 1px solid {COLOR_LIME}18 !important;
}}
.v-data-footer .v-icon, .v-data-footer .v-select {{
    color: {COLOR_MUTED} !important;
}}
.v-pagination .v-pagination__item, .v-pagination__navigation {{
    background: {COLOR_STEEL} !important;
    color: {COLOR_TEXT} !important;
    box-shadow: none !important;
}}
.v-pagination .v-pagination__item--active {{
    background: {COLOR_LIME} !important;
    color: {COLOR_NAVY} !important;
}}
.v-input input, .v-input textarea {{
    color: {COLOR_TEXT} !important;
    caret-color: {COLOR_LIME} !important;
}}
.v-label {{ color: {COLOR_MUTED} !important; }}
.v-messages {{ color: {COLOR_MUTED} !important; }}
.v-input__slot::before {{ border-color: {COLOR_LIME}30 !important; }}
.v-input__slot::after {{ border-color: {COLOR_LIME} !important; }}
.v-icon {{ color: inherit !important; }}
.v-text-field .v-input__slot {{
    background: rgba(29,36,54,.9) !important;
    border-radius: 8px !important;
}}
.theme--light.v-application, .theme--light .v-main {{
    background: transparent !important;
    color: {COLOR_TEXT} !important;
}}
.theme--light.v-card {{ background: transparent !important; color: {COLOR_TEXT} !important; }}
.theme--light.v-data-table {{ background: {COLOR_STEEL} !important; color: {COLOR_TEXT} !important; }}
.theme--light.v-list {{ background: transparent !important; color: {COLOR_TEXT} !important; }}

.v-tab {{
    color: {COLOR_MUTED} !important;
    font-weight: 600 !important;
    font-size: .84rem !important;
    transition: color .2s ease, background .2s ease, transform .15s ease !important;
    position: relative !important;
}}
.v-tab--active {{
    color: {COLOR_LIME} !important;
    animation: wcs-ball-kick 0.4s cubic-bezier(0.22, 0.61, 0.36, 1) both !important;
}}
.v-tab:hover {{
    color: {COLOR_WHITE} !important;
    background: rgba(205,255,0,.06) !important;
    transform: translateY(-1px) !important;
}}
.v-tabs-bar {{ background: rgba(29,36,54,0.7) !important; border-radius:10px !important; }}
.v-tabs-slider {{
    background: linear-gradient(90deg, {COLOR_BLUE}88, {COLOR_LIME}) !important;
    height: 3px !important;
    border-radius: 2px 2px 0 0 !important;
    transition: left .3s cubic-bezier(0.22, 0.61, 0.36, 1) !important;
}}
.v-slider__track-fill {{ background: linear-gradient(90deg, {COLOR_BLUE}, {COLOR_LIME}) !important; height:4px !important; border-radius:2px !important; }}
.v-slider__track-background {{ background: rgba(255,255,255,.10) !important; height:4px !important; border-radius:2px !important; }}
.v-slider__thumb {{
    background: transparent !important;
    border-color: transparent !important;
    box-shadow: none !important;
    overflow: visible !important;
    z-index: 2 !important;
    transition: transform .15s ease !important;
}}
.v-slider__thumb-container {{ overflow: visible !important; }}
.v-slider__thumb::after {{
    content: '⚽';
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.5rem;
    line-height: 1;
    display: block;
    pointer-events: none;
    filter: drop-shadow(0 2px 6px rgba(0,0,0,.7));
}}
.v-slider__thumb-container--active .v-slider__thumb {{
    transform: scale(1.2) !important;
}}
.v-slider__thumb-container--active .v-slider__thumb::after {{
    filter: drop-shadow(0 0 10px {COLOR_LIME}80) !important;
}}
.v-select .v-input__slot {{ background: rgba(29,36,54,.9) !important; border:1px solid rgba(205,255,0,.18) !important; border-radius:8px !important; }}
::-webkit-scrollbar {{ width:6px; height:6px; }}
::-webkit-scrollbar-track {{ background:{COLOR_NAVY}; }}
::-webkit-scrollbar-thumb {{ background:rgba(205,255,0,.25); border-radius:3px; }}
::-webkit-scrollbar-thumb:hover {{ background:rgba(205,255,0,.45); }}

.wcs-kpi {{ animation: fadeInUp .45s ease both; }}
.wcs-kpi:hover {{ transform:translateY(-4px) !important; transition:transform .2s ease !important; }}
.wcs-kpi-lime {{ animation: pulse-lime 3.5s ease-in-out infinite; }}
.wcs-kpi-red  {{ animation: pulse-red  3.5s ease-in-out infinite .6s; }}
.wcs-kpi-blue {{ animation: pulse-blue 3.5s ease-in-out infinite 1.2s; }}
.wcs-kpi-white {{ }}
.wcs-insight {{ animation: fadeInUp .4s ease both; }}
.wcs-qblock {{ animation: fadeInLeft .4s ease both; }}
.wcs-edition-card {{ animation: fadeInUp .5s ease both; transition: transform .2s ease, box-shadow .2s ease; }}
.wcs-edition-card:hover {{ transform: translateY(-3px); box-shadow: 0 12px 32px rgba(0,0,0,.6) !important; }}
.wcs-hero {{ animation: border-breathe 4s ease-in-out infinite; }}

.v-menu__content {{
    background: {COLOR_NAVY} !important;
    border: 1px solid {COLOR_LIME}28 !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 44px rgba(0,0,0,.85) !important;
    overflow-y: auto !important;
    backdrop-filter: blur(8px) !important;
}}
.v-menu__content .v-list {{
    background: transparent !important;
    padding: 4px 0 !important;
}}
.v-menu__content .v-list-item {{
    background: transparent !important;
    color: {COLOR_TEXT} !important;
    min-height: 38px !important;
    border-radius: 6px !important;
    margin: 1px 4px !important;
    transition: background .15s ease !important;
}}
.v-menu__content .v-list-item:hover::before {{
    background: {COLOR_LIME}0C !important;
    opacity: 1 !important;
    border-radius: 6px !important;
}}
.v-menu__content .v-list-item__title,
.v-menu__content .v-list-item__content {{
    color: {COLOR_TEXT} !important;
    font-size: .84rem !important;
    font-weight: 500 !important;
}}
.v-menu__content .v-list-item--active {{
    background: {COLOR_LIME}12 !important;
}}
.v-menu__content .v-list-item--active .v-list-item__title {{
    color: {COLOR_LIME} !important;
    font-weight: 700 !important;
}}
.v-menu__content .v-simple-checkbox .v-icon,
.v-menu__content .v-icon {{
    color: {COLOR_LIME} !important;
}}
.v-select__selections, .v-select__selection, .v-select__selection--comma {{
    color: {COLOR_TEXT} !important;
    font-size: .84rem !important;
}}
.v-select__placeholder {{ color: {COLOR_MUTED} !important; }}
.v-chip {{ background: {COLOR_LIME}18 !important; color: {COLOR_LIME} !important; border: 1px solid {COLOR_LIME}35 !important; }}
.v-chip .v-chip__content {{ color: {COLOR_LIME} !important; font-size: .75rem !important; }}
"""
