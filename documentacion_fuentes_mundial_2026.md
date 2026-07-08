# Documentación de fuentes de datos

## Proyecto final: Algoritmo predictivo para el Mundial de Fútbol 2026

**Curso:** Minería de Datos Avanzada  

---

## 1. Propósito del documento

Este documento describe las fuentes de datos utilizadas para el proyecto final, cuyo objetivo es construir un modelo predictivo para estimar la probabilidad de que cada selección llegue a semifinales, final y posiciones del podio en el Mundial de Fútbol 2026.

La documentación incluye el origen de los datos, archivos utilizados, cobertura temporal, método de descarga, variables principales y limitaciones. Esta información servirá como respaldo para el proceso metodológico CRISP-DM y para justificar las decisiones tomadas en la construcción del modelo.

---

## 2. Estructura de carpetas

La carpeta de datos se organizó de la siguiente manera:

```text
datos_proyecto_mundial_2026/
│
├── raw/
│   ├── results.csv
│   ├── shootouts.csv
│   ├── goalscorers.csv
│   ├── fifa_ranking_men_2026_07_08.json
│   ├── fifa_ranking_men_2026_07_08.csv
│   └── elo_ratings_2026_07_08.csv
│
├── opcional/
│   ├── national_teams.csv
│   ├── players.csv
│   ├── appearances.csv
│   └── games.csv
│
└── documentacion_fuentes.md
```

> **Nota:** Si el archivo FIFA se maneja únicamente en CSV dentro del repositorio, debe conservarse como archivo procesado. El JSON original se recomienda mantener porque corresponde a la fuente cruda descargada desde FIFA.

---

## 3. Inventario de archivos entregados

| Carpeta | Archivo | Descripción | Uso dentro del proyecto |
|---|---|---|---|
| `raw/` | `results.csv` | Historial de partidos internacionales entre selecciones. | Dataset principal para calcular rendimiento histórico, resultados recientes, goles a favor, goles en contra y desempeño por torneo. |
| `raw/` | `shootouts.csv` | Resultados de tandas de penales en partidos internacionales. | Complemento para definir ganadores en partidos de eliminación directa que terminaron empatados. |
| `raw/` | `goalscorers.csv` | Registro de goleadores en partidos internacionales. | Fuente complementaria para analizar capacidad ofensiva, penales y autogoles. |
| `raw/` | `fifa_ranking_men_2026_07_08.json` | Archivo original obtenido desde la carga dinámica de la página oficial de FIFA. | Fuente cruda del ranking FIFA masculino. |
| `raw/` | `fifa_ranking_men_2026_07_08.csv` | Versión tabular generada a partir del JSON oficial de FIFA. | Variable oficial de fuerza relativa: ranking FIFA, puntos FIFA y movimiento en ranking. |
| `raw/` | `elo_ratings_2026_07_08.csv` | Tabla de ratings Elo por selección. | Variable estadística independiente para medir fuerza deportiva. |
| `opcional/` | `national_teams.csv` | Información general de selecciones nacionales. | Fuente opcional para enriquecer información por país, selección o confederación. |
| `opcional/` | `players.csv` | Información de jugadores. | Fuente opcional para variables de plantilla, jugadores y valor de mercado. |
| `opcional/` | `appearances.csv` | Apariciones de jugadores en partidos. | Fuente opcional para analizar participación, experiencia y minutos o presencia de jugadores. |
| `opcional/` | `games.csv` | Registro de partidos de Transfermarkt. | Fuente opcional para contraste de partidos, clubes, selecciones o contexto adicional. |

---

## 4. Fuentes de datos utilizadas

