# Justificación de Cálculos - Planificación de Capacidad AGUNSA Europa

Este documento explica de manera sencilla cómo se calculan las Unidades de Predicción Natural (UPN) y los recursos de infraestructura necesarios para la plataforma de Inteligencia Competitiva y Vigilancia Tecnológica.

---

## 1. Unidades de Predicción Natural (UPN)

Las UPN son las "cosas" que crecen en el sistema y que generan demanda de recursos. Cada una tiene su propia forma de crecer en el tiempo.

### 1.1. Fuente de Información

**¿Qué es?** Cada sitio web, API, repositorio científico, base de patentes o boletín regulatorio que la plataforma monitorea automáticamente.

**¿Cómo crece?** Empieza con 300 fuentes en diciembre de 2025. Tiene un crecimiento mensual del 1,2% (crecimiento exponencial suave) y además recibe "saltos" o "olas" cuando se incorporan nuevas fuentes en momentos específicos:
- Mes 3: +40 fuentes (marzo 2026)
- Mes 9: +50 fuentes (septiembre 2026)
- Mes 15: +60 fuentes (marzo 2027)
- Mes 21: +60 fuentes (septiembre 2027)

**Ecuación:**
```
Fuentes(mes) = 300 × (1,012)^mes + saltos acumulados
```

**¿Por qué crece así?** El crecimiento exponencial refleja la expansión gradual del negocio, mientras que los saltos representan momentos donde AGUNSA expande operaciones a nuevos países o sectores, incorporando de golpe múltiples fuentes de información.

---

### 1.2. Documento Recolectado

**¿Qué es?** Cada ítem individual de información que entra al repositorio: papers científicos, noticias, patentes, reportes, fichas tecnológicas, etc.

**¿Cómo crece?** Empieza con 18.000 documentos por mes en diciembre de 2025. El objetivo es llegar a 42.000 documentos por mes hacia finales de 2027. El crecimiento combina:
- Un factor de crecimiento exponencial que lleva de 18k a 42k en 24 meses
- Una dependencia parcial del número de fuentes (a más fuentes, más documentos)

**Ecuación:**
```
Factor de crecimiento = (42.000 / 18.000)^(1/24)
Documentos(mes) = 18.000 × (factor)^mes × (Fuentes(mes) / 300)^0,25
Documentos acumulados = 50.000 (históricos) + suma de todos los documentos mensuales
```

**¿Por qué crece así?** Los documentos crecen más rápido que las fuentes porque cada fuente puede generar múltiples documentos. El factor 0,25 significa que el crecimiento de documentos es moderadamente influenciado por el número de fuentes (no es proporcional 1:1, sino que hay un efecto de "rendimientos decrecientes").

---

### 1.3. Tecnología Verde Registrada

**¿Qué es?** Cada categoría única de tecnología sustentable identificada y normalizada en el sistema. Por ejemplo: "energía solar fotovoltaica", "hidrógeno verde", "captura de carbono", etc.

**¿Cómo crece?** Empieza con 100 categorías en diciembre de 2025. Tiene un crecimiento mensual del 1% y recibe saltos cuando aparecen nuevas oleadas tecnológicas:
- Mes 12: +15 categorías (diciembre 2026)
- Mes 18: +20 categorías (junio 2027)
- Mes 22: +15 categorías (octubre 2027)

**Ecuación:**
```
Tecnologías(mes) = 100 × (1,01)^mes + saltos acumulados
```

**¿Por qué crece así?** El crecimiento suave refleja la consolidación gradual de nuevas tecnologías, mientras que los saltos representan momentos donde aparecen innovaciones disruptivas que obligan a crear nuevas categorías en la ontología tecnológica del sistema.

---

### 1.4. Iniciativa de la Competencia Monitoreada

**¿Qué es?** Cada proyecto o iniciativa sostenible de empresas competidoras que AGUNSA sigue activamente (programas de descarbonización, inversiones en energías limpias, certificaciones, etc.).

**¿Cómo crece?** Empieza con 80 iniciativas en diciembre de 2025. Tiene un crecimiento mensual del 2% y recibe saltos cuando se incorporan nuevos grupos de iniciativas:
- Mes 6: +18 iniciativas (junio 2026)
- Mes 14: +22 iniciativas (febrero 2027)
- Mes 20: +28 iniciativas (agosto 2027)

