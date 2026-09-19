# 02 · Method Fit Matrix (Deliverable No. 2)

**Archivo:** `Method_Fit_Matrix_Deliverable_2_(Jesus_Inca).pdf`

## Resumen

Matriz de ajuste metodológico que compara cuatro enfoques candidatos para responder la pregunta de investigación acotada del proyecto sobre recomendación verificable de cláusulas contractuales.

### Pregunta de investigación acotada
¿Cómo diseñar y evaluar rigurosamente un artefacto de IA generativa verificable y human-in-the-loop para recomendar cláusulas contractuales, cuya salida sea siempre trazable a una fuente normativa/contractual contrastable, en una institución fiduciaria supervisada por la SBS y una tarea de recomendación de cláusulas acotada — y si supera a un baseline RAG estándar en verificabilidad y control de alucinaciones?

### Criterios de evaluación (y pesos)
| Criterio | Peso | Qué mide |
|---|---|---|
| E — Ajuste epistemológico | 30% | Coherencia con el paradigma DSR/realismo crítico |
| D — Viabilidad de datos | 20% | Posibilidad real de obtener datos bajo secreto bancario |
| F — Factibilidad | 15% | Viabilidad dentro de un doctorado de 3 años |
| C — Contribución | 20% | Generación de artefacto + conocimiento de diseño transferible |
| V — Ajuste de venue | 15% | Publicabilidad en revistas/conferencias objetivo |

### Resultados comparativos

| Método | Puntaje ponderado | Resultado |
|---|---|---|
| Experimento Puro | 2.80/5 (56/100) | Eliminado (falla en viabilidad de datos y factibilidad) |
| Estudio de Caso Puro | 2.50/5 (50/100) | Eliminado (débil en ajuste epistemológico y contribución) |
| Métodos Mixtos | 3.65/5 (73/100) | Viable como estrategia de evaluación, no como método rector |
| **Design Science Research** | **4.65/5 (93/100)** | **Seleccionado como método principal** |

**Regla de exclusión (gate rule):** cualquier candidato con puntaje ≤2 en un criterio crítico es eliminado. Bajo esta regla, Experimento Puro y Estudio de Caso Puro quedan descartados (ambos puntúan 2/5 en al menos un criterio clave: viabilidad de datos/factibilidad para el experimento, contribución para el caso de estudio).

### Decisión final
Se selecciona **Design Science Research (DSR)** como método principal. Métodos Mixtos se mantiene como estrategia de evaluación embebida dentro del ciclo DSR, pero no como método rector.

Para mantener la factibilidad dentro de tres años, el estudio DSR se acota a:
- **1** prototipo funcional
- **1** institución supervisada por la SBS
- **1** tarea de recomendación de cláusulas claramente delimitada
- **2–3** resultados primarios: calidad de verificabilidad/atribución, tasa de alucinación y calidad de recomendación

Se incluye una comparación controlada acotada contra un baseline RAG estándar, más baselines de no-recuperación y práctica institucional actual, junto con retroalimentación focalizada de expertos, todo embebido dentro del ciclo de evaluación DSR.

**Nota adicional:** el enfoque de simulación/datos sintéticos no se preselecciona como método principal (la afirmación central requiere verificabilidad contra fuentes normativas reales y auditabilidad institucional real), pero puede usarse para pruebas de estrés previas al despliegue sobre modos de fallo de alucinación y mala atribución.

### Fuentes de datos del plan DSR seleccionado
- Logs de interacción del prototipo
- Trazas de recuperación (pasajes recuperados por consulta)
- Cláusulas generadas con sus citas
- Etiquetas de precisión y recall de citación
- Juicios de atribuibilidad a nivel de fragmento
- Anotaciones de alucinación (no soportada, mal atribuida o contradictoria)
- Gold standard legal anotado
- Retroalimentación focalizada de abogados/especialistas

**Prerrequisitos:** autorización institucional, cumplimiento de secreto bancario (Ley 26702), protección de datos (Ley 29733), anonimización de textos contractuales, procesamiento local/on-premise cuando sea factible, y autoridad humana sobre cualquier cláusula adoptada.
