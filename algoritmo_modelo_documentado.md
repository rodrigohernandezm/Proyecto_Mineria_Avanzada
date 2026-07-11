# Algoritmo / Modelo documentado

## Proyecto final: Algoritmo predictivo para el Mundial de Fútbol 2026

Este documento describe el algoritmo utilizado para estimar las probabilidades de avance de las selecciones en el Mundial 2026 y proyectar el podio final: campeón, subcampeón, tercer lugar y cuarto lugar.

El modelo fue desarrollado en el notebook:

```text
notebooks/02_modelo_predictivo.ipynb
```

y utiliza como insumos principales los archivos procesados generados en la etapa de limpieza:

```text
data/processed/clean_model_dataset.csv
data/processed/team_features_2026.csv
```

Los resultados finales se exportan a la carpeta:

```text
outputs_powerbi/
```

---

## 1. Objetivo del modelo

El objetivo del modelo es transformar información histórica de partidos internacionales en probabilidades interpretables para cada selección participante del Mundial 2026.

El modelo estima:

- Probabilidad de avanzar a ronda de 32.
- Probabilidad de avanzar a octavos de final.
- Probabilidad de avanzar a cuartos de final.
- Probabilidad de avanzar a semifinales.
- Probabilidad de llegar a la final.
- Probabilidad de ser campeón.
- Probabilidad de terminar como subcampeón.
- Probabilidad de terminar en tercer lugar.
- Probabilidad de terminar en cuarto lugar.

A partir de estas probabilidades se genera una predicción del podio final.

---

## 2. Enfoque general del algoritmo

El proyecto utiliza un enfoque en dos etapas:

1. **Modelo supervisado de resultado de partido.**  
   Se entrena un modelo de clasificación con partidos internacionales históricos para estimar la probabilidad de tres posibles resultados:
   - victoria del equipo local o equipo A,
   - empate,
   - victoria del equipo visitante o equipo B.

2. **Simulación Monte Carlo del torneo.**  
   Con las probabilidades generadas por el modelo, se simulan miles de versiones del Mundial 2026. En cada simulación se juega fase de grupos, ronda de 32, octavos, cuartos, semifinales, partido por tercer lugar y final. Luego se agregan los resultados para obtener probabilidades finales por selección.

Este enfoque permite que la predicción no dependa de una única corrida aislada, sino del resumen estadístico de miles de escenarios posibles.

---

## 3. Datos de entrada

### 3.1 Dataset histórico de partidos

Archivo utilizado:

```text
data/processed/clean_model_dataset.csv
```

Este archivo contiene un registro por partido internacional histórico. Fue generado en el notebook de limpieza y contiene variables como:

| Variable | Descripción |
|---|---|
| `date` | Fecha del partido. |
| `home_team` | Selección local o equipo A. |
| `away_team` | Selección visitante o equipo B. |
| `home_score` | Goles del equipo local. |
| `away_score` | Goles del equipo visitante. |
| `result` | Resultado objetivo: `home_win`, `draw` o `away_win`. |
| `neutral` | Indica si el partido se jugó en sede neutral. |
| `tournament_tier` | Nivel de importancia del torneo. |
| `decided_by_penalties` | Indica si el partido fue definido por penales. |
| `home_form_points_avg` | Promedio reciente de puntos del equipo local. |
| `home_form_gf_avg` | Promedio reciente de goles a favor del equipo local. |
| `home_form_ga_avg` | Promedio reciente de goles en contra del equipo local. |
| `away_form_points_avg` | Promedio reciente de puntos del equipo visitante. |
| `away_form_gf_avg` | Promedio reciente de goles a favor del equipo visitante. |
| `away_form_ga_avg` | Promedio reciente de goles en contra del equipo visitante. |
| `home_elo_pre_match` | Rating Elo histórico del equipo local antes del partido. |
| `away_elo_pre_match` | Rating Elo histórico del equipo visitante antes del partido. |
| `elo_diff` | Diferencia de rating Elo entre ambos equipos. |
| `has_min_history` | Indica si ambos equipos tenían historial suficiente antes del partido. |

Este dataset contiene 49,505 partidos, de los cuales 48,191 fueron utilizados para entrenamiento final después de filtrar partidos con historial mínimo suficiente.

