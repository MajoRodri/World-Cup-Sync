<div align="center">
  <img src="docs/LogoWorldCup.png" alt="World Cup Sync Logo" width="300"/>

  # World Cup Sync

  **Plataforma de Analítica para Datos del Mundial de Fútbol FIFA · 1930–2022**

  [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
  [![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
  [![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?logo=plotly&logoColor=white)](https://plotly.com)
  [![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
  [![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/majorodri/world-cup-sync)

  *Inteligencia operativa para planificación de CDN en streaming y gestión de Fan Zones urbanas*
</div>

---

## Demo

> Video próximamente — ¡mantente al tanto!

### Notebooks publicados

| Notebook | Descripción |
|----------|-------------|
| [EDA](https://majorodri.github.io/World-Cup-Sync/EDA.html) | Análisis Exploratorio de Datos |
| [Sesgos](https://majorodri.github.io/World-Cup-Sync/Sesgos.html) | Análisis de sesgos históricos |

---

## Descripción General

World Cup Sync es un dashboard de analítica interactivo construido con **Streamlit** que expone 92 años de datos del Mundial FIFA (1930–2022) para dos casos de uso operativos principales:

- **Operaciones de Streaming** — predecir la demanda de ancho de banda CDN a partir de patrones de densidad de goles.
- **Fan Zones Urbanas** — pronosticar la saturación de afluencia y dimensionar la seguridad en sedes de transmisión en vivo.

---

## Funcionalidades

| Módulo | Enfoque | Salida Clave |
|--------|---------|--------------|
| 📊 Resumen Ejecutivo | Tendencia de goles + historial de ediciones | Pronóstico de demanda CDN, tarjetas editoriales |
| 🌆 Fan Zones & Venues | Asistencia por ciudad y estadio | Probabilidad de saturación de afluencia |
| 🏅 Análisis por Fase | Riesgo dual por fase del torneo | Picos simultáneos de espectáculo y afluencia |
| 🌍 Equipos | Ataque / defensa / ranking de equipos | Scatter de posicionamiento táctico |
| 🔍 Match Explorer | Base de datos de partidos individuales | Registros de partidos filtrados y ordenables |

<details>
<summary><strong>Ver detalle de cada módulo y KPIs</strong></summary>

### 5 KPIs Principales (siempre visibles)

| KPI | Descripción |
|-----|-------------|
| ⚽ Partidos Analizados | Total de partidos en el período seleccionado |
| 📺 Espectáculo Digital | Promedio de goles por partido (proxy de ancho de banda CDN) |
| 🏟️ Pico de Afluencia | Mayor asistencia en un solo partido + contexto |
| 🔥 Mayor Goleada Histórica | La goleada más grande jamás registrada |
| 🏅 Edición Más Golera | Edición con el mayor promedio de goles por partido |

### 📊 Resumen Ejecutivo

- **Gráfico de evolución de goles** — línea + área con media móvil de 3 ediciones y anotación del campeón por edición
- **Tarjetas de inteligencia por edición** — sede, campeón, subcampeón, goleador y asistencia total de cada Mundial
- **Insight CDN** — identifica el pico histórico de goles por partido para dimensionar ancho de banda

### 🌆 Fan Zones & Venues

- **Top 12 ciudades por asistencia promedio** con récord individual por ciudad
- **Histograma de saturación de streaming** — distribución de goles/partido con umbrales P75 y P90
- **Histograma de saturación de Fan Zone** — distribución de asistencia con alertas de presión de afluencia
- **Benchmarks de estadios** — top 10 venues ordenados por utilización promedio de capacidad

### 🏅 Análisis por Fase

- **Gráfico de doble eje** — goles por fase (barras) superpuesto con asistencia promedio (línea), destacando fases de riesgo simultáneo
- **Mapa de calor Año × Fase** — intensidad de goles por partido en cada edición y fase del torneo

### 🌍 Equipos

- **Ranking ofensivo** — top 15 equipos por promedio de goles por partido
- **Scatter de posicionamiento táctico** — cuadrante ataque vs. defensa con burbuja proporcional a partidos jugados
- **Tabla de rendimiento completa** — victorias, empates, derrotas, GF, GC, diferencial y promedios ordenables

### 🔍 Match Explorer

- Filtro por mínimo de goles, mínima asistencia y criterio de ordenamiento
- Tabla completa: año, fase, equipos, marcador, goles, asistencia, ciudad y estadio

</details>

---

## Cómo funciona la app

La app tiene dos modos de ejecución según si los datos reales están disponibles o no. **Ambos modos son completamente funcionales** — todos los filtros, gráficos e interacciones funcionan igual en los dos.

### Modo 1 — Con datos reales (entorno local)

Los datasets originales son privados y no se incluyen en el repositorio ni en la imagen Docker. Para ejecutar la app con datos reales hay que seguir este pipeline:

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
         │  CSV depurado generado por el notebook
         │  Tampoco se sube (está en .gitignore)
         ↓
streamlit run app.py  →  App con datos reales completos
```

### Modo 2 — Sin datos / Modo Demo (Docker Hub)

Cuando los CSVs no están presentes, la app activa automáticamente el **Modo Demo**. Está diseñado para que cualquier persona pueda evaluar la app sin necesitar acceso al dataset privado.

```
docker pull majorodri/world-cup-sync
docker run -p 8501:8501 majorodri/world-cup-sync
         │
         │  app.py busca matches_limpio.csv → no encontrado
         ↓
data/demo_data.py  (ya viene dentro de la imagen Docker)
         │
         │  Genera 858 partidos con el mismo esquema exacto
         ↓
App funciona con banner "Modo Demo 🔒"
```

### Sobre los datos del Modo Demo

Los datos del Modo Demo **no son inventados** — provienen del dataset real:

- **Datos 100% reales:** campeones, subcampeones, goleadores históricos, sedes, ciudades y estadios de cada edición FIFA (1930–2022).
- **Generados sintéticamente:** únicamente las estadísticas partido a partido (goles y asistencia por match), manteniendo distribuciones estadísticas realistas mediante modelos de Poisson.

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

| Archivo | GitHub | Docker Hub | Descripción |
|---------|:------:|:----------:|-------------|
| `data/matches.csv` | ❌ | ❌ | Dataset original (privado) |
| `data/world_cup.csv` | ❌ | ❌ | Dataset original (privado) |
| `data/matches_limpio.csv` | ❌ | ❌ | Generado por el notebook EDA |
| `data/demo_data.py` | ✅ | ✅ | Datos demo empaquetados |
| `notebooks/EDA.ipynb` | ✅ | ❌ | Análisis exploratorio |
| `app.py` | ✅ | ✅ | Aplicación principal |
| `Dockerfile` | ✅ | — | Definición de la imagen |

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

# 4. Colocar los datasets originales en data/
#    data/matches.csv  y  data/world_cup.csv

# 5. Ejecutar el notebook EDA (genera data/matches_limpio.csv)
jupyter notebook notebooks/EDA.ipynb

# 6. Lanzar la app
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`.

---

## Instalación con Docker (Modo Demo)

Forma recomendada para evaluar la app sin necesitar los datos originales. Solo requiere tener [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.

### Opción A — Desde Docker Hub ✅ recomendado

```bash
docker pull majorodri/world-cup-sync
docker run -p 8501:8501 majorodri/world-cup-sync
```

Abrir `http://localhost:8501`. La app inicia en Modo Demo automáticamente.

### Opción B — Construir la imagen localmente

```bash
git clone https://github.com/MajoRodri/World-Cup-Sync.git
cd World-Cup-Sync
docker build -t world-cup-sync .
docker run -p 8501:8501 world-cup-sync
```

### Opción C — Con datos reales montados

Si tienes los CSVs y quieres usarlos con Docker:

```bash
docker run -p 8501:8501 -v ./data:/app/data majorodri/world-cup-sync
```

Docker monta la carpeta `data/` local dentro del contenedor y la app usa los datos reales en vez del modo demo.

---

<details>
<summary><strong>Estructura del Proyecto</strong></summary>

```
World-Cup-Sync/
├── app.py                        # Aplicación principal de Streamlit
├── Dockerfile                    # Definición de la imagen Docker
├── requirements.txt              # Dependencias de Python
├── .gitignore                    # Excluye CSVs privados y entornos virtuales
├── .dockerignore                 # Excluye CSVs, env/, notebooks del build
├── .streamlit/
│   └── config.toml               # Tema oscuro + configuración del servidor
├── .github/
│   └── workflows/
│       └── deploy-notebooks.yml  # GitHub Actions → publica HTMLs en Pages
├── data/
│   ├── demo_data.py              # Datos demo empaquetados (incluido en Docker)
│   ├── matches.csv               # Dataset original — NO se sube (privado)
│   ├── world_cup.csv             # Dataset original — NO se sube (privado)
│   └── matches_limpio.csv        # Generado por EDA.ipynb — NO se sube
├── docs/
│   └── LogoWorldCup.png          # Logo de la app
└── notebooks/
    ├── EDA.ipynb                 # Limpieza y análisis → genera matches_limpio.csv
    ├── EDA.html                  # EDA exportado (publicado en GitHub Pages)
    ├── Sesgos.ipynb              # Análisis de sesgos históricos
    └── Sesgos.html               # Sesgos exportado (publicado en GitHub Pages)
```

</details>

<details>
<summary><strong>Stack Tecnológico y Datos</strong></summary>

### Stack

| Capa | Tecnología |
|------|-----------|
| Framework UI | [Streamlit](https://streamlit.io) 1.32+ |
| Procesamiento de Datos | [Pandas](https://pandas.pydata.org) 2.0+, [NumPy](https://numpy.org) 1.24+ |
| Visualizaciones | [Plotly](https://plotly.com/python/) 5.18+ |
| Contenedores | [Docker](https://www.docker.com/) |
| CI/CD | GitHub Actions → GitHub Pages |
| Notebooks | Jupyter |

### Esquema de datos

**Fuente:** [FIFA Football World Cup — Kaggle](https://www.kaggle.com/datasets/piterfm/fifa-football-world-cup)

| Archivo | Descripción | Columnas Clave |
|---------|-------------|----------------|
| `matches_limpio.csv` | Más de 1,000 partidos depurados | year, stage_clean, home_team, away_team, home_goals, away_goals, total_goals, attendance, city, stadium |
| `world_cup.csv` | Metadata por edición | Year, Host, Champion, Runner-Up, TopScorrer, Attendance, Matches |

> **Nota de Gobernanza de Datos:** Las cifras de asistencia anteriores a 1970 pueden contener inconsistencias metodológicas. Para proyecciones operativas se recomienda filtrar a **2010–2022**.

</details>

<details>
<summary><strong>Solución de Problemas</strong></summary>

### La app no abre en el navegador

Verifica que Streamlit esté corriendo y accede manualmente a `http://localhost:8501`. Si el puerto está ocupado:

```bash
streamlit run app.py --server.port 8502
```

### Error: `matches_limpio.csv` no encontrado (instalación local)

El CSV limpio se genera ejecutando el notebook EDA. Asegúrate de:
1. Tener `data/matches.csv` y `data/world_cup.csv` en la carpeta `data/`
2. Haber ejecutado **todas** las celdas de `notebooks/EDA.ipynb`
3. Verificar que `data/matches_limpio.csv` fue creado

Si no tienes los CSVs originales, la app entra automáticamente en **Modo Demo**.

### Docker: el contenedor no arranca

```bash
docker logs <container_id>   # ver qué falló
docker ps                    # ver contenedores corriendo
docker stop $(docker ps -q)  # detener todos
```

### Docker: puerto 8501 ya en uso

```bash
docker run -p 8502:8501 majorodri/world-cup-sync
```

Luego abrir `http://localhost:8502`.

### El Modo Demo muestra un banner de aviso

Es el comportamiento esperado. El banner `⚠️ Modo Demo` confirma que la app está corriendo con datos demo porque no encontró los CSVs privados. Todos los filtros y visualizaciones funcionan normalmente.

### Dependencias desactualizadas

```bash
pip install --upgrade -r requirements.txt
```

### Gráficos no renderizan / pantalla en blanco

Prueba con Chrome o Firefox. Streamlit no es compatible con Internet Explorer. Si el problema persiste, limpia la caché del navegador.

</details>

---

## Licencia

Este proyecto es de uso interno / analítico únicamente. Todos los datos del Mundial FIFA se utilizan con fines educativos y de investigación.

---

<div align="center">
  Hecho con pasión por el fútbol por <a href="https://github.com/MajoRodri">MajoRodri</a>
</div>
