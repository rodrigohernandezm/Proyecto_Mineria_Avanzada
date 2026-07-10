# Mundial 2026 - Modelo predictivo

Proyecto final del curso de Mineria de Datos Avanzada. Construye, de forma reproducible, un modelo que
estima la probabilidad de que cada seleccion llegue a semifinales/final del Mundial 2026, y proyecta el
podio: campeon, subcampeon, 3er y 4o lugar.

La final del Mundial 2026 es el **19 de julio**; el corte de datos usado en este proyecto es el
**8 de julio de 2026**.

## Datos pesados (Google Drive)

Los archivos crudos y procesados pesados no se versionan en GitHub. Estan en Drive:

<https://drive.google.com/drive/folders/1mqVbO1AZTUBDOBQJHlAVa-PVNf9ztFTO?usp=sharing>

Ver `data/README_DATA_LOCAL.md` para como descargarlos localmente antes de correr los notebooks, y
`documentacion_fuentes_mundial_2026.md` para el detalle de cada fuente: URL, cobertura, metodo de
descarga y limitaciones.

## Equipo y responsabilidades

| Integrante | Encargado de | Entrega |
|---|---|---|
| Edgar Rolando Ramirez Lopez | Fuentes de datos | `documentacion_fuentes_mundial_2026.md` + archivos en Drive |
| Persona 2 | Limpieza y metodologia CRISP-DM | `notebooks/01_limpieza_datos.ipynb` -> dataset limpio |
| Persona 3 | Modelo predictivo | `notebooks/02_modelo_predictivo.ipynb` -> prediccion de podio y probabilidades |
| Persona 4 | Power BI e informe final | `notebooks/03_export_powerbi.ipynb` + `powerbi/dashboard_mundial_2026.pbix` |

## Estructura del repositorio

```text
.
|-- README.md
|-- documentacion_fuentes_mundial_2026.md
|-- requirements.txt
|-- .gitignore
|-- notebooks/
|   |-- 01_limpieza_datos.ipynb      # Persona 2: limpieza + CRISP-DM
|   |-- 02_modelo_predictivo.ipynb   # Persona 3: modelo + prediccion
|   `-- 03_export_powerbi.ipynb      # Persona 4: exportacion para el dashboard
|-- scripts/
|   `-- convert_fifa_json_to_csv.py
|-- outputs_powerbi/                 # CSVs livianos que alimentan el dashboard
`-- powerbi/
    `-- dashboard_mundial_2026.pbix
```

Los datos pesados (`data/raw/`, `data/opcional/`, `data/processed/`) viven solo en Drive y en tu copia
local dentro de `data/` (ignorada por git).

## Como correr el proyecto localmente

1. Crear entorno e instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Descargar los datos del Drive dentro de `data/` siguiendo `data/README_DATA_LOCAL.md`.
3. Correr `notebooks/01_limpieza_datos.ipynb` de principio a fin. Genera:
   - `data/processed/clean_model_dataset.csv`
   - `data/processed/team_features_2026.csv`
4. Correr `notebooks/02_modelo_predictivo.ipynb`. Genera:
   - `outputs_powerbi/team_probabilities.csv`
   - `outputs_powerbi/predicted_podium.csv`
   - `outputs_powerbi/model_metrics.csv`
   - `outputs_powerbi/model_metadata.json`
5. Continuar con `notebooks/03_export_powerbi.ipynb` y actualizar `powerbi/dashboard_mundial_2026.pbix`.

## Estado actual para Persona 4

Persona 3 ya fue ejecutada con los archivos procesados descargados del Drive:

- `data/processed/clean_model_dataset.csv`
- `data/processed/team_features_2026.csv`
- `data/processed/world_cup_2026_teams.csv`

El notebook `notebooks/02_modelo_predictivo.ipynb` entreno el modelo, evaluo varias alternativas y exporto
los archivos livianos para Power BI en `outputs_powerbi/`.

### Archivos que debe consumir Power BI

| Archivo | Uso sugerido en el dashboard |
|---|---|
| `outputs_powerbi/team_probabilities.csv` | Tabla principal por seleccion: probabilidades de avanzar a ronda de 32, octavos, cuartos, semifinal, final, campeon, subcampeon, tercer y cuarto lugar. |
| `outputs_powerbi/predicted_podium.csv` | Visual del podio proyectado: campeon, subcampeon, tercer lugar y cuarto lugar. |
| `outputs_powerbi/model_metrics.csv` | Tabla de respaldo metodologico: comparacion de modelos por `log_loss` y `accuracy`. |
| `outputs_powerbi/model_metadata.json` | Metadatos del experimento: modelo seleccionado, numero de simulaciones, escenario usado y archivos de entrada/salida. |

### Resultado actual del modelo

El mejor modelo seleccionado fue `gradient_boosting`.

Podio proyectado:

| Posicion | Seleccion | Probabilidad |
|---:|---|---:|
| 1 | Argentina | 0.1400 |
| 2 | Portugal | 0.0542 |
| 3 | Spain | 0.0650 |
| 4 | Norway | 0.0414 |

Metricas del mejor modelo:

- `log_loss`: 0.874594
- `accuracy`: 0.609088

### Escenario usado

Persona 3 ya usa `data/processed/world_cup_2026_teams.csv`, con 48 selecciones distribuidas en 12 grupos
de 4 equipos. El notebook respeta esos grupos para la fase de grupos y luego simula la eliminacion directa.

El archivo debe conservar estas columnas:

```text
group,team
```

Si se modifica algun grupo o seleccion, volver a ejecutar `notebooks/02_modelo_predictivo.ipynb` para
regenerar los CSV de `outputs_powerbi/` antes de actualizar Power BI.

## Recomendacion para el dashboard

Para Persona 4, el dashboard puede organizarse en cuatro vistas:

1. **Resumen del podio:** tarjetas o tabla con `predicted_podium.csv`.
2. **Probabilidades por seleccion:** ranking con `team_probabilities.csv`, ordenado por `p_champion`.
3. **Camino al titulo:** barras comparando `p_round32`, `p_round16`, `p_quarterfinal`, `p_semifinal`, `p_final` y `p_champion`.
4. **Metodologia:** tabla simple con `model_metrics.csv` y nota del escenario desde `model_metadata.json`.
