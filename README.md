# Mundial 2026 — Modelo predictivo

Proyecto final del curso de Minería de Datos Avanzada. Construye, de forma reproducible, un modelo que
estima la probabilidad de que cada selección llegue a semifinales/final del Mundial 2026, y proyecta el
podio: campeón, subcampeón, 3° y 4° lugar.

La final del Mundial 2026 es el **19 de julio**; el corte de datos usado en este proyecto es el
**8 de julio de 2026**.

## Datos pesados (Google Drive)

Los archivos crudos y procesados (pesados) no se versionan en GitHub. Están en Drive:

<https://drive.google.com/drive/folders/1mqVbO1AZTUBDOBQJHlAVa-PVNf9ztFTO?usp=sharing>

Ver `data/README_DATA_LOCAL.md` para cómo descargarlos localmente antes de correr los notebooks, y
`documentacion_fuentes_mundial_2026.md` para el detalle de cada fuente (URL, cobertura, método de
descarga y limitaciones).

## Equipo y responsabilidades

| Integrante | Encargado de | Entrega |
|---|---|---|
| Persona 1 | Fuentes de datos | `documentacion_fuentes_mundial_2026.md` + archivos en Drive |
| Persona 2 | Limpieza y metodología CRISP-DM | `notebooks/01_limpieza_datos.ipynb` → dataset limpio |
| Persona 3 | Modelo predictivo | `notebooks/02_modelo_predictivo.ipynb` → predicción de podio |
| Persona 4 | Power BI e informe final | `notebooks/03_export_powerbi.ipynb` + `powerbi/dashboard_mundial_2026.pbix` |

## Estructura del repositorio

```text
.
├── README.md
├── documentacion_fuentes_mundial_2026.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_limpieza_datos.ipynb      # Persona 2: limpieza + CRISP-DM
│   ├── 02_modelo_predictivo.ipynb   # Persona 3: modelo + predicción
│   └── 03_export_powerbi.ipynb      # Persona 4: exportación para el dashboard
├── scripts/
│   └── convert_fifa_json_to_csv.py
├── outputs_powerbi/                 # CSVs livianos que alimentan el dashboard
└── powerbi/
    └── dashboard_mundial_2026.pbix
```

Los datos pesados (`data/raw/`, `data/opcional/`, `data/processed/`) viven solo en Drive y en tu copia
local dentro de `data/` (ignorada por git).

## Cómo correr el proyecto localmente

1. Crear entorno e instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Descargar los datos del Drive dentro de `data/` siguiendo `data/README_DATA_LOCAL.md`.
3. Correr `notebooks/01_limpieza_datos.ipynb` de principio a fin. Genera:
   - `data/processed/clean_model_dataset.csv`
   - `data/processed/team_features_2026.csv`
4. Continuar con `02_modelo_predictivo.ipynb` (Persona 3) y `03_export_powerbi.ipynb` (Persona 4).
