"""
Scraper de Fan Festivals FIFA World Cup 2026
Fuente: https://www.fifa.com/es/tournaments/mens/worldcup/canadamexicousa2026/fifa-fan-festival

Requiere: pip install playwright pandas
          playwright install chromium
"""

from playwright.sync_api import sync_playwright
import pandas as pd


def extraer_fan_fests() -> pd.DataFrame:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_extra_http_headers({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/110.0.0.0 Safari/537.36"
            )
        })

        url = (
            "https://www.fifa.com/es/tournaments/mens/worldcup/"
            "canadamexicousa2026/fifa-fan-festival"
        )

        print("Accediendo a la web de la FIFA...")
        page.goto(url, wait_until="networkidle")

        datos_ciudades = []

        tarjetas_ciudades = page.locator(".fan-fest-card").all()
        print(f"Se encontraron {len(tarjetas_ciudades)} sedes. Extrayendo...")

        for tarjeta in tarjetas_ciudades:
            try:
                ciudad = tarjeta.locator(".city-name").inner_text()
                ubicacion = tarjeta.locator(".location-details").inner_text()
                fechas = tarjeta.locator(".dates-info").inner_text()
                datos_ciudades.append({
                    "Ciudad": ciudad,
                    "Ubicación": ubicacion,
                    "Fechas": fechas,
                })
            except Exception as e:
                print(f"Error extrayendo una tarjeta: {e}")

        browser.close()

        # Si el selector dinámico falló, se carga el dataset construido manualmente
        if not datos_ciudades:
            print("No se detectaron tarjetas dinámicas — cargando datos manuales...")
            return _datos_manuales()

        return pd.DataFrame(datos_ciudades)


