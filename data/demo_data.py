"""
Datos sintéticos para modo demo — se usan cuando los CSVs reales no están disponibles.

"""
import numpy as np
import pandas as pd

# ── Valores válidos de stage_clean — NO modificar ─────────────────────────────
VALID_STAGES = [
    "Fase de Grupos",
    "Eliminatorias",
    "Cuartos de Final",
    "Semifinal",
    "Final",
]
STAGE_MATCHES = {
    "Fase de Grupos":  24,
    "Eliminatorias":    8,
    "Cuartos de Final": 4,
    "Semifinal":        2,
    "Final":            1,
}

# ── Ediciones — puedes editar cualquier valor ──────────────────────────────────
EDITIONS = [
    #  año    sede             campeón        subcampeón        goleador
    (1930, "Uruguay",      "Uruguay",      "Argentina",      "Guillermo Stábile"),
    (1934, "Italy",        "Italy",        "Czechoslovakia", "Oldřich Nejedlý"),
    (1938, "France",       "Italy",        "Hungary",        "Leônidas"),
    (1950, "Brazil",       "Uruguay",      "Brazil",         "Ademir"),
    (1954, "Switzerland",  "Germany",      "Hungary",        "Sándor Kocsis"),
    (1958, "Sweden",       "Brazil",       "Sweden",         "Just Fontaine"),
    (1962, "Chile",        "Brazil",       "Czechoslovakia", "Garrincha"),
    (1966, "England",      "England",      "Germany",        "Eusébio"),
    (1970, "Mexico",       "Brazil",       "Italy",          "Gerd Müller"),
    (1974, "Germany",      "Germany",      "Netherlands",    "Grzegorz Lato"),
    (1978, "Argentina",    "Argentina",    "Netherlands",    "Mario Kempes"),
    (1982, "Spain",        "Italy",        "Germany",        "Paolo Rossi"),
    (1986, "Mexico",       "Argentina",    "Germany",        "Gary Lineker"),
    (1990, "Italy",        "Germany",      "Argentina",      "Salvatore Schillaci"),
    (1994, "USA",          "Brazil",       "Italy",          "Hristo Stoichkov"),
    (1998, "France",       "France",       "Brazil",         "Davor Šuker"),
    (2002, "Japan/Korea",  "Brazil",       "Germany",        "Ronaldo"),
    (2006, "Germany",      "Italy",        "France",         "Miroslav Klose"),
    (2010, "South Africa", "Spain",        "Netherlands",    "Thomas Müller"),
    (2014, "Brazil",       "Germany",      "Argentina",      "James Rodríguez"),
    (2018, "Russia",       "France",       "Croatia",        "Harry Kane"),
    (2022, "Qatar",        "Argentina",    "France",         "Kylian Mbappé"),
]

# ── Equipos — puedes agregar o quitar ─────────────────────────────────────────
TEAMS = [
    "Brazil", "Germany", "Italy", "France", "Argentina", "England",
    "Spain", "Netherlands", "Uruguay", "Portugal", "Croatia", "Belgium",
    "Mexico", "Colombia", "Chile", "Japan", "South Korea", "Senegal",
    "Morocco", "Australia", "USA", "Poland", "Switzerland", "Denmark",
]

