# Página 5 — Match Explorer / Page 5 — Match Explorer

import pandas as pd
import solara

from app.components import QBlock, InsightBox, ScoreBadge


@solara.component
def Tab5_Explorer(df: pd.DataFrame):
    QBlock("01", "🔍 Base de datos histórica · análisis individual",
           "¿Cuál fue el partido más memorable de la historia del Mundial?",
           "Filtra por goles, afluencia y ordenación para encontrar los partidos que definieron una era")

    fe_min_g, set_fe_min_g = solara.use_state(0)
    fe_min_a, set_fe_min_a = solara.use_state(0)
    fe_sort,  set_fe_sort  = solara.use_state("Año (reciente)")

    with solara.Columns([1, 1, 1]):
        with solara.Column():
            solara.InputInt(label="Goles mínimos", value=fe_min_g, on_value=set_fe_min_g)
        with solara.Column():
            solara.InputInt(label="Afluencia mínima (miles)", value=fe_min_a, on_value=set_fe_min_a)
        with solara.Column():
            solara.Select(label="Ordenar por", value=fe_sort,
                          values=["Año (reciente)", "Goles (más goles)",
                                  "Afluencia (mayor)", "Año (antiguo)"],
                          on_value=set_fe_sort)

    sort_map = {
        "Año (reciente)":    ("year",        False),
        "Goles (más goles)": ("total_goals", False),
        "Afluencia (mayor)": ("attendance",  False),
        "Año (antiguo)":     ("year",        True),
    }
    sc, sa = sort_map.get(fe_sort, ("year", False))

    edf = df[df["total_goals"] >= fe_min_g].copy()
    att_threshold = fe_min_a * 1000
    if att_threshold > 0:
        edf = edf[edf["attendance"] >= att_threshold]
    edf = edf.sort_values(sc, ascending=sa)

    edf["Resultado"]  = (edf["home_goals"].astype(int).astype(str) + " – " +
                         edf["away_goals"].astype(int).astype(str))
    edf["Asistencia"] = edf["attendance"].apply(
        lambda v: f"{int(v):,}" if pd.notna(v) else "—")

    show = edf[["year", "stage_clean", "home_team", "Resultado", "away_team",
                "total_goals", "Asistencia", "city", "stadium"]].rename(columns={
        "year": "Año", "stage_clean": "Fase", "home_team": "Local",
        "away_team": "Visitante", "total_goals": "Goles",
        "city": "Ciudad", "stadium": "Estadio",
    })

    InsightBox(f"⚽ <b>{len(show):,} partidos encontrados</b> con los filtros actuales.")

    if not show.empty:
        top5 = show.head(5)
        for _, row in top5.iterrows():
            ScoreBadge(
                str(row["Local"]), str(row["Resultado"]), str(row["Visitante"]),
                int(row["Año"]), str(row["Fase"])
            )
        solara.HTML("div", unsafe_innerHTML="<div style='height:10px'></div>")

    solara.DataFrame(show.reset_index(drop=True), items_per_page=25)