| Fuente | URL | Archivo utilizado | Cobertura temporal | Método de descarga | Variables principales | Limitaciones |
|---|---|---|---|---|---|---|
| International football results, Mart Jürisoo | <https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017> | `results.csv`, `shootouts.csv`, `goalscorers.csv` | 1872–2026, según la versión descargada del dataset. | Descarga directa desde Kaggle/GitHub en formato CSV. | Fecha, selección local, selección visitante, goles, torneo, ciudad, país, sede neutral, penales y goleadores. | No incluye lesiones, alineaciones completas, datos tácticos, convocatorias finales ni estado físico de jugadores. |
| FIFA/Coca-Cola Men’s World Ranking | <https://inside.fifa.com/fifa-world-ranking/men> | `fifa_ranking_men_2026_07_08.json` y `fifa_ranking_men_2026_07_08.csv` | Ranking consultado el 8 de julio de 2026. | Extracción desde la solicitud dinámica de la página oficial de FIFA mediante Network/Fetch-XHR del navegador. El JSON fue convertido posteriormente a CSV. | Selección, código de país, ranking actual, ranking anterior, movimiento, puntos FIFA, puntos anteriores, confederación y partidos evaluados. | FIFA no ofrece descarga directa en CSV desde la interfaz pública; por ello se guardó el JSON cargado dinámicamente y se transformó a CSV. |
| World Football Elo Ratings | <https://www.eloratings.net/> | `elo_ratings_2026_07_08.csv` | Ranking Elo consultado el 8 de julio de 2026. | Extracción de tabla web y guardado en formato CSV. | Selección, ranking Elo, rating Elo y confederación. | No es ranking oficial FIFA; funciona como una medida estadística independiente de fuerza deportiva. |
| Transfermarkt Datasets | <https://github.com/dcaribou/transfermarkt-datasets> | `national_teams.csv`, `players.csv`, `appearances.csv`, `games.csv` | Dataset actualizado periódicamente; fecha de descarga: 8 de julio de 2026. | Descarga desde repositorio/dataset público. | Selecciones, jugadores, apariciones, partidos, valores de mercado y datos complementarios. | Los valores de mercado son estimaciones y pueden no representar directamente el rendimiento deportivo. Esta fuente se mantiene como opcional. |

---

## 5. Proceso de obtención de datos

### 5.1 International football results

Se descargaron los archivos `results.csv`, `shootouts.csv` y `goalscorers.csv` del dataset **International football results**.

El archivo `results.csv` será utilizado como base principal del análisis, ya que contiene el historial de partidos internacionales entre selecciones, incluyendo marcador, torneo, fecha, país y condición de sede neutral.

Los archivos `shootouts.csv` y `goalscorers.csv` serán utilizados como apoyo. El primero permite identificar ganadores en partidos definidos por penales, mientras que el segundo puede emplearse para analizar información ofensiva cuando sea necesario.

### 5.2 FIFA Ranking

La fuente oficial de ranking FIFA fue obtenida desde la página **FIFA/Coca-Cola Men’s World Ranking**.

Debido a que la interfaz pública no ofrece descarga directa en CSV, se inspeccionó la carga dinámica de la página mediante la pestaña **Network** del navegador. La respuesta JSON obtenida fue guardada como:

```text
fifa_ranking_men_2026_07_08.json
```

Posteriormente, ese archivo fue transformado a CSV para facilitar su uso en Power BI, Python y el modelo predictivo. El archivo procesado generado fue:

```text
fifa_ranking_men_2026_07_08.csv
```

El archivo CSV contiene una fila por selección y columnas como ranking actual, ranking anterior, movimiento en ranking, puntos FIFA, confederación y partidos evaluados.

### 5.3 World Football Elo Ratings

La fuente **World Football Elo Ratings** fue utilizada como medida estadística complementaria para representar la fuerza deportiva de cada selección.

Los ratings Elo permiten comparar equipos con base en su rendimiento histórico y reciente. Esta fuente no sustituye al ranking FIFA, sino que se utiliza como variable adicional para fortalecer el modelo predictivo.

El archivo fue guardado como:

```text
elo_ratings_2026_07_08.csv
```

### 5.4 Transfermarkt Datasets

Los archivos de Transfermarkt fueron colocados en la carpeta `opcional/` porque pueden enriquecer el modelo con información adicional de selecciones, jugadores, apariciones y partidos.

Los archivos incluidos son:

```text
national_teams.csv
players.csv
appearances.csv
games.csv
```

Estos datos deben utilizarse únicamente si el equipo decide incorporar variables relacionadas con valor de plantilla, experiencia de jugadores, participación en partidos o información individual. En caso contrario, permanecerán como respaldo documental y no como fuente principal del modelo.

---

## 6. Variables sugeridas para el modelo

