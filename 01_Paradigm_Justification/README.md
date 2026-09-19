# 01 · Paradigm Justification (Deliverable No. 1)

**Archivo:** `Epistemological_Statement.pdf`

## Resumen

Declaración de justificación del paradigma epistemológico para la tesis doctoral *"A Verifiable Generative Artificial Intelligence Model for Contractual Clause Recommendation in Regulated Fiduciary Institutions"*.

### Paradigma adoptado
- **Design Science Research (DSR)**, fundamentado filosóficamente en **realismo crítico** (Bhaskar), en lugar del pragmatismo habitual en DSR.
- Distingue los dominios de lo *real* (mecanismos generativos: marco regulatorio SBS, lógica legal de cláusulas, comportamiento del modelo), lo *actual* (eventos como la generación de una cláusula o una alucinación) y lo *empírico* (lo observable/medible por el investigador).

### Por qué realismo crítico y no pragmatismo
1. El objeto de estudio es genuinamente estratificado (mecanismos causales reales aunque no se observen).
2. La verificabilidad exige un fundamento independiente de la mente (la norma o cláusula fuente debe existir con contenido propio).
3. El fallibilismo encaja con un artefacto estocástico evaluado contra un estándar legal contestable ("objetividad modificada").

### Pregunta de investigación preliminar
- **Principal:** ¿Cómo diseñar un artefacto de IA generativa verificable para recomendar cláusulas contractuales de modo que toda recomendación sea trazable a una fuente normativa/contractual contrastable, y supera dicho artefacto a un baseline RAG estándar en verificabilidad y control de alucinaciones sin perder calidad?
- **RQ1 (diseño):** principios de diseño para un artefacto de recomendación de cláusulas verificable en un entorno fiduciario supervisado por la SBS.
- **RQ2 (evaluación):** ¿logra el artefacto mayor calidad de atribución y menor tasa de alucinaciones que (a) baseline sin recuperación, (b) RAG estándar y (c) práctica institucional actual, manteniendo la calidad de recomendación?

### Datos, métodos y contribución
- **Datos:** corpus anonimizado de contratos/cláusulas fiduciarias, corpus regulatorio (normas SBS, Ley 26702) y un gold standard anotado.
- **Métodos:** ciclo DSR de Peffers et al. (2007), con evaluación cuantitativa mediante comparación controlada y anotación humana.
- **Contribución dual** (Gregor & Hevner, 2013): principios de diseño prescriptivos + evidencia empírica del efecto de una capa explícita de verificabilidad.
- **Venues objetivo:** MIS Quarterly, JAIS, EJIS, DESRIST; Artificial Intelligence and Law, ICAIL/JURIX; venues de NLP sobre atribución y factualidad.

### Operacionalización de la verificabilidad
- Basada en el concepto de *atribución* (Rashkin et al., 2023): una proposición es atribuible a una fuente si un lector razonable afirmaría "Según P, s".
- Métricas: *citation precision/recall* (Gao et al., 2023) y juicios humanos de atribuibilidad a nivel de fragmento (span-level).
- Alucinación definida como: (i) no atribuible, (ii) mal atribuida, o (iii) contradictoria con el marco regulatorio.

### Gold standard y análisis estadístico
- Construido por al menos 2-3 abogados especializados en materia fiduciaria/regulación financiera, con acuerdo inter-anotador (Cohen's κ o Krippendorff's α ≥ 0.67, idealmente ≥ 0.80).
- Comparación de 4 condiciones: B0 (sin recuperación), B1 (RAG estándar), B2 (artefacto propuesto), B3 (práctica institucional actual).
- Pruebas pareadas (McNemar, bootstrap pareado), corrección de error por comparaciones múltiples (Holm–Bonferroni / Benjamini–Hochberg), reporte de tamaños de efecto e intervalos de confianza.

### Riesgo legal y supervisión humana
- Marco legal aplicable: secreto bancario (Ley 26702, art. 140) y protección de datos personales (Ley 29733).
- Implicaciones de diseño: anonimización/pseudonimización de datos, preferencia por despliegue local/on-premise, y evaluación de impacto de protección de datos si hay procesamiento externo.
- El artefacto es **explícitamente asesor**: la autoridad final sobre cualquier cláusula adoptada recae en un oficial legal calificado.

### Transferibilidad y novedad
- Transferibilidad reclamada como generalización analítica (principios de diseño), no estadística, validada por panel de expertos y, de ser posible, una segunda instanciación.
- La afirmación de que no existe un modelo similar en la literatura ni en el Estado peruano se sustentará con una revisión sistemática estilo PRISMA (Scopus, Web of Science, IEEE Xplore, ACL Anthology, SSRN).

### Tensión abierta
Verificabilidad ≠ corrección: una cláusula puede ser perfectamente atribuible a una fuente desactualizada o legalmente errónea. La tesis tratará la corrección como una dimensión distinta de la atribución, y declarará la verificabilidad como condición necesaria pero no suficiente.