**Ecuación:**
```
Iniciativas(mes) = 80 × (1,02)^mes + saltos acumulados
```

**¿Por qué crece así?** Refleja que cada mes nuevas empresas anuncian programas ASG o se suman a acuerdos climáticos. Los saltos pueden ocurrir en épocas de cumbres climáticas o cuando se descubren nuevos competidores relevantes.

---

### 1.5. Sesión de Usuario Concurrente

**¿Qué es?** El número máximo de usuarios que están usando la plataforma simultáneamente en un momento dado.

**¿Cómo crece?** Empieza con 40 sesiones concurrentes pico en diciembre de 2025. Tiene un crecimiento base mensual del 3%, pero además se le aplica una estacionalidad que simula:
- Picos durante horarios de oficina europeos
- Bajones nocturnos y en fines de semana
- Variaciones mensuales y trimestrales (cierres de reportes, comités)

**Ecuación:**
```
Sesiones base(mes) = 40 × (1,03)^mes
Estacionalidad = 1 + 0,18 × sin(2π × mes / 12) + 0,05 × sin(4π × mes / 12)
Sesiones(mes) = Sesiones base × Estacionalidad
```

**¿Por qué crece así?** El crecimiento base refleja la adopción progresiva de la plataforma por más usuarios. La estacionalidad simula los patrones reales de uso: más usuarios durante el día laboral europeo, menos en la noche, y picos adicionales en épocas de reportes trimestrales.

---

## 2. Cálculo de Recursos de Infraestructura

Los recursos se calculan como una combinación de las UPN, porque cada UPN consume diferentes tipos de recursos según su naturaleza.

### 2.1. CPU (Procesamiento)

**¿Qué representa?** Las horas de procesamiento del servidor necesarias cada mes para ejecutar todas las tareas: scraping, indexación, análisis y atención a usuarios.

**¿Cómo se calcula?** Se suman cuatro componentes principales:

1. **CPU por scraping de fuentes:** Cada 100 fuentes requieren aproximadamente 0,9 horas de CPU al mes para hacer las consultas periódicas.
   ```
   CPU_scraping = 0,9 × (Fuentes / 100)
   ```

2. **CPU por indexación de documentos:** Cada 1.000 documentos nuevos requieren aproximadamente 1,5 horas de CPU para ser indexados y analizados.
   ```
   CPU_indexing = 0,0015 × Documentos_mes
   ```

3. **CPU por análisis de tecnologías e iniciativas:** Las tecnologías verdes y las iniciativas de competidores requieren análisis comparativos y cálculos de ranking.
   ```
   CPU_analytics = 0,08 × (Tecnologías / 50) + 0,05 × (Iniciativas / 50)
   ```

4. **CPU por sesiones de usuario:** Cada 50 sesiones concurrentes requieren aproximadamente 0,12 horas de CPU para mantener las conexiones y procesar consultas.
   ```
   CPU_sessions = 0,12 × (Sesiones / 50)
   ```

**Total de CPU:**
```
CPU_componentes = CPU_scraping + CPU_indexing + CPU_analytics + CPU_sessions
```

Luego, estos componentes se normalizan (se escalan entre 0 y 1) y se mapean a un uso de CPU que va del 10% al 70% de la capacidad total del cluster (5.200 horas/mes disponibles):
```
CPU_saturación = 10% + (normalización × 60%)
CPU_total = CPU_saturación × 5.200 horas/mes
```

**¿Por qué estos valores?** Los coeficientes (0,9, 0,0015, etc.) se estimaron basándose en:
- La frecuencia de actualización de fuentes (al menos cada 24 horas)
- El tiempo promedio de indexación por documento (considerando análisis semántico)
- La complejidad de los cálculos comparativos
- La carga típica de mantener sesiones de usuario activas

---

### 2.2. Almacenamiento

**¿Qué representa?** El espacio en disco (en GB o TB) necesario para almacenar todos los documentos, sus metadatos, embeddings y los índices de búsqueda.

**¿Cómo se calcula?** Se suman tres componentes:

1. **Almacenamiento de documentos:** Cada documento ocupa aproximadamente 0,45 MB (incluyendo texto, metadatos y vectores de embedding). Se multiplica por el total acumulado de documentos.
   ```
   Almacenamiento_docs = Documentos_acumulados × 0,00045 GB
   ```

2. **Almacenamiento de índices:** Las tecnologías verdes y las iniciativas generan estructuras de datos adicionales (ontologías, grafos de conocimiento) que ocupan espacio.
   ```
   Almacenamiento_índices = 0,0009 × Tecnologías + 0,0004 × Iniciativas
   ```

3. **Almacenamiento base del sistema:** 5 GB para el sistema operativo, logs y componentes base.
   ```
   Almacenamiento_total = 5 GB + Almacenamiento_docs + Almacenamiento_índices
   ```

**¿Por qué estos valores?** El tamaño promedio de 0,45 MB por documento considera:
- Texto completo del documento (papers, noticias, etc.)
- Metadatos (fecha, fuente, categorías, etc.)
- Vectores de embedding para búsqueda semántica (típicamente 768 o 1536 dimensiones)
- Índices invertidos para búsqueda rápida

---

### 2.3. Ancho de Banda (Red)

**¿Qué representa?** Los gigabytes de datos transferidos por mes, tanto entrantes (descarga de documentos y consultas a APIs) como salientes (respuestas a usuarios).

**¿Cómo se calcula?** Se suman tres componentes:

1. **Tráfico por descarga de documentos:** Cada documento nuevo descargado ocupa aproximadamente 0,45 MB (mismo tamaño que en almacenamiento).
   ```
   Red_docs = Documentos_mes × 0,00045 GB
   ```

2. **Tráfico por polling de fuentes:** Cada 50 fuentes generan aproximadamente 0,015 GB/mes en consultas periódicas (pings, RSS, llamadas API).
   ```
   Red_polling = 0,015 × (Fuentes / 50)
   ```

3. **Tráfico por sesiones de usuario:** Cada 40 sesiones concurrentes generan aproximadamente 0,02 GB/mes en descargas de dashboards, exportaciones y consultas.
   ```
   Red_sessions = 0,02 × (Sesiones / 40)
   ```

**Total de ancho de banda:**
```
Red_total = Red_docs + Red_polling + Red_sessions
```

**¿Por qué estos valores?** El tráfico de documentos es el componente dominante (la mayoría de los datos entran al sistema). El polling de fuentes es pequeño pero constante (consultas regulares para verificar actualizaciones). El tráfico de usuarios es moderado (dashboards y exportaciones no son tan pesados como las descargas masivas de documentos).

---

### 2.4. RAM (Memoria)

**¿Qué representa?** La memoria RAM necesaria en el servidor para mantener índices de búsqueda en memoria, cachés de tecnologías, y datos de sesiones activas.

**¿Cómo se calcula?** Se calcula en dos partes:

1. **RAM base y por documentos:** 16 GB base del sistema, más una cantidad proporcional al volumen de documentos acumulados (normalizada entre 0 y 10 GB adicionales).
   ```
   RAM_normalizada = (Documentos_acumulados - mínimo) / (máximo - mínimo)
   RAM_docs = 16 + RAM_normalizada × 10
   ```

2. **RAM por sesiones:** Un pequeño incremento adicional por cada sesión concurrente activa.
   ```
   RAM_peak = RAM_docs + 0,05 × (Sesiones / 40)
   ```

**¿Por qué estos valores?** La RAM se usa principalmente para:
- Índices de búsqueda en memoria (para consultas rápidas)
- Caché de tecnologías verdes y ontologías (para clasificación en tiempo real)
- Datos de sesiones activas (resultados filtrados, dashboards precargados)
- Vectores de embedding en memoria (para búsqueda semántica)

El crecimiento no es lineal con los documentos porque se implementan optimizaciones (liberación de cachés, almacenamiento en disco de datos fríos) a medida que crece el volumen.

---

### 2.5. GPU (Procesamiento Gráfico)

**¿Qué representa?** Las horas de procesamiento en GPU necesarias para renderizar dashboards comparativos complejos y ejecutar modelos de análisis avanzados.

**¿Cómo se calcula?** Se suman dos componentes:

1. **GPU por dashboards de iniciativas:** Cada 50 iniciativas requieren aproximadamente 0,02 horas/mes de GPU para renderizar visualizaciones comparativas.
   ```
   GPU_dashboards = 0,02 × (Iniciativas / 50)
   ```

2. **GPU por modelado de tecnologías:** Cada 50 tecnologías requieren aproximadamente 0,015 horas/mes de GPU para ejecutar modelos de análisis y clasificación.
   ```
   GPU_modeling = 0,015 × (Tecnologías / 50)
   ```

**Total de GPU:**
```
GPU_total = GPU_dashboards + GPU_modeling
```

**¿Por qué estos valores?** La GPU se usa principalmente para:
- Renderizado de dashboards interactivos con muchos elementos (gráficos comparativos de iniciativas de competidores)
- Ejecución de modelos de machine learning para clasificación y análisis de tecnologías
- Procesamiento de imágenes y visualizaciones complejas

El consumo es relativamente bajo porque la GPU solo se usa para tareas específicas, no para el procesamiento general del sistema.

---

### 2.6. Latencia y Tiempo de Alerta

**¿Qué representan?** Indicadores de rendimiento del sistema: cuánto tiempo tarda en responder una consulta (latencia) y cuánto tiempo tarda en emitir una alerta automática.

**¿Cómo se calculan?** Ambos están ligados al nivel de saturación de CPU:

```
Latencia(segundos) = 1,7 + 3,2 × (CPU_saturación - 10%) / 60%
Tiempo_alerta(segundos) = 18 + 32 × (CPU_saturación - 10%) / 60%
```

Ambos valores están limitados (clipeados) a rangos razonables:
- Latencia: entre 1,5 y 4,8 segundos (el SLA requiere <5 segundos)
- Tiempo de alerta: entre 12 y 55 segundos (el SLA requiere <60 segundos)

**¿Por qué estos valores?** A medida que el CPU se satura más, el sistema tarda más en procesar consultas y generar alertas. La relación es aproximadamente lineal: cuando el CPU está al 10% de uso, la latencia es mínima (1,7 segundos). Cuando está al 70% de uso, la latencia se acerca al máximo permitido (4,8 segundos).

---

## 3. Resumen de Relaciones

Para facilitar la comprensión, aquí está el resumen de qué UPN afecta a qué recurso:

| Recurso | UPNs que lo afectan | Tipo de relación |
|---------|---------------------|------------------|
| **CPU** | Fuentes, Documentos, Tecnologías, Iniciativas, Sesiones | Suma de componentes |
| **Almacenamiento** | Documentos acumulados, Tecnologías, Iniciativas | Suma de componentes |
| **Red** | Documentos mensuales, Fuentes, Sesiones | Suma de componentes |
| **RAM** | Documentos acumulados, Sesiones | Normalización + componente adicional |
| **GPU** | Tecnologías, Iniciativas | Suma de componentes |
| **Latencia** | CPU (indirectamente, vía todas las UPN) | Función de saturación de CPU |
| **Tiempo de alerta** | CPU (indirectamente, vía todas las UPN) | Función de saturación de CPU |

---

## 4. Valores de Referencia

**Punto de partida (diciembre 2025):**
- Fuentes: 300
- Documentos/mes: 18.000
- Tecnologías: 100
- Iniciativas: 80
- Sesiones pico: 40

**Objetivos a 2 años (diciembre 2027):**
- Fuentes: ~600
- Documentos/mes: ~42.000
- Tecnologías: ~150
- Iniciativas: ~200
- Sesiones pico: ~120

**Recursos proyectados a 2 años:**
- CPU: ~70% de uso (3.640 horas/mes de 5.200 disponibles)
- Almacenamiento: ~0,39 TB
- Red: ~22 GB/mes
- RAM pico: ~26 GB
- GPU: ~0,13 horas/mes
- Latencia: ~4,8 segundos (cerca del límite de 5 segundos)
- Tiempo de alerta: ~55 segundos (cerca del límite de 60 segundos)

---

*Documento generado para la planificación de capacidad de la plataforma CI + Vigilancia Tecnológica de AGUNSA Europa (2025-2027)*