| Variable | Fuente | Uso sugerido |
|---|---|---|
| Victorias recientes | `results.csv` | Medir forma reciente de cada selección. |
| Derrotas recientes | `results.csv` | Identificar tendencia negativa de rendimiento. |
| Empates recientes | `results.csv` | Medir estabilidad competitiva. |
| Goles a favor | `results.csv` | Evaluar capacidad ofensiva. |
| Goles en contra | `results.csv` | Evaluar solidez defensiva. |
| Diferencia de goles | `results.csv` | Medir balance general de rendimiento. |
| Torneo | `results.csv` | Diferenciar partidos amistosos, clasificatorios, copas continentales y Mundial. |
| Sede neutral | `results.csv` | Ajustar posible ventaja de localía. |
| Ranking FIFA | `fifa_ranking_men_2026_07_08.csv` | Variable oficial de posición relativa. |
| Puntos FIFA | `fifa_ranking_men_2026_07_08.csv` | Medida oficial de fuerza acumulada. |
| Movimiento en ranking | `fifa_ranking_men_2026_07_08.csv` | Indicar mejora o caída reciente en clasificación FIFA. |
| Rating Elo | `elo_ratings_2026_07_08.csv` | Medida estadística de fuerza deportiva. |
| Confederación | FIFA / Elo / Transfermarkt | Agrupar equipos por región competitiva. |
| Valor de plantilla | `players.csv`, opcional | Aproximar calidad económica/deportiva de la plantilla. |
| Apariciones de jugadores | `appearances.csv`, opcional | Medir experiencia o participación acumulada. |
| Información de partidos | `games.csv`, opcional | Contrastar resultados o enriquecer contexto. |

---

## 7. Limitaciones generales de los datos

Los datos utilizados permiten construir un modelo reproducible y justificable, pero presentan algunas limitaciones.

En primer lugar, los datasets históricos no incluyen información completa sobre lesiones, estado físico de jugadores, cambios tácticos, convocatorias finales o decisiones técnicas de último momento.

En segundo lugar, el ranking FIFA y el rating Elo representan aproximaciones de fuerza deportiva, pero no garantizan resultados en partidos individuales.

En tercer lugar, los datos de Transfermarkt, si se utilizan, deben interpretarse con cautela porque los valores de mercado son estimaciones económicas y no necesariamente reflejan rendimiento deportivo inmediato.

Finalmente, existe una diferencia entre datos históricos y el contexto real del torneo. Por ello, el modelo debe entenderse como una herramienta predictiva basada en datos disponibles, no como una predicción exacta del resultado final.

---

## 8. Archivos principales y archivos opcionales

Para evitar complejidad innecesaria en el modelo, se recomienda separar las fuentes en dos grupos.

### Archivos principales

Estos archivos deberían utilizarse directamente para el modelo base:

```text
results.csv
shootouts.csv
fifa_ranking_men_2026_07_08.csv
elo_ratings_2026_07_08.csv
```

### Archivos complementarios

Estos archivos pueden utilizarse si el equipo desea enriquecer el modelo:

```text
goalscorers.csv
national_teams.csv
players.csv
appearances.csv
games.csv
```

---

## 9. Conclusión sobre la selección de fuentes

Las fuentes seleccionadas cubren tres dimensiones importantes para el modelo predictivo.

El dataset **International football results** proporciona la base histórica de resultados entre selecciones. El ranking FIFA aporta una medida oficial de posicionamiento internacional. El rating Elo incorpora una medida estadística independiente de fuerza deportiva. Adicionalmente, los datos de Transfermarkt quedan disponibles como fuente opcional para enriquecer el modelo con información de plantilla, jugadores, apariciones y partidos.

Esta combinación permite justificar el modelo con datos históricos, oficiales y estadísticos, cumpliendo con el requisito de documentar el origen, cobertura, método de descarga y limitaciones de las fuentes utilizadas.

---

## 10. Recomendación para el equipo

Para una primera versión del modelo, se recomienda trabajar únicamente con:

```text
results.csv
shootouts.csv
fifa_ranking_men_2026_07_08.csv
elo_ratings_2026_07_08.csv
```

Los archivos de Transfermarkt pueden incorporarse después si el equipo dispone de tiempo suficiente para limpiar, relacionar y validar correctamente las variables adicionales.
