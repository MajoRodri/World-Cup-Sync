<div align="center">
  <img src="docs/LogoWorldCup.png" alt="World Cup Sync Logo" width="300"/>

  # World Cup Sync

  **Plataforma de Analítica para el Mundial FIFA · Histórico 1930–2022 + Oportunidad 2026**

  [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
  [![Solara](https://img.shields.io/badge/Solara-1.57.4-CDFF00?logoColor=black)](https://solara.dev)
  [![Plotly](https://img.shields.io/badge/Plotly-6.8.0-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
  [![Pandas](https://img.shields.io/badge/Pandas-3.0.3-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
  [![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/majorodri/world-cup-sync)
  [![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?logo=render&logoColor=white)](https://world-cup-sync.onrender.com)

  *Inteligencia operativa para Streaming CDN · Fan Zones urbanas · Oportunidad presencial 2026*
</div>

---

## Demo

**App en vivo:** [https://world-cup-sync.onrender.com](https://world-cup-sync.onrender.com)

> Desplegada en Render. Si el servidor está inactivo puede tardar ~30 segundos en despertar en la primera carga.

### Notebooks publicados

| Notebook | Descripción |
|----------|-------------|
| [EDA](https://majorodri.github.io/World-Cup-Sync/EDA.html) | Análisis Exploratorio de Datos |
| [Sesgos](https://majorodri.github.io/World-Cup-Sync/Sesgos.html) | Análisis de sesgos históricos |

---

## Fuente de Datos

**Dataset histórico:** [FIFA Football World Cup — Kaggle (piterfm)](https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup)

Histórico completo de **964 partidos** de la Copa del Mundo FIFA (1930–2022). Incluye goles por partido, asistencia, equipos, sedes y resultados por fase. Variables numéricas: `total_goals`, `attendance`, `home_goals`, `away_goals` (4+). Variables categóricas: `stage`, `city`, `home_team`, `away_team` (4+).

> Los CSVs originales no se incluyen en el repositorio. El dataset está disponible públicamente en el link de Kaggle. Sin los archivos locales, la app activa automáticamente el **Modo Demo** con datos sintéticos de distribución equivalente.

**Dataset Fan Festivals 2026:** extraído mediante web scraping de la web oficial de la FIFA con Playwright (`scripts/scrape_fan_fests.py`). El resultado se guarda en `data/fan_fests_2026.csv` — 13 ciudades × 12 campos (ubicación, fechas, capacidad estimada, tipo de acceso, coordenadas geográficas, etc.).

---

## Descripción General

**World Cup Sync** es un dashboard de analítica interactivo construido con **Solara** que combina 92 años de datos históricos del Mundial FIFA (1930–2022) con un análisis prospectivo del torneo en curso. La plataforma está diseñada para responder preguntas de negocio concretas en dos frentes:

- **Operaciones de Streaming** — predecir la demanda de ancho de banda CDN a partir de patrones históricos de densidad de goles por partido.
- **Fan Zones Urbanas** — pronosticar saturación de afluencia y dimensionar seguridad en sedes de transmisión en vivo.
- **Oportunidad comercial 2026** — identificar los 13 puntos de concentración masiva de fans en Norteamérica, cruzando demanda histórica probada con la escala de los Fan Festivals 2026.

La app sigue una estructura narrativa de consultoría: los primeros 5 tabs cuentan la historia del pasado (análisis histórico) y el sexto tab presenta el cierre accionable orientado a directivos (la oportunidad 2026).

---

## Tabs del Dashboard

| Tab | Pregunta de negocio | Salida clave |
|-----|---------------------|--------------|
| 📊 Resumen Ejecutivo | ¿Cómo ha evolucionado el espectáculo goleador en 92 años? | Forecast CDN, tendencia animada, tarjetas por edición |
| 🌆 Fan Zones y Venues | ¿Qué ciudades concentran mayor presión de afluencia? | Ranking top 12 ciudades, P75/P90 saturación, top 10 estadios |
| 🏅 Análisis por Fase | ¿En qué fases converge máximo espectáculo y máxima afluencia? | Riesgo simultáneo, mapa de calor Año × Fase |
| 🌍 Equipos | ¿Cómo se posicionan los equipos ofensiva y defensivamente? | Ranking goleador, scatter táctico, tabla completa |
| 🔍 Match Explorer | ¿Cuál fue el partido más explosivo bajo ciertos filtros? | Tabla de partidos filtrable y ordenable |
| 🗺️ Oportunidad 2026 | ¿Dónde están los 13 puntos de mayor concentración de fans en 2026? | Mapa interactivo, demanda histórica por ciudad, benchmark comparativo |

### KPIs principales (siempre visibles en la parte superior)

| KPI | Descripción |
|-----|-------------|
| ⚽ Partidos Analizados | Total de partidos en el período y filtros seleccionados |
| 📺 Goles / Partido | Promedio de goles por partido — proxy directo de demanda CDN |
| 🏟️ Pico de Afluencia | Mayor asistencia registrada en un solo partido + contexto del partido |
| 🔥 Mayor Goleada Histórica | La goleada más grande de los datos filtrados |
| 🏅 Edición Más Golera | Edición con el mayor promedio de goles por partido |

---

## ¿Por qué Solara y no Streamlit o Power BI?

La elección de **[Solara](https://solara.dev)** tiene dos motivaciones que se refuerzan mutuamente: una personal y una técnica.

**Motivación de diseño:** este proyecto nace de una convicción sobre cómo deben comunicarse los datos a una audiencia no técnica — con jerarquía visual clara, animaciones que guíen la atención y una paleta de color coherente que refuerce el mensaje. Herramientas como Power BI o Streamlit imponen estilos predefinidos que limitan ese control. Solara permite construir cada componente visual desde cero en Python puro, con el mismo nivel de detalle que tendría una aplicación web profesional: colores exactos, tipografía, transiciones, layout responsivo. Para un proyecto orientado al storytelling ejecutivo, esa libertad de diseño no es un lujo — es parte del argumento.

**Motivación técnica:** más allá del diseño, Solara resuelve limitaciones concretas de las alternativas:

| Criterio | Streamlit | Power BI | **Solara** ✓ |
|----------|-----------|----------|--------------|
| Modelo de ejecución | Re-ejecuta todo el script en cada interacción | Motor DAX cerrado | **Reactivo por componente** — solo re-renderiza lo que cambia |
| Integración con Plotly | Parcial (sin control de estado entre gráficos) | No nativo | **Nativa** — `FigurePlotly` + `plotly_iframe` con animaciones completas |
| Control visual y CSS | Mínimo | Nulo desde código | **Total** — paleta, tipografía, layout y animaciones personalizadas |
| Animaciones con `go.Frame` | No soportadas | No disponibles | **Soporte completo** — animaciones ▶/⏸ en todos los gráficos |
| Código modular | Script monolítico | Archivo `.pbix` binario | **Módulos Python** — separación clara de datos, componentes y páginas |
| Despliegue | Streamlit Cloud (limitado) | Power BI Service (requiere licencia) | **Render / Docker** — imagen portable, sin dependencia de plataforma |

> Solara fue aprobado como alternativa equivalente a Streamlit para este proyecto por el equipo docente.

---

## Detalle de cada tab

<details>
<summary><strong>📊 Resumen Ejecutivo</strong></summary>

- **Evolución de goles** — gráfico animado (▶/⏸) de línea + área con media móvil de 3 ediciones, rango min/max y anotaciones del campeón por edición
- **Tarjetas de inteligencia** — una card por edición con sede, campeón, subcampeón, goleador y asistencia total del torneo
- **Insight CDN** — identifica el pico histórico y sugiere filtrar a 2010–2022 para proyecciones operativas precisas
- **Gobernanza de Datos** — sección expandible con 4 sesgos identificados (temporal, formato, asistencia, geográfico) con severidad y mitigaciones, y enlace al Notebook de Sesgos

</details>

<details>
<summary><strong>🌆 Fan Zones y Venues</strong></summary>

- **Top 12 ciudades por afluencia promedio** — gráfico animado de barras horizontales con pico individual por ciudad
- **Distribución estadística con curva KDE** — histograma de goles/partido normalizado a densidad de probabilidad con curva Gaussian KDE (ancho de banda Silverman) y umbrales P75/P90 como alertas CDN
- **Distribución de afluencia con curva KDE** — histograma de asistencia con curva de densidad superpuesta y umbral P75 como alerta operativa Fan Zone
- **Top 10 estadios** — benchmarks de afluencia promedio por recinto, con colorscale azul→lima

</details>

<details>
<summary><strong>🏅 Análisis por Fase</strong></summary>

- **Eje dual por fase** — barras de goles promedio (eje izquierdo, escala lima) superpuestas con línea de afluencia (eje derecho, azul), identificando fases de riesgo simultáneo
- **Mapa de calor Año × Fase** — intensidad de goles por partido en cada combinación edición/fase; colorscale de azul oscuro a rojo pasando por lima

</details>

<details>
<summary><strong>🌍 Equipos</strong></summary>

- **Ranking ofensivo** — top 15 equipos por promedio de goles por partido, con barra animada
- **Scatter de posicionamiento táctico** — cuadrante ataque vs. defensa con burbuja proporcional a partidos jugados; divide el espacio en cuatro arquetipos: Dominadores, Sólidos, Entretenidos y Vulnerables
- **Tabla completa de rendimiento** — victorias, empates, derrotas, GF, GC, diferencial y promedios, filtrable y ordenable

</details>

<details>
<summary><strong>🔍 Match Explorer</strong></summary>

- Controles de filtro: mínimo de goles por partido, mínima asistencia, criterio de ordenamiento
- Tabla completa exportable: año, fase, equipos, marcador, goles totales, asistencia, ciudad y estadio

</details>

<details>
<summary><strong>🗺️ Oportunidad 2026 — Tab de cierre ejecutivo</strong></summary>

Este tab es el **cierre narrativo** del dashboard. Responde la pregunta: *"¿Dónde y cómo se materializa la oportunidad del Mundial 2026?"*. No usa filtros del sidebar — su contenido es independiente y siempre completo.

**Estructura:**

1. **Hero narrativo** — encuadra el análisis como prospectiva comercial: 13 puntos de concentración masiva en Norteamérica.

2. **Mapa interactivo de Norteamérica** — 13 pines coloreados por país (🇲🇽 lima / 🇨🇦 rojo / 🇺🇸 azul). Filtros por país con toggle. Clic en un pin → selecciona esa ciudad.

3. **Detalle de ciudad seleccionada** — dos columnas:
   - *Izquierda*: info del Fan Festival (ubicación, fechas, capacidad estimada, highlights, restricciones de acceso, si requiere registro previo)
   - *Derecha*: historial FIFA de esa ciudad si existe en el dataset (KPIs de promedio/pico/partidos + gráfico animado por edición). Si la ciudad nunca fue sede → card de "mercado virgen" con framing de primer movedor.

4. **Benchmark comparativo** — gráfico animado de barras horizontales: afluencia histórica promedio por ciudad (barras coloreadas por país) superpuesta con marcadores de capacidad estimada del Fan Festival 2026 (línea lima). Permite ver de un vistazo qué ciudades tienen demanda comprobada vs. cuáles son nuevos mercados.

5. **Matriz de acceso** — tabla completa con las 13 ciudades: registro requerido, zona VIP disponible, capacidad estimada por día y tipo de acceso. Identifica las ciudades de mayor potencial de monetización premium.

**Ciudades con historial FIFA comprobado en el dataset:**

| Ciudad | Ediciones | Datos |
|--------|-----------|-------|
| Ciudad de México | 1970, 1986 | `Mexico City` en CSV |
| Guadalajara | 1970, 1986 | `Guadalajara` en CSV |
| Monterrey | 1970, 1986 | `Monterrey` en CSV |
| Boston | 1994 | `Boston` en CSV |
| Los Ángeles | 1994 | `Los Angeles` en CSV |
| Nueva York | 1994 | `New York/New Jersey` en CSV |

Las otras 7 ciudades (Toronto, Vancouver, Atlanta, Houston, Kansas City, Miami, Filadelfia) son nuevas sedes sin historial FIFA → se muestran como "mercados vírgenes".

</details>

---

## Cómo funciona la app

La app tiene dos modos según si los datos están disponibles. **Ambos son completamente funcionales** — todos los filtros, animaciones e interacciones funcionan igual en los dos.

### Modo 1 — Con datos reales (entorno local)

Los datasets originales son privados y no se incluyen en el repositorio ni en la imagen Docker.

```
data/matches.csv  +  data/world_cup.csv
         │
         │  CSVs originales del dataset (privados)
         ↓
notebooks/EDA.ipynb
         │
         │  Limpieza, transformación y análisis exploratorio
         │  Ejecutar todas las celdas del notebook
         ↓
data/matches_limpio.csv
         │
         │  CSV depurado generado por el notebook (también privado)
         ↓
solara run app.py  →  App con datos reales completos
```

### Modo 2 — Modo Demo (Docker Hub / sin CSV)

Cuando los CSVs no están presentes, la app activa automáticamente el **Modo Demo**. Está diseñado para que cualquier persona pueda evaluar la app sin acceso al dataset privado.

```
app.py busca matches_limpio.csv → no encontrado
         │
         ↓
data/demo_data.py  (ya viene dentro de la imagen Docker)
         │
         │  Genera 858 partidos con el mismo esquema exacto
         │  usando distribuciones estadísticas reales (Poisson)
         ↓
App funciona con banner "⚠️ Modo Demo"
```

> **Nota sobre el tab Oportunidad 2026:** sus datos son 100% estáticos (hardcodeados en el código). Funciona igual en Modo Demo y con datos reales. Los datos históricos del historial por ciudad sí dependen del CSV.

### Sobre los datos del Modo Demo

Los datos del Modo Demo **no son inventados** — provienen del dataset real:

- **100% reales:** campeones, subcampeones, sedes, ciudades y estadios históricos de cada edición FIFA (1930–2022).
- **Sintéticos:** únicamente las estadísticas partido a partido (goles y asistencia por match), generadas con distribuciones Poisson que respetan los promedios históricos reales.

<details>
<summary><strong>Ver cobertura del Modo Demo y tabla de archivos por entorno</strong></summary>

| Dimensión | Cobertura |
|-----------|-----------|
| Ediciones | 22 (1930–2022 completas) |
| Selecciones | 24 equipos reales |
| Ciudades | 37 sedes históricas |
| Partidos generados | 858 |
| Valores nulos | 0 |
| Filtros funcionales | Todos |

### Qué se incluye en cada entorno

| Archivo | GitHub | Docker Hub | Render | Descripción |
|---------|:------:|:----------:|:------:|-------------|
| `data/matches.csv` | ❌ | ❌ | ❌ | Dataset original (privado) |
| `data/world_cup.csv` | ❌ | ❌ | ❌ | Dataset original (privado) |
| `data/matches_limpio.csv` | ❌ | ❌ | ❌ | Generado por EDA.ipynb |
| `data/fan_fests_2026.csv` | ✅ | ✅ | ✅ | Resultado del scraping Fan Festivals |
| `scripts/scrape_fan_fests.py` | ✅ | ❌ | ❌ | Scraper Playwright (ejecución local) |
| `data/demo_data.py` | ✅ | ✅ | ✅ | Datos demo empaquetados |
| `notebooks/EDA.ipynb` | ✅ | ❌ | ❌ | Análisis exploratorio |
| `app.py` | ✅ | ✅ | ✅ | Aplicación principal |
| `Dockerfile` | ✅ | — | ✅ | Definición de la imagen |

</details>

---

## Instalación local (con datos reales)

**Requisitos:** Python 3.10+, pip, Jupyter, y los archivos `data/matches.csv` y `data/world_cup.csv`.

```bash
# 1. Clonar el repositorio
git clone https://github.com/MajoRodri/World-Cup-Sync.git
cd World-Cup-Sync

# 2. Crear y activar entorno virtual
python -m venv env
env\Scripts\activate        # Windows
source env/bin/activate     # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar el navegador de Playwright (necesario para el scraper)
playwright install chromium

# 5. Colocar los datasets originales en data/
#    data/matches.csv  y  data/world_cup.csv

# 6. Ejecutar el notebook EDA (genera data/matches_limpio.csv)
jupyter notebook notebooks/EDA.ipynb

# 7. (Opcional) Regenerar el CSV de Fan Festivals desde la web de la FIFA
python scripts/scrape_fan_fests.py

# 8. Lanzar la app
solara run app.py
```

La app se abrirá en `http://localhost:8765`.

---

## Instalación con Docker (Modo Demo)

Forma recomendada para evaluar la app sin necesitar los datos originales. Solo requiere [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Opción A — Desde Docker Hub ✅ recomendado

```bash
docker pull majorodri/world-cup-sync
docker run -p 8765:8765 majorodri/world-cup-sync
```

Abrir `http://localhost:8765`. La app inicia en Modo Demo automáticamente.

### Opción B — Construir la imagen localmente

```bash
git clone https://github.com/MajoRodri/World-Cup-Sync.git
cd World-Cup-Sync
docker build -t world-cup-sync .
docker run -p 8765:8765 world-cup-sync
```

### Opción C — Con datos reales montados

Si tienes los CSVs y quieres usarlos con Docker:

```bash
docker run -p 8765:8765 -v ./data:/app/data majorodri/world-cup-sync
```

Docker monta la carpeta `data/` local dentro del contenedor y la app usa los datos reales.

---

<details>
<summary><strong>Estructura del Proyecto</strong></summary>

```
World-Cup-Sync/
├── app.py                         # Entrypoint de Solara (importa app/page.py)
├── Dockerfile                     # Imagen Docker
├── requirements.txt               # Dependencias Python (versiones fijadas)
├── .gitignore                     # Excluye CSVs privados y entornos virtuales
├── .dockerignore                  # Excluye env/, notebooks y CSVs del build
├── .github/
│   └── workflows/
│       └── deploy-notebooks.yml   # CI/CD: publica HTMLs en GitHub Pages
├── app/
│   ├── page.py                    # Componente raíz: sidebar, hero, KPIs y tabs
│   ├── constants.py               # Paleta de colores, BASE_LAYOUT, APP_CSS, play_menu
│   ├── data.py                    # Carga de datos (local → Drive → demo)
│   ├── components/
│   │   ├── __init__.py
│   │   ├── ui_blocks.py           # QBlock, InsightBox, ScoreBadge, plotly_iframe
│   │   ├── kpi_cards.py           # KPICard
│   │   └── sidebar.py             # AppSidebar (filtros año, fase, equipo)
│   └── pages/
│       ├── __init__.py
│       ├── resumen.py             # Tab 1 — Resumen Ejecutivo
│       ├── fanzones.py            # Tab 2 — Fan Zones y Venues
│       ├── fases.py               # Tab 3 — Análisis por Fase
│       ├── equipos.py             # Tab 4 — Equipos
│       ├── explorer.py            # Tab 5 — Match Explorer
│       └── festivales.py          # Tab 6 — Oportunidad 2026 (Fan Festivals)
├── scripts/
│   └── scrape_fan_fests.py        # Web scraper Playwright — extrae Fan Festivals 2026 de la FIFA
├── data/
│   ├── fan_fests_2026.csv         # Resultado del scraping — 13 Fan Festivals, 12 campos
│   ├── demo_data.py               # Generador de datos demo (incluido en Docker)
│   ├── matches.csv                # Dataset original — NO se sube (privado)
│   ├── world_cup.csv              # Dataset original — NO se sube (privado)
│   └── matches_limpio.csv         # Generado por EDA.ipynb — NO se sube
├── docs/
│   └── LogoWorldCup.png           # Logo de la app
└── notebooks/
    ├── EDA.ipynb                  # Limpieza y análisis → genera matches_limpio.csv
    ├── EDA.html                   # EDA exportado (publicado en GitHub Pages)
    ├── Sesgos.ipynb               # Análisis de sesgos históricos
    └── Sesgos.html                # Sesgos exportado (publicado en GitHub Pages)
```

</details>

<details>
<summary><strong>Stack Tecnológico y Datos</strong></summary>

### Stack

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Framework UI | [Solara](https://solara.dev) | 1.57.4 |
| Visualizaciones | [Plotly](https://plotly.com/python/) | 6.8.0 |
| Procesamiento de datos | [Pandas](https://pandas.pydata.org) | 3.0.3 |
| Álgebra numérica | [NumPy](https://numpy.org) | 2.4.6 |
| Widgets reactivos | ipyvuetify, ipywidgets | 1.11.3 / 8.1.8 |
| Servidor ASGI | uvicorn + starlette | 0.49.0 / 1.2.1 |
| Web Scraping | [Playwright](https://playwright.dev/python/) | latest |
| Contenedores | Docker | — |
| Despliegue cloud | [Render](https://render.com) | — |
| CI/CD | GitHub Actions → GitHub Pages | — |

### Esquema de datos

**Fuente histórica:** [FIFA Football World Cup — Kaggle (piterfm)](https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup)

| Archivo | Registros | Columnas clave |
|---------|-----------|----------------|
| `matches_limpio.csv` | ~1,000+ partidos | `year`, `stage_clean`, `home_team`, `away_team`, `home_goals`, `away_goals`, `total_goals`, `attendance`, `city`, `stadium` |
| `world_cup.csv` | 22 ediciones | `Year`, `Host`, `Champion`, `Runner-Up`, `TopScorer`, `Attendance`, `Matches` |

**Fuente prospectiva (Tab 6):** datos del Fan Festival 2026 extraídos de la web oficial de la FIFA mediante el scraper `scripts/scrape_fan_fests.py` (Playwright) y guardados en `data/fan_fests_2026.csv`. Los mismos datos se integran en `app/pages/festivales.py` para la visualización interactiva — ubicaciones, fechas, capacidad estimada, requisitos de acceso y artistas confirmados para las 13 ciudades sede.

> **Nota de Gobernanza:** Las cifras de asistencia anteriores a 1970 pueden contener inconsistencias metodológicas. Para proyecciones operativas se recomienda filtrar a **2010–2022** usando el slider del sidebar.

</details>

<details>
<summary><strong>Solución de Problemas</strong></summary>

### La app no abre en el navegador

Verifica que Solara esté corriendo y accede a `http://localhost:8765`. Si el puerto está ocupado:

```bash
solara run app.py --port 8766
```

### Error: `matches_limpio.csv` no encontrado

El CSV limpio se genera ejecutando el notebook EDA. Verifica que:
1. Tienes `data/matches.csv` y `data/world_cup.csv`
2. Ejecutaste **todas** las celdas de `notebooks/EDA.ipynb`
3. El archivo `data/matches_limpio.csv` fue creado

Si no tienes los CSVs originales, la app entra automáticamente en **Modo Demo** — esto es el comportamiento esperado.

### Docker: el contenedor no arranca

```bash
docker logs <container_id>   # ver el error
docker ps                    # ver contenedores activos
docker stop $(docker ps -q)  # detener todos
```

### Docker: puerto 8765 ya en uso

```bash
docker run -p 8766:8765 majorodri/world-cup-sync
# abrir http://localhost:8766
```

### El Modo Demo muestra un banner de aviso

Es el comportamiento correcto. El banner `⚠️ Modo Demo` confirma que la app no encontró los CSVs privados y está usando datos sintéticos. Todos los filtros y visualizaciones funcionan normalmente, excepto que el Tab 6 mostrará "Sin historial" para todas las ciudades (ya que no hay datos reales cargados).

### Error al ejecutar el scraper (`playwright install` requerido)

Playwright necesita descargar el navegador por separado después del `pip install`:

```bash
playwright install chromium
```

Si el scraper no detecta tarjetas dinámicas en la web de la FIFA (la estructura HTML puede cambiar), carga automáticamente los datos manuales incorporados en el script — el CSV resultante es el mismo.

### Gráficos no renderizan / pantalla en blanco

Prueba con Chrome o Firefox actualizados. Si el problema persiste, limpia la caché del navegador (`Ctrl+Shift+R`).

### Dependencias desactualizadas

```bash
pip install --upgrade -r requirements.txt
```

</details>

---

## Licencia

Este proyecto es de uso interno / analítico. Los datos históricos del Mundial FIFA se utilizan con fines educativos y de investigación.

---

<div align="center">
  Hecho con pasión por el fútbol por <a href="https://github.com/MajoRodri">MajoRodri</a>
</div>
