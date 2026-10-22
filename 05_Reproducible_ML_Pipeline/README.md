# Entregable 05 — Pipeline de ML reproducible (clasificación de tipo de cláusula)

**Objetivo:** demostrar que cualquier resultado reportado se puede volver a obtener *exactamente*,
por el autor o por un tercero. El número que importa no es la mejor corrida sino la **estabilidad
entre semillas** (media ± DE).

**Tarea:** predecir el tipo de cláusula de una disposición contractual (subconjunto de LEDGAR,
benchmark LexGLUE): 20 tipos × 150 cláusulas = 3 000 textos. Es el primer paso del artefacto de la
tesis: reconocer qué clase de cláusula se necesita antes de recomendar candidatas.

**Datos:** LEDGAR contiene disposiciones de contratos públicos (SEC EDGAR). No se usa ningún dato
institucional ni de clientes.

## Resultado principal

TF-IDF (1–2 gramas) + regresión logística, validación cruzada estratificada de 5 folds, 7 semillas
(7, 12, 21, 42, 101, 2026, 3407):

| Modelo | Macro-F1 (media ± DE, 7 semillas) | Accuracy (media ± DE) | Rango entre semillas |
|---|---|---|---|
| TF-IDF + LogReg | **0.9239 ± 0.0011** | 0.9235 ± 0.0011 | 0.30 pp |
| Baseline clase mayoritaria (B0) | 0.0048 ± 0.0000 | 0.0500 ± 0.0000 | 0.00 pp |

La mejor semilla (21) da 0.9257 de macro-F1, pero lo que se reporta es la media ± DE: el resultado no
depende de una corrida con suerte. Referencia de la semilla 42: accuracy 0.92367, macro-F1 0.92421.

Tabla completa: [`results/stability_table.md`](results/stability_table.md) · Figuras: [`figures/`](figures/)

## Cómo cada capa queda bajo control

| Capa | Riesgo que evita | Cómo se controla aquí |
|---|---|---|
| Código | No saber qué versión produjo el resultado | Git (historial de commits); el hash del commit se guarda en MLflow y en `results/manifest.json` |
| Datos | Que el dataset cambie sin notarlo | Revisión del Hub fijada en `params.yaml` + DVC (`dvc.lock` guarda el MD5 del CSV) |
| Aleatoriedad | Reportar una corrida con suerte | Semillas fijas, 7 semillas, media ± DE; `PYTHONHASHSEED=0` forzado; prueba de repetibilidad con la misma semilla (mismo proceso y procesos nuevos) |
| Experimentos | Perder qué parámetros dieron qué número | MLflow: una corrida padre `seed-study` con 14 corridas hijas (2 modelos × 7 semillas), parámetros, métricas, versiones y artefactos |
| Entorno | Que otra versión de una librería cambie el resultado | `requirements.txt` con versiones exactas + `Dockerfile` (Python 3.13.13, BLAS de un hilo) |
| Validez | Fuga de datos que infla el resultado | El TF-IDF está dentro del `Pipeline` de sklearn y se ajusta solo con el fold de entrenamiento; baseline de clase mayoritaria como control mínimo (B0) |
| Comunicación | Que nadie más sepa cómo correrlo | Este README + `src/verify_reproduction.py` (stranger test automático) |

## Estructura

```
params.yaml                 parámetros: revisión del Hub, 20 clases × 150, semilla de muestreo, 7 semillas
dvc.yaml / dvc.lock         pipeline prepare -> seeds y MD5 de cada dependencia y salida
src/prepare_data.py         construye data/ledgar_subset.csv (versionado por DVC) y data/dataset_card.json
src/train.py                pipeline sin fuga + CV estratificada para una semilla
src/run_seeds.py            estudio de 7 semillas, repetibilidad, MLflow, manifest, figuras
src/verify_reproduction.py  stranger test: compara una corrida nueva contra los resultados del repo
reference/expected_seed42.json  número de referencia (semilla 42) que toda corrida debe reproducir
results/                    métricas por fold y por semilla, tabla media ± DE, manifest.json
figures/                    fig1 accuracy/macro-F1 por semilla, fig2 todas las métricas, fig3 boxplot por fold
```

## Reproducir (stranger test)

### Opción A — Docker (recomendada: entorno idéntico)

```bash
git clone <url-del-repo> && cd 05_Reproducible_ML_Pipeline
docker build -t d5-repro .
docker run --rm d5-repro
```

El contenedor reconstruye el dataset desde la revisión fijada del Hub, verifica su MD5 contra
`dvc.lock`, vuelve a correr los 2 modelos × 7 semillas y los compara con `results/seed_summary.csv`.
Debe terminar con `REPRODUCED`.

### Opción B — Entorno local con DVC

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

dvc repro                                  # prepare -> seeds (descarga LEDGAR, ~5 min)
python src/verify_reproduction.py --full   # debe imprimir REPRODUCED
mlflow ui --backend-store-uri sqlite:///mlflow.db   # ver las corridas en http://127.0.0.1:5000
```

Comandos útiles:

```bash
dvc status            # ¿cambió algún dato, código o parámetro desde el último dvc.lock?
dvc metrics show      # media y DE de cada métrica (results/metrics.json)
python src/train.py --seed 42             # una sola semilla
python src/run_seeds.py --no-mlflow       # estudio de semillas sin registrar en MLflow
```

### Qué se considera "reproducido"

1. El MD5 de `data/ledgar_subset.csv` es igual al de `dvc.lock` (`bc995ef9bacb814a07d06dbecad47ad0`).
2. La semilla 42 da exactamente `reference/expected_seed42.json` (5 decimales).
3. Con `--full`, las 14 corridas coinciden con `results/seed_summary.csv` (diferencia ≤ 1e-12).

`run_seeds.py` también falla si la semilla 42 no coincide con la referencia; la referencia solo se
reemplaza a propósito con `--update-reference`.

## Notas metodológicas

- **Qué mide la varianza entre semillas.** La regresión logística (lbfgs) es determinista, así que la
  semilla cambia la partición de `StratifiedKFold`. La DE entre semillas es, por tanto, variabilidad
  por partición de los datos. La muestra de 3 000 cláusulas usa una semilla fija aparte (2026).
- **Hiperparámetros** (`C=4`, 1–2 gramas, `min_df=2`) están fijos en `src/train.py`; no hay búsqueda
  de hiperparámetros dentro de la validación cruzada.
- **Baseline de clase mayoritaria.** Con clases balanceadas da accuracy = 1/20 = 0.05; es la versión
  mínima del B0 de la tesis.
- **Remoto de DVC.** No hay un remoto configurado: el dataset se reconstruye byte por byte desde la
  revisión fijada del Hub y DVC verifica el MD5. Para compartir el caché, añadir uno con
  `dvc remote add -d storage <ruta-o-url>` y `dvc push`.

## Relación con la tesis (protocolo D3)

| Promesa del protocolo | Práctica en este entregable |
|---|---|
| k corridas por sistema con semillas fijas, reportando la varianza | 7 semillas, media ± DE, repetibilidad verificada |
| Snapshot fechado y versionado del corpus | Revisión del Hub fijada + DVC/MD5 |
| Prerregistro y versionado de prompts, semillas y artefactos | `params.yaml`, MLflow y `results/manifest.json` |
| Comparación contra baselines | Baseline de clase mayoritaria (B0 mínimo) |
