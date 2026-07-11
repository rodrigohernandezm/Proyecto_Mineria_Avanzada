# Guia de preparacion para la presentacion

## Contexto general del proyecto

El proyecto construye un modelo predictivo para el Mundial de Futbol 2026. El objetivo es estimar la probabilidad de que cada seleccion avance por las rondas principales y proyectar un podio: campeon, subcampeon, tercer lugar y cuarto lugar.

El corte de datos usado fue el 8 de julio de 2026. La final del Mundial 2026 esta programada para el 19 de julio de 2026, por lo que el proyecto busca generar una prediccion antes del cierre del torneo.

La presentacion debe dejar claro que no se trata de adivinar un resultado exacto, sino de construir un proceso reproducible con datos, limpieza, modelado, simulacion y visualizacion.

## Orden sugerido de exposicion

1. Persona 1: fuentes de datos.
2. Persona 2: limpieza, metodologia CRISP-DM y preparacion del dataset.
3. Persona 3: modelo predictivo, simulacion y resultados.
4. Persona 4: tablero de Power BI y visualizacion final.

Persona 4 presentara el tablero, pero todos deben estar listos para explicar la parte que les corresponde y responder dudas.

## Persona 1: fuentes de datos

La primera parte explica de donde salieron los datos y por que son utiles.

Fuentes principales:

- `results.csv`: historial de partidos internacionales.
- `shootouts.csv`: resultados de tandas de penales.
- `fifa_ranking_men_2026_07_08.csv`: ranking oficial FIFA consultado el 8 de julio de 2026.
- `elo_ratings_2026_07_08.csv`: ratings Elo por seleccion.

Fuentes opcionales documentadas:

- `goalscorers.csv`.
- Archivos de Transfermarkt: jugadores, apariciones, equipos nacionales y partidos.

Mensaje clave:

> Se usaron fuentes historicas, oficiales y estadisticas para construir una base justificable. Algunas fuentes opcionales quedaron documentadas, pero no se incorporaron al modelo base para evitar complejidad innecesaria.

## Persona 2: limpieza y preparacion

La segunda parte explica como los datos crudos se transformaron en archivos listos para modelar.

Principales pasos:

- Normalizacion de nombres de selecciones entre fuentes.
- Integracion de informacion de penales.
- Definicion del resultado del partido como variable objetivo: `home_win`, `draw` o `away_win`.
- Creacion de variables de forma reciente: puntos, goles a favor y goles en contra.
- Uso de variables de contexto, como sede neutral e importancia del torneo.
- Union del rating Elo historico antes de cada partido para evitar fuga de informacion.
- Exportacion de archivos procesados para Persona 3.

Archivos entregados:

- `data/processed/clean_model_dataset.csv`: dataset historico a nivel de partido.
- `data/processed/team_features_2026.csv`: foto actual por seleccion para simular el Mundial 2026.

Mensaje clave:

> La limpieza se hizo cuidando que el modelo solo usara informacion disponible antes de cada partido historico, evitando data leakage.

## Persona 3: modelo predictivo

Esta es tu parte principal.

### Objetivo de Persona 3

Transformar el dataset limpio en probabilidades interpretables y usar esas probabilidades para simular el Mundial 2026.

Tu idea central puede decirse asi:

> Mi parte toma los datos ya limpios, entrena varios modelos para predecir el resultado de un partido y luego usa el mejor modelo para simular miles de posibles Mundiales. Con eso obtenemos probabilidades por seleccion y un podio proyectado.

### Entradas usadas

El notebook principal es:

- `notebooks/02_modelo_predictivo.ipynb`

Entradas:

- `data/processed/clean_model_dataset.csv`
- `data/processed/team_features_2026.csv`
- `data/processed/world_cup_2026_teams.csv`, si existe, para respetar los 48 equipos y sus grupos.

### Orden logico de lo que se hizo

Si te preguntan cual fue el orden de trabajo de Persona 3, puedes explicarlo asi:

1. Primero recibi los archivos procesados por Persona 2, especialmente el dataset historico de partidos y la foto actual de selecciones para 2026.
2. Luego revise que las variables necesarias estuvieran disponibles: forma reciente, goles recientes, sede neutral, importancia del torneo y rating Elo.
3. Despues defini el problema como una prediccion de resultado de partido, con tres posibles clases: gana equipo A, empate o gana equipo B.
4. Luego separe los datos de forma cronologica para entrenar con partidos antiguos y validar con partidos mas recientes.
5. Despues entrene y compare tres modelos: regresion logistica, random forest y gradient boosting.
6. Luego seleccione el mejor modelo usando principalmente `log_loss`, porque el proyecto necesitaba probabilidades confiables.
7. Despues reentrene el mejor modelo con todos los partidos disponibles para aprovechar mas informacion historica.
8. Luego use ese modelo para simular el Mundial 2026 con 5,000 escenarios Monte Carlo.
9. Finalmente exporte los resultados para Power BI: probabilidades por seleccion, podio proyectado, metricas del modelo y metadatos.