---

### 3.2 Dataset de selecciones para 2026

Archivo utilizado:

```text
data/processed/team_features_2026.csv
```

Este archivo contiene una fila por selección y representa la foto actual utilizada para simular el Mundial 2026.

| Variable | Descripción |
|---|---|
| `team` | Nombre normalizado de la selección. |
| `fifa_rank` | Posición en el ranking FIFA. |
| `fifa_points` | Puntos FIFA. |
| `confederation` | Confederación de la selección. |
| `elo_rating` | Rating Elo más reciente disponible. |
| `recent_points_avg` | Promedio reciente de puntos. |
| `recent_gf_avg` | Promedio reciente de goles a favor. |
| `recent_ga_avg` | Promedio reciente de goles en contra. |
| `last_match_date` | Fecha del último partido registrado. |

---

## 4. Variable objetivo

La variable objetivo del modelo es:

```text
result
```

Esta variable representa el resultado del partido desde la perspectiva del equipo local o equipo A.

Los valores posibles son:

| Clase | Significado |
|---|---|
| `home_win` | Gana el equipo local o equipo A. |
| `draw` | Empate. |
| `away_win` | Gana el equipo visitante o equipo B. |

En partidos empatados que fueron definidos por penales, el resultado se ajusta según el ganador de la tanda. Esto permite representar mejor los partidos de eliminación directa.

---

## 5. Variables predictoras utilizadas

Las variables usadas para entrenar el modelo fueron:

```python
FEATURES = [
    "neutral",
    "tournament_tier",
    "home_form_points_avg",
    "home_form_gf_avg",
    "home_form_ga_avg",
    "home_matches_played_before",
    "away_form_points_avg",
    "away_form_gf_avg",
    "away_form_ga_avg",
    "away_matches_played_before",
    "home_elo_pre_match",
    "away_elo_pre_match",
    "elo_diff",
]
```

Estas variables fueron seleccionadas porque representan tres dimensiones importantes:

| Dimensión | Variables |
|---|---|
| Contexto del partido | `neutral`, `tournament_tier` |
| Forma reciente | promedios recientes de puntos, goles a favor y goles en contra |
| Fuerza relativa | Elo de cada selección y diferencia Elo |

No se utilizaron los goles finales como variables predictoras porque son parte del resultado que se desea predecir.

---

## 6. Prevención de fuga de información

Una decisión importante del modelo fue evitar la fuga de información hacia el futuro.

Para ello:

- La forma reciente se calculó usando partidos anteriores al partido evaluado.
- Se utilizó `shift(1)` antes de calcular promedios móviles.
- El rating Elo se integró como rating previo al partido.
- El ranking FIFA de julio de 2026 no se usó para entrenar partidos históricos, porque representa una foto actual y no el ranking real de cada selección en fechas pasadas.
- Los partidos sin historial mínimo suficiente fueron excluidos del entrenamiento.

Esto permite que el modelo aprenda con información que habría estado disponible antes de cada partido histórico.

---

## 7. División de entrenamiento y validación

El dataset se ordenó cronológicamente por fecha y se dividió en:

| Conjunto | Porcentaje | Descripción |
|---|---:|---|
| Entrenamiento | 80% | Partidos históricos más antiguos. |
| Validación | 20% | Partidos más recientes. |

La validación cronológica es más adecuada para este problema que una división aleatoria, porque el modelo busca predecir partidos futuros a partir de información pasada.

El corte de validación se ubicó aproximadamente en junio de 2016.

---

## 8. Modelos evaluados

Se compararon tres modelos de clasificación:

| Modelo | Descripción |
|---|---|
| Regresión logística | Modelo lineal base, interpretable y útil como referencia. |
| Random Forest | Ensamble de árboles de decisión, robusto ante relaciones no lineales. |
| Gradient Boosting | Modelo de boosting basado en árboles, útil para capturar relaciones no lineales y mejorar desempeño predictivo. |

Los modelos fueron evaluados con dos métricas principales:

| Métrica | Interpretación |
|---|---|
| `log_loss` | Penaliza predicciones probabilísticas incorrectas. Menor valor indica mejor calibración probabilística. |
| `accuracy` | Porcentaje de predicciones correctas. Mayor valor indica mejor clasificación directa. |