def _datos_manuales() -> pd.DataFrame:
    """
    Datos recopilados manualmente de la web oficial de la FIFA (junio 2026).
    Se usa como fallback cuando el scraper dinámico no encuentra los selectores CSS.
    """
    registros = [
        dict(Ciudad="Ciudad de México", País="México",
             Ubicación="Zócalo · Plaza de la Constitución",
             Fechas="11 jun – 19 jul 2026",
             Acceso="Gratuito", Registro=False, VIP=False,
             Capacidad_est=150_000,
             Highlights="Banda El Recodo · K-Tigers · Frida: The Musical · Pantallas gigantes",
             Restricciones="Sin mochilas grandes · Bolsas transparentes recomendadas",
             Latitud=19.4326, Longitud=-99.1332),
        dict(Ciudad="Guadalajara", País="México",
             Ubicación="Plaza Liberación · Centro Histórico",
             Fechas="11 jun – 19 jul 2026 (días de partido)",
             Acceso="Gratuito · Requiere pase digital FIFA", Registro=True, VIP=False,
             Capacidad_est=40_000,
             Highlights="Tacos y tortas ahogadas · Activaciones FIFA · Tienda oficial",
             Restricciones="Cupo limitado · Registro obligatorio en plataforma FIFA",
             Latitud=20.6767, Longitud=-103.3475),
        dict(Ciudad="Monterrey", País="México",
             Ubicación="Parque Fundidora",
             Fechas="11 jun – 19 jul 2026",
             Acceso="Gratuito + Zonas VIP / Conciertos de pago", Registro=False, VIP=True,
             Capacidad_est=80_000,
             Highlights="Espacio industrial recuperado · Canchas recreativas · Gastronomía regia",
             Restricciones="VIP y conciertos especiales requieren ticket (Ticketmaster)",
             Latitud=25.6714, Longitud=-100.2846),
        dict(Ciudad="Toronto", País="Canadá",
             Ubicación="Fort York National Historic Site · The Bentway",
             Fechas="11 jun – 19 jul 2026",
             Acceso="Gratuito", Registro=False, VIP=False,
             Capacidad_est=50_000,
             Highlights="'El Mundo en una Ciudad' · Conciertos diarios · Diversidad multicultural",
             Restricciones="Sin mochilas grandes ni equipaje de mano grande",
             Latitud=43.6386, Longitud=-79.4014),
        dict(Ciudad="Vancouver", País="Canadá",
             Ubicación="PNE Grounds · Hastings Park",
             Fechas="11 jun – 19 jul 2026",
             Acceso="Gratuito + Hospitalidad Premium de pago", Registro=False, VIP=True,
             Capacidad_est=45_000,
             Highlights="Freedom Mobile Amphitheatre · Vista a montañas · Food trucks internacionales",
             Restricciones="Zonas Premium/VIP con ticket adicional",
             Latitud=49.2827, Longitud=-123.1207),
        dict(Ciudad="Atlanta", País="EE.UU.",
             Ubicación="Centennial Olympic Park",
             Fechas="11 jun – 19 jul 2026",
             Acceso="GA Gratuito + Zona GA+ mejorada", Registro=False, VIP=True,
             Capacidad_est=70_000,
             Highlights="Summer Walker · Ludacris · CeeLo Green · EARTHGANG",
             Restricciones="GA+ requiere acceso diferenciado · Política de bolsas estándar FIFA",
             Latitud=33.7595, Longitud=-84.3921),
        dict(Ciudad="Boston", País="EE.UU.",
             Ubicación="City Hall Plaza",
             Fechas="16 días (días de partido asignados)",
             Acceso="Gratuito", Registro=False, VIP=False,
             Capacidad_est=35_000,
             Highlights="Acceso MBTA · Ambiente comunitario local · Orientado al fan local",
             Restricciones="Activo exclusivamente en días de partido programados",
             Latitud=42.3601, Longitud=-71.0589),
        dict(Ciudad="Houston", País="EE.UU.",
             Ubicación="EaDo · East Downtown",
             Fechas="11 jun – 19 jul 2026",
             Acceso="Gratuito", Registro=False, VIP=False,
             Capacidad_est=60_000,
             Highlights="Football Fiesta Houston · Música latina · Torneos Fútbol 5 · Fusión tejano-mexicana",
             Restricciones="Protocolo estándar FIFA de seguridad",
             Latitud=29.7604, Longitud=-95.3595),
        dict(Ciudad="Kansas City", País="EE.UU.",
             Ubicación="National WWI Museum and Memorial",
             Fechas="18 días seleccionados del torneo",
             Acceso="Gratuito · Requiere registro digital previo", Registro=True, VIP=False,
             Capacidad_est=30_000,
             Highlights="Vista panorámica al skyline KC · Pantalla gigante · Activaciones patrocinadores",
             Restricciones="Registro digital obligatorio · Regulaciones estrictas del memorial · Aforo controlado",
             Latitud=39.0997, Longitud=-94.5786),
        dict(Ciudad="Los Ángeles", País="EE.UU.",
             Ubicación="LA Memorial Coliseum + Fan Zones satélite",
             Fechas="11–15 jun centralizado · luego distribución metropolitana",
             Acceso="Gratuito", Registro=False, VIP=False,
             Capacidad_est=100_000,
             Highlights="Semana inaugural centralizada · Zonas satélite costeras y plazas urbanas",
             Restricciones="Post-15 jun: múltiples ubicaciones — verificar cada zona satélite",
             Latitud=34.0141, Longitud=-118.2879),
        dict(Ciudad="Miami", País="EE.UU.",
             Ubicación="Bayfront Park · Downtown Miami",
             Fechas="13 jun – 5 jul 2026",
             Acceso="Gratuito · Sin registro", Registro=False, VIP=False,
             Capacidad_est=30_000,
             Highlights="Frente al mar · Música urbana, caribeña y electrónica · ~30K personas/día",
             Restricciones="Sin pase previo requerido · Acceso directo",
             Latitud=25.7743, Longitud=-80.1870),
        dict(Ciudad="Filadelfia", País="EE.UU.",
             Ubicación="Lemon Hill · Fairmount Park",
             Fechas="11 jun – 19 jul 2026",
             Acceso="GA Gratuito · Conciertos sin partido con ticket", Registro=False, VIP=True,
             Capacidad_est=50_000,
             Highlights="Acceso general gratuito en días de partido · Festivales de música adicionales",
             Restricciones="Días sin partido: eventos de pago con ticket independiente",
             Latitud=39.9526, Longitud=-75.1652),
        dict(Ciudad="Nueva York", País="EE.UU.",
             Ubicación="Queens · Manhattan · Bronx · Brooklyn · Staten Island",
             Fechas="11 jun – 19 jul 2026 (rotación por fase)",
             Acceso="Gratuito", Registro=False, VIP=False,
             Capacidad_est=80_000,
             Highlights="USTA Queens (grupos) · Rockefeller Center (eliminatorias/final) · Brooklyn Bridge Park",
             Restricciones="Formato satélite: zona activa varía por fase del torneo",
             Latitud=40.7128, Longitud=-74.0060),
    ]
    return pd.DataFrame(registros)


if __name__ == "__main__":
    df = extraer_fan_fests()
    print("\n--- Datos Extraídos ---")
    print(df.to_string())

    out = "data/fan_fests_2026.csv"
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"\nArchivo guardado como {out}")
