# Bloques UI reutilizables: QBlock, InsightBox, ScoreBadge, iframe / Reusable UI blocks

import base64

import solara
from app.constants import (
    COLOR_RED, COLOR_LIME, COLOR_BLUE, COLOR_WHITE,
    COLOR_NAVY, COLOR_MUTED, COLOR_TEXT,
)


@solara.component
def QBlock(num: str, label_text: str, question: str, context: str, variant: str = "lime"):
    color_map = {"lime": COLOR_LIME, "red": COLOR_RED, "blue": COLOR_BLUE}
    bg_map = {
        "lime": f"linear-gradient(90deg,{COLOR_LIME}06 0%,transparent 80%)",
        "red":  f"linear-gradient(90deg,{COLOR_RED}08 0%,transparent 80%)",
        "blue": f"linear-gradient(90deg,{COLOR_BLUE}0A 0%,transparent 80%)",
    }
    c  = color_map.get(variant, COLOR_LIME)
    bg = bg_map.get(variant, bg_map["lime"])
    solara.HTML("div", unsafe_innerHTML=f"""
        <div class="wcs-qblock" style="margin:32px 0 12px;padding:18px 22px 16px;background:{bg};
            border-left:3px solid {c};border-radius:0 10px 10px 0;position:relative;overflow:hidden;">
            <div style="position:absolute;right:10px;bottom:-8px;font-size:3.6rem;opacity:.04;
                pointer-events:none;user-select:none;">⚽</div>
            <span style="font-size:4rem;font-weight:900;color:rgba(255,255,255,.04);
                position:absolute;right:48px;top:0;line-height:1;pointer-events:none;">{num}</span>
            <p style="font-size:.62rem;font-weight:700;text-transform:uppercase;
                letter-spacing:2px;color:{c};margin:0 0 4px;">{label_text}</p>
            <p style="font-size:1.12rem;font-weight:800;color:{COLOR_WHITE};
                line-height:1.35;margin:0 0 4px;">{question}</p>
            <p style="font-size:.70rem;color:{COLOR_MUTED};margin:0;">{context}</p>
        </div>
    """)


@solara.component
def InsightBox(text: str, variant: str = "lime"):
    palette = {
        "lime":  (f"{COLOR_LIME}07",  f"{COLOR_LIME}28"),
        "red":   (f"{COLOR_RED}08",   f"{COLOR_RED}32"),
        "blue":  (f"{COLOR_BLUE}0A",  f"{COLOR_BLUE}38"),
    }
    bg, border = palette.get(variant, palette["lime"])
    icon = {"lime": "💡", "red": "📺", "blue": "🌆"}.get(variant, "💡")
    solara.HTML("div", unsafe_innerHTML=f"""
        <div class="wcs-insight" style="background:{bg};border:1px solid {border};
            border-radius:8px;padding:10px 14px;margin:8px 0 18px;
            font-size:.80rem;color:{COLOR_TEXT};line-height:1.6;
            position:relative;overflow:hidden;">
            <div style="position:absolute;right:-4px;bottom:-6px;font-size:2.2rem;
                opacity:.05;pointer-events:none;">{icon}</div>
            {text}
        </div>
    """)


def plotly_iframe(fig, height: int = 450) -> None:
    # iframe necesario para serializar frames de animación en Solara / iframe required so Plotly animation frames serialize in Solara
    html_bytes = fig.to_html(full_html=True, include_plotlyjs="cdn").encode("utf-8")
    b64 = base64.b64encode(html_bytes).decode("ascii")
    solara.HTML("div", unsafe_innerHTML=(
        f'<iframe src="data:text/html;base64,{b64}" '
        f'width="100%" height="{height + 20}px" '
        f'style="border:none;display:block;overflow:hidden;"></iframe>'
    ))


@solara.component
def ScoreBadge(home: str, score: str, away: str, year: int, phase: str):
    solara.HTML("div", unsafe_innerHTML=f"""
        <div style="background:linear-gradient(135deg,#0A1220 0%,#111E35 100%);
            border:1px solid {COLOR_LIME}22;border-radius:10px;padding:10px 16px;
            display:flex;align-items:center;justify-content:space-between;
            margin:4px 0;font-family:'Inter',sans-serif;gap:10px;">
            <span style="color:{COLOR_TEXT};font-size:.78rem;font-weight:600;
                flex:1;text-align:right;">{home}</span>
            <div style="background:{COLOR_NAVY};border:1px solid {COLOR_LIME}40;
                border-radius:6px;padding:4px 14px;text-align:center;min-width:64px;">
                <div style="font-size:1.1rem;font-weight:900;color:{COLOR_LIME};
                    letter-spacing:3px;">{score}</div>
                <div style="font-size:.52rem;color:{COLOR_MUTED};letter-spacing:1px;
                    text-transform:uppercase;">{year} · {phase}</div>
            </div>
            <span style="color:{COLOR_TEXT};font-size:.78rem;font-weight:600;
                flex:1;text-align:left;">{away}</span>
        </div>
    """)
