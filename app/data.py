# Carga de datos con fallback en 3 pasos / Data loading with 3-step fallback

import pandas as pd

_GD = "https://drive.google.com/uc?export=download&id={}"
_MATCHES_URL = _GD.format("1RriyHpIlIW_igyxv-0GR5VoBI0llUDf9")
_WC_URL      = _GD.format("1AjTrgi91fmDh6M8Ltiuz_8mdUjsOIF90")


def _load_matches(src: str) -> pd.DataFrame:
    df = pd.read_csv(src)
    df["year"]        = pd.to_numeric(df["year"],        errors="coerce")
    df["total_goals"] = pd.to_numeric(df["total_goals"], errors="coerce")
    df["attendance"]  = pd.to_numeric(df["attendance"],  errors="coerce")
    return df.dropna(subset=["year", "total_goals"])


def _load_wc(src: str) -> pd.DataFrame:
    try:
        wc = pd.read_csv(src, encoding="latin-1")
        wc.columns = [c.strip() for c in wc.columns]
        wc["Year"] = pd.to_numeric(wc["Year"], errors="coerce")
        return wc.dropna(subset=["Year"])
    except Exception:
        return pd.DataFrame()


def _try_load():
    # 1. Archivos locales — entorno de desarrollo / Local files — dev environment
    try:
        return _load_matches("data/matches_limpio.csv"), _load_wc("data/world_cup.csv"), False
    except (FileNotFoundError, Exception):
        pass

    # 2. Google Drive — deploy, Docker, cualquier entorno sin archivos locales / any env without local files
    try:
        return _load_matches(_MATCHES_URL), _load_wc(_WC_URL), False
    except Exception:
        pass

    # 3. Demo sintético de emergencia / Synthetic emergency fallback
    try:
        from data.demo_data import make_matches_df, make_wc_df as _mk_wc
        return make_matches_df(), _mk_wc(), True
    except ImportError:
        _cols = ["year", "total_goals", "attendance", "stage_clean",
                 "home_team", "away_team", "home_goals", "away_goals", "city", "stadium"]
        return pd.DataFrame(columns=_cols), pd.DataFrame(), True


df_raw, wc_df, DEMO_MODE = _try_load()

yr_min = int(df_raw["year"].min()) if not df_raw.empty else 1930
yr_max = int(df_raw["year"].max()) if not df_raw.empty else 2022

stages_all       = sorted(df_raw["stage_clean"].dropna().unique().tolist()) if not df_raw.empty else []
teams_all        = (sorted(set(df_raw["home_team"]) | set(df_raw["away_team"]))
                    if not df_raw.empty else [])
years_available  = (sorted(df_raw["year"].dropna().unique().astype(int).tolist())
                    if not df_raw.empty else [yr_min, yr_max])
