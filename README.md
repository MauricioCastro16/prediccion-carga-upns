# prediccion-carga-upns
  
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)  
![Pandas](https://img.shields.io/badge/Pandas-2.x-black.svg)  
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-orange.svg)  
  
Modelo de planificación de capacidad que proyecta el crecimiento de Unidades de Predicción Natural (UPN) y traduce su evolución en consumo de recursos técnicos (CPU, almacenamiento, red y RAM) para una plataforma de Inteligencia Competitiva y Vigilancia Tecnológica.
  
## Características Principales  
- Modelado de tres UPNs (Fuentes, Documentos, Tecnologías) con crecimiento escalonado y exponencial. 
- Proyección de recursos: CPU, almacenamiento, red y RAM pico, con normalización y saturación.  
- Dashboard mensual automatizado con 7 paneles usando matplotlib y gridspec.
- Salida tabular mensual (DataFrame) con métricas clave y ratios diarios
- Trazabilidad explícita entre UPNs y fórmulas de consumo documentadas.  
  
## Stack Tecnológico  
| Categoría       | Tecnologías                     |  
|-----------------|---------------------------------|  
| Backend         | Python, pandas, numpy           |  
| Herramientas    | matplotlib, matplotlib.gridspec |  
  
## Arquitectura / Flujo  
El script `TPI.py` define el horizonte temporal, modela cada UPN con `stepped_series`, calcula componentes de recurso a partir de las UPNs, normaliza la CPU y RAM, construye un DataFrame mensual y renderiza un dashboard con gridspec para visualizar tendencias y valores clave.
  
## Instalación y Uso  
```bash  
# Clonar el repositorio
git clone https://github.com/MauricioCastro16/AdmSI-TecnicasPrediccionCarga.git  
cd AdmSI-TecnicasPrediccionCarga  
  
# Crear y activar entorno virtual
python -m venv venv  
source venv/bin/activate  # En Windows: venv\Scripts\activate  
  
# Instalar dependencias
pip install pandas matplotlib numpy  
  
# Ejecutar el modelo principal
python TPI.py