# ── Ciudades y estadios por sede — puedes editar ──────────────────────────────
CITIES_BY_HOST = {
    "Uruguay":       [("Montevideo",      "Estadio Centenario")],
    "Italy":         [("Rome",            "Stadio Olimpico"),    ("Milan",         "San Siro")],
    "France":        [("Paris",           "Stade de France"),    ("Lyon",          "Stade de Gerland")],
    "Brazil":        [("Rio de Janeiro",  "Maracanã"),           ("São Paulo",     "Morumbi"),       ("Belo Horizonte", "Mineirão")],
    "Switzerland":   [("Bern",            "Wankdorf"),           ("Basel",         "St. Jakob-Park")],
    "Sweden":        [("Stockholm",       "Råsunda"),            ("Gothenburg",    "Ullevi")],
    "Chile":         [("Santiago",        "Estadio Nacional"),   ("Viña del Mar",  "Sausalito")],
    "England":       [("London",          "Wembley"),            ("Manchester",    "Old Trafford")],
    "Mexico":        [("Mexico City",     "Azteca"),             ("Guadalajara",   "Jalisco")],
    "Germany":       [("Munich",          "Olympiastadion"),     ("Berlin",        "Olympiastadion"), ("Dortmund", "Signal Iduna Park")],
    "Argentina":     [("Buenos Aires",    "Monumental"),         ("Córdoba",       "Mario Alberto Kempes")],
    "Spain":         [("Madrid",          "Bernabéu"),           ("Barcelona",     "Camp Nou"),       ("Seville", "Sánchez Pizjuán")],
    "USA":           [("New York",        "Giants Stadium"),     ("Los Angeles",   "Rose Bowl"),      ("Chicago", "Soldier Field")],
    "Japan/Korea":   [("Yokohama",        "Int'l Stadium"),      ("Seoul",         "World Cup Stadium")],
    "South Africa":  [("Johannesburg",    "Soccer City"),        ("Cape Town",     "Green Point")],
    "Russia":        [("Moscow",          "Luzhniki"),           ("Saint Petersburg", "Zenit Arena")],
    "Qatar":         [("Lusail",          "Lusail Stadium"),     ("Al Rayyan",     "Education City")],
}

# ── Afluencia base por año — puedes editar los números ───────────────────────
ATT_BASE = {
    1930: 25000, 1934: 35000, 1938: 40000, 1950: 55000, 1954: 38000,
    1958: 32000, 1962: 30000, 1966: 45000, 1970: 52000, 1974: 55000,
    1978: 48000, 1982: 42000, 1986: 50000, 1990: 48000, 1994: 68000,
    1998: 56000, 2002: 40000, 2006: 52000, 2010: 54000, 2014: 62000,
    2018: 45000, 2022: 38000,
}


# ── Generadores ───────────────────────────────────────────────────────────────

def make_matches_df(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    for year, host, *_ in EDITIONS:
        cities   = CITIES_BY_HOST.get(host, [("Host City", "Main Stadium")])
        att_base = ATT_BASE.get(year, 45000)

        for stage, n_matches in STAGE_MATCHES.items():
            for _ in range(n_matches):
                teams  = rng.choice(TEAMS, size=2, replace=False)
                home_g = int(rng.poisson(1.5 if stage == "Fase de Grupos" else 1.2))
                away_g = int(rng.poisson(1.1))
                city, stadium = cities[rng.integers(len(cities))]
                att_mult   = 1.0 + 0.4 * (VALID_STAGES.index(stage) / len(VALID_STAGES))
                attendance = int(max(10000, rng.normal(att_base * att_mult, att_base * 0.15)))

                rows.append({
                    "year":        year,
                    "stage_clean": stage,
                    "home_team":   teams[0],
                    "away_team":   teams[1],
                    "home_goals":  home_g,
                    "away_goals":  away_g,
                    "total_goals": home_g + away_g,
                    "attendance":  attendance,
                    "city":        city,
                    "stadium":     stadium,
                })

    df = pd.DataFrame(rows)

    # Forzar tipos — garantiza que el app nunca falle por tipo incorrecto
    df["year"]        = df["year"].astype(int)
    df["home_goals"]  = df["home_goals"].astype(int)
    df["away_goals"]  = df["away_goals"].astype(int)
    df["total_goals"] = df["total_goals"].astype(int)
    df["attendance"]  = df["attendance"].astype(int)
    df["stage_clean"] = pd.Categorical(df["stage_clean"], categories=VALID_STAGES)

    return df


def make_wc_df() -> pd.DataFrame:
    records = []
    for year, host, champion, runner_up, top_scorer in EDITIONS:
        n_matches = sum(STAGE_MATCHES.values())
        records.append({
            "Year":       year,
            "Host":       host,
            "Champion":   champion,
            "Runner-Up":  runner_up,
            "TopScorrer": top_scorer,       # doble r — coincide con el app
            "Attendance": ATT_BASE.get(year, 45000) * n_matches,
            "Matches":    n_matches,
        })

    df = pd.DataFrame(records)
    df["Year"]       = df["Year"].astype(int)
    df["Attendance"] = df["Attendance"].astype(int)
    df["Matches"]    = df["Matches"].astype(int)
    return df