---

## 9. Resultados de validación

Los resultados obtenidos fueron:

| Modelo | Log Loss | Accuracy |
|---|---:|---:|
| Gradient Boosting | 0.8746 | 0.6091 |
| Random Forest | 0.8996 | 0.5842 |
| Regresión logística | 0.9270 | 0.5530 |

El modelo seleccionado fue:

```text
gradient_boosting
```

Se seleccionó Gradient Boosting porque obtuvo el menor `log_loss` y la mayor exactitud entre los modelos evaluados.

---

## 10. Modelo seleccionado

El modelo final utilizado fue:

```python
HistGradientBoostingClassifier(
    max_iter=300,
    learning_rate=0.04,
    l2_regularization=0.05,
    random_state=42
)
```

Antes del modelo se aplicó imputación de valores faltantes mediante la mediana:

```python
SimpleImputer(strategy="median")
```

El modelo final fue reentrenado con todos los partidos históricos válidos para maximizar la información disponible antes de simular el torneo.

---

## 11. Cálculo de probabilidad de partido

Para simular un partido entre dos selecciones del Mundial 2026, se construye una fila con el mismo formato usado en entrenamiento.

Ejemplo conceptual:

```text
Equipo A vs Equipo B
```

El modelo recibe variables como:

- forma reciente del equipo A,
- forma reciente del equipo B,
- rating Elo del equipo A,
- rating Elo del equipo B,
- diferencia Elo,
- sede neutral,
- nivel de torneo.

Luego devuelve probabilidades para:

```text
home_win
draw
away_win
```

En la simulación del Mundial, los partidos se consideran neutrales y se usa un nivel de torneo alto porque corresponden al Mundial.

---

## 12. Simulación Monte Carlo del Mundial 2026

Después de entrenar el modelo, se ejecutó una simulación Monte Carlo con:

```text
5,000 simulaciones
```

La estructura simulada corresponde al formato de 48 selecciones:

1. 12 grupos de 4 selecciones.
2. Clasifican los dos primeros de cada grupo.
3. Clasifican los 8 mejores terceros.
4. Se juega ronda de 32.
5. Se juegan octavos de final.
6. Se juegan cuartos de final.
7. Se juegan semifinales.
8. Se juega partido por tercer lugar.
9. Se juega la final.

En cada simulación se registró hasta dónde llegó cada selección.

Al finalizar, las probabilidades se calcularon como:

```text
probabilidad = número de veces que ocurre el evento / número total de simulaciones
```

Por ejemplo:

```text
p_champion = veces que una selección fue campeona / 5000
```

---

## 13. Selecciones y grupos utilizados

El modelo lee la lista de clasificados desde:

```text
data/processed/world_cup_2026_teams.csv
```

Cuando este archivo existe, el simulador respeta los grupos definidos en esa fuente. En este proyecto se utilizó una lista de clasificados y grupos leída desde ese archivo.

Los grupos simulados fueron:

| Grupo | Selecciones |
|---|---|
| Grupo A | Mexico, South Korea, Czech Republic, South Africa |
| Grupo B | Switzerland, Canada, Qatar, Bosnia and Herzegovina |
| Grupo C | Brazil, Morocco, Scotland, Haiti |
| Grupo D | United States, Turkey, Australia, Paraguay |
| Grupo E | Germany, Ecuador, Ivory Coast, Curaçao |
| Grupo F | Netherlands, Japan, Sweden, Tunisia |
| Grupo G | Belgium, Iran, Egypt, New Zealand |
| Grupo H | Spain, Uruguay, Saudi Arabia, Cape Verde |
| Grupo I | France, Senegal, Norway, Iraq |
| Grupo J | Argentina, Austria, Algeria, Jordan |
| Grupo K | Portugal, Colombia, DR Congo, Uzbekistan |
| Grupo L | England, Croatia, Panama, Ghana |

---

## 14. Resultados principales del modelo

El archivo `team_probabilities.csv` contiene las probabilidades por selección.

Las primeras selecciones ordenadas por probabilidad de campeonato fueron:

| Selección | Prob. semifinal | Prob. final | Prob. campeón |
|---|---:|---:|---:|
| Argentina | 0.2854 | 0.1950 | 0.1400 |
| Spain | 0.2598 | 0.1744 | 0.1220 |
| France | 0.2344 | 0.1454 | 0.0992 |
| Portugal | 0.1998 | 0.1192 | 0.0650 |
| England | 0.1768 | 0.0976 | 0.0616 |
| Colombia | 0.1878 | 0.1072 | 0.0592 |

---

## 15. Predicción del podio

El podio se construyó tomando la selección con mayor probabilidad marginal para cada posición, evitando repetir equipos.

El resultado fue:

| Posición | Resultado | Selección | Probabilidad asociada |
|---:|---|---|---:|
| 1 | Campeón | Argentina | 0.1400 |
| 2 | Subcampeón | Portugal | 0.0542 |
| 3 | Tercer lugar | Spain | 0.0650 |
| 4 | Cuarto lugar | Norway | 0.0414 |

Este criterio permite generar una salida estable para Power BI, ya que no depende de una sola simulación individual, sino de probabilidades agregadas.

---

## 16. Archivos generados

El modelo genera los siguientes archivos:

| Archivo | Descripción |
|---|---|
| `outputs_powerbi/team_probabilities.csv` | Probabilidades de avance por selección. |
| `outputs_powerbi/predicted_podium.csv` | Podio proyectado del Mundial 2026. |
| `outputs_powerbi/model_metrics.csv` | Métricas comparativas de los modelos evaluados. |
| `outputs_powerbi/model_metadata.json` | Configuración general del modelo y simulación. |

Estos archivos son los insumos principales para el dashboard de Power BI.

---

## 17. Reproducibilidad

Para que el modelo sea reproducible se definió una semilla aleatoria:

```python
RANDOM_STATE = 42
```

Además:

- La división entrenamiento-validación es cronológica.
- Las simulaciones usan el mismo generador aleatorio.
- Los archivos de entrada y salida están definidos por rutas fijas dentro del proyecto.
- El modelo seleccionado queda registrado en `model_metadata.json`.
- El número de simulaciones queda documentado en `model_metadata.json`.

---

## 18. Limitaciones del modelo

El modelo es útil para generar una predicción basada en datos, pero tiene limitaciones:

1. **No incluye lesiones ni convocatorias finales.**  
   El modelo no conoce cambios de último momento en jugadores disponibles.

2. **No incluye tácticas ni alineaciones.**  
   La predicción se basa en datos agregados por selección, no en planteamientos específicos por partido.

3. **El ranking FIFA es una foto actual.**  
   Se usa para representar el estado de las selecciones en 2026, pero no como variable histórica de entrenamiento.

4. **El rating Elo disponible tiene desfase temporal.**  
   Aunque el archivo se usó como fuente Elo, el último rating real disponible en el dataset llega hasta diciembre de 2025.

5. **La simulación simplifica algunos criterios oficiales.**  
   Los desempates y cruces se representan de forma reproducible, pero pueden no capturar todos los detalles reglamentarios del torneo real.

6. **El empate es difícil de predecir.**  
   En la validación, el modelo tuvo menor desempeño identificando empates, lo cual es común en modelos de fútbol por la naturaleza incierta de este resultado.

---

## 19. Justificación del enfoque

El enfoque utilizado es adecuado para el proyecto porque combina:

- datos históricos de partidos,
- forma reciente de selecciones,
- fuerza relativa mediante Elo,
- comparación de modelos,
- validación cronológica,
- predicciones probabilísticas,
- simulación Monte Carlo,
- exportación de resultados para visualización.

Esto permite entregar un modelo documentado, reproducible y conectado con Power BI.

La predicción no se presenta como una certeza, sino como una estimación probabilística basada en los datos disponibles.

---

## 20. Resumen final

El modelo final utiliza Gradient Boosting para estimar probabilidades de resultado de partido. Estas probabilidades alimentan una simulación Monte Carlo de 5,000 torneos completos del Mundial 2026. A partir de las simulaciones se calculan probabilidades de avance por selección y se proyecta el podio final.

El resultado final del modelo fue:

```text
Campeón: Argentina
Subcampeón: Portugal
Tercer lugar: Spain
Cuarto lugar: Norway
```

Los resultados se exportaron en archivos CSV y JSON para ser utilizados en Power BI y documentar el proceso de manera reproducible.