Respuesta corta:

> El orden fue: recibir datos limpios, definir variables, entrenar modelos, evaluar, elegir el mejor, simular el torneo y exportar resultados para el tablero.

### Que se predice primero

El modelo no predice directamente "quien sera campeon". Primero predice el resultado probable de un partido entre dos selecciones.

El problema se plantea como clasificacion multiclase:

- Victoria del equipo A/local: `home_win`.
- Empate: `draw`.
- Victoria del equipo B/visitante: `away_win`.

Esto es importante porque el campeon se obtiene despues, mediante simulacion del torneo.

### Variables usadas por el modelo

Las variables principales fueron:

- `neutral`: indica si el partido fue en sede neutral.
- `tournament_tier`: importancia o nivel del torneo.
- Forma reciente del equipo local/equipo A:
  - puntos recientes promedio.
  - goles a favor recientes.
  - goles en contra recientes.
  - partidos previos jugados.
- Forma reciente del equipo visitante/equipo B:
  - puntos recientes promedio.
  - goles a favor recientes.
  - goles en contra recientes.
  - partidos previos jugados.
- Rating Elo previo del equipo A.
- Rating Elo previo del equipo B.
- Diferencia de Elo: `elo_diff`.

No se usan los goles finales del partido como variables predictoras porque esos goles son parte del resultado que se quiere predecir.

### Modelos comparados

Se probaron tres alternativas:

- Regresion logistica.
- Random forest.
- Gradient boosting.

La evaluacion se hizo con separacion cronologica: partidos antiguos para entrenar y partidos mas recientes para validar.

Esto es importante porque en problemas deportivos no conviene mezclar aleatoriamente todo el historico sin considerar el tiempo. La idea es acercarse mas a una situacion real: entrenar con el pasado y evaluar con partidos posteriores.

### Metrica usada

La metrica principal fue `log_loss`.

Por que:

- El proyecto no solo necesita acertar ganador.
- Necesita probabilidades razonables.
- `log_loss` penaliza cuando el modelo da mucha confianza a una prediccion incorrecta.

Tambien se reporto `accuracy`, pero como apoyo.

Resultados de comparacion:

| Modelo | log_loss | accuracy |
|---|---:|---:|
| Gradient boosting | 0.8746 | 0.6091 |
| Random forest | 0.8996 | 0.5842 |
| Regresion logistica | 0.9270 | 0.5530 |

Modelo seleccionado:

> `gradient_boosting`, porque obtuvo el menor `log_loss` y la mejor exactitud entre los modelos comparados.

### Reentrenamiento final

Despues de seleccionar el mejor modelo, se reentreno usando todos los partidos historicos disponibles del dataset limpio.

Cantidad de partidos usados en el entrenamiento final:

- 48,191 partidos.

Esto se hizo para aprovechar la mayor cantidad posible de informacion antes de simular el torneo.

### Simulacion del Mundial 2026

La simulacion usa Monte Carlo con:

- 5,000 simulaciones.
- 48 selecciones.
- 12 grupos de 4 equipos.
- Clasifican los dos primeros de cada grupo y los 8 mejores terceros.
- Luego se simula eliminacion directa desde ronda de 32.

En cada simulacion:

1. Se juegan los grupos.
2. Se asignan puntos.
3. Se eligen clasificados.
4. Se simulan cruces de eliminacion directa.
5. Se registra quien llega a cada ronda, final, campeon, subcampeon, tercer y cuarto lugar.

Mensaje clave:

> El podio no sale de una unica simulacion aislada. Sale del resumen de 5,000 escenarios posibles.

### Salidas generadas para Power BI

Persona 3 exporta archivos livianos para que Persona 4 los use en el tablero:

- `outputs_powerbi/team_probabilities.csv`: probabilidades por seleccion.
- `outputs_powerbi/predicted_podium.csv`: podio proyectado.
- `outputs_powerbi/model_metrics.csv`: comparacion de modelos.
- `outputs_powerbi/model_metadata.json`: configuracion del experimento.

### Resultado actual del modelo

Podio proyectado:

| Posicion | Seleccion | Probabilidad usada |
|---:|---|---:|
| 1 | Argentina | 0.1400 |
| 2 | Portugal | 0.0542 |
| 3 | Spain | 0.0650 |
| 4 | Norway | 0.0414 |

Interpretacion:

- Argentina aparece como campeon proyectado porque tiene la mayor probabilidad marginal de ser campeon.
- Portugal aparece como subcampeon por su probabilidad marginal de quedar segundo, evitando repetir equipos.
- Spain y Norway aparecen como tercer y cuarto lugar bajo el mismo criterio.

Importante:

> Las probabilidades no son certezas. Representan la frecuencia con la que cada seleccion alcanzo ese resultado dentro de las simulaciones.

### Como explicar tu parte en 1 minuto

Puedes decir:

> En mi parte trabaje el modelo predictivo. Use el dataset limpio de partidos historicos y entrene tres modelos: regresion logistica, random forest y gradient boosting. El objetivo era predecir el resultado de un partido como victoria, empate o derrota, usando variables como forma reciente, goles recientes, sede neutral, importancia del torneo y rating Elo previo.
>
> Para evaluar use una separacion cronologica, entrenando con partidos antiguos y validando con partidos mas recientes. La metrica principal fue log_loss porque nuestro objetivo era obtener buenas probabilidades, no solo acertar una clase. El mejor modelo fue gradient boosting, con log_loss de 0.8746 y accuracy de 0.6091.
>
> Luego reentrene ese modelo con todos los partidos disponibles y lo use para simular 5,000 veces el Mundial 2026. En cada simulacion se jugaron grupos y rondas eliminatorias. Finalmente exporte las probabilidades por seleccion y el podio proyectado para que se visualizaran en Power BI.

### Como explicar tu parte en 30 segundos

Puedes decir:

> Mi parte convierte los datos limpios en predicciones. Primero entrene modelos para estimar el resultado de cada partido. Compare regresion logistica, random forest y gradient boosting, y seleccione gradient boosting porque tuvo el mejor log_loss. Despues use ese modelo para simular 5,000 escenarios del Mundial 2026. De esas simulaciones salieron las probabilidades por seleccion y el podio que se muestra en el tablero.

## Preguntas probables para Persona 3

### Por que usaron log_loss y no solo accuracy?

Porque el proyecto necesita probabilidades. `accuracy` solo dice cuantas veces se acerto la clase final, pero no evalua si las probabilidades estan bien calibradas. `log_loss` castiga predicciones demasiado confiadas cuando son incorrectas.

### Por que seleccionaron gradient boosting?

Porque fue el modelo con mejor desempeno entre los comparados. Tuvo el menor `log_loss` y tambien la mejor `accuracy`.

### Que significa Monte Carlo?

Significa repetir muchas veces una simulacion con probabilidades. En este caso, se simulo el Mundial 5,000 veces para observar con que frecuencia cada seleccion avanzaba a cada ronda o ganaba el torneo.

### Por que el modelo no predice directamente el campeon?

Porque el campeon depende de muchos partidos y cruces. Primero se estima la probabilidad de cada partido; despues se simula la estructura del torneo para obtener campeon, finalistas y podio.

### Que limitaciones tiene el modelo?

Limitaciones principales:

- No incluye lesiones, convocatorias finales ni cambios tacticos de ultimo momento.
- El ranking FIFA es una foto del 8 de julio de 2026, no una serie historica completa.
- El Elo disponible tiene desfase respecto al corte de julio de 2026.
- El resultado depende tambien del calendario, cruces y eventos aleatorios del futbol.

Respuesta corta:

> Es un modelo basado en datos historicos y variables disponibles, no una garantia del resultado real.

### Que significa que Argentina tenga 0.1400 de probabilidad?

Significa que Argentina fue campeona en aproximadamente el 14% de las simulaciones realizadas.

### Por que el tercer lugar puede tener una probabilidad mayor que el subcampeon?

Porque cada posicion usa una probabilidad marginal distinta. Ser subcampeon, tercer lugar o cuarto lugar son eventos diferentes. El podio se construyo evitando repetir equipos y tomando el equipo mas probable para cada posicion.

### Que pasaria si cambian los grupos o equipos?

Se debe actualizar `world_cup_2026_teams.csv` y volver a ejecutar `notebooks/02_modelo_predictivo.ipynb` para regenerar los archivos de `outputs_powerbi/`.

## Persona 4: tablero Power BI

Persona 4 presenta el tablero y conecta los resultados con visualizaciones.

Archivos usados:

- `team_probabilities.csv`
- `predicted_podium.csv`
- `model_metrics.csv`
- `model_metadata.json`

Vistas sugeridas:

- Resumen del podio.
- Ranking de probabilidades por seleccion.
- Camino al titulo por ronda.
- Respaldo metodologico con metricas del modelo.

Mensaje clave:

> El tablero convierte las salidas del modelo en una visualizacion facil de interpretar para comparar selecciones, probabilidades y resultados esperados.

## Cierre sugerido de la presentacion

Como cierre de equipo:

> El proyecto integra las fases principales de mineria de datos: obtencion de fuentes, limpieza, preparacion, modelado, simulacion y visualizacion. El resultado es un pipeline reproducible que permite estimar probabilidades del Mundial 2026 y explicar de forma transparente como se construyo la prediccion.

## Recordatorio para practicar

Persona 3 debe tener claros estos numeros:

- Modelo elegido: `gradient_boosting`.
- Simulaciones: 5,000.
- Partidos usados en entrenamiento final: 48,191.
- Mejor `log_loss`: 0.8746.
- Mejor `accuracy`: 0.6091.
- Campeon proyectado: Argentina.
- Archivo principal de salida: `outputs_powerbi/team_probabilities.csv`.

Frase de seguridad:

> El valor del proyecto no esta en prometer que ese sera el resultado exacto, sino en mostrar una metodologia reproducible, basada en datos y probabilidades.
