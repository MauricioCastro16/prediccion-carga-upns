import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# ============================================================================
# Modelo de planeación de capacidad para la plataforma CI + Vigilancia.
# El objetivo es cuantificar cómo las cinco UPN definidas (Fuentes,
# Documentos, Tecnologías verdes, Iniciativas de la competencia y Sesiones
# concurrentes) evolucionan y cómo su crecimiento impacta en los recursos
# técnicos (CPU, almacenamiento, memoria, red y GPU).
# Cada bloque del script referencia explícitamente qué UPN participa en el
# cálculo para mantener la trazabilidad con la tabla de consumos entregada.
# ============================================================================

# =================================================
# 1. Horizonte temporal (dic-2025 -> dic-2027)
# =================================================
START_MONTH = pd.Timestamp("2025-12-01")
TOTAL_MONTHS = 25  # incluye dic-2027
MONTHS = pd.date_range(start=START_MONTH, periods=TOTAL_MONTHS, freq="MS")
MONTH_INDEX = np.arange(len(MONTHS))

# Estilo y branding para el dashboard final
plt.style.use("seaborn-v0_8-whitegrid")
AGUNSA_RED = "#ed1c24"
ACCENT_BLUE = "#005f92"
ACCENT_GOLD = "#f2a900"
ACCENT_GREEN = "#4caf50"
ACCENT_PURPLE = "#7a3eb1"
ACCENT_GRAY = "#4d4d4d"
PALETTE = {
    "fuentes": AGUNSA_RED,
    "docs": ACCENT_GREEN,
    "tec": ACCENT_PURPLE,
    "inits": ACCENT_GOLD,
    "ses": ACCENT_BLUE,
    "cpu": "#ff7043",
    "storage": "#6d4c41",
    "network": "#26a69a",
    "ram": "#8e24aa",
    "gpu": "#546e7a",
}
LOGO_PATH = "4619-AGUNSA_(2).jpg"
FONT_FAMILY = "DejaVu Sans"
plt.rcParams.update(
    {
        "font.family": FONT_FAMILY,
        "axes.labelcolor": ACCENT_GRAY,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "xtick.color": "#5c5c5c",
        "ytick.color": "#5c5c5c",
        "grid.alpha": 0.25,
    }
)

def add_brand_logo(fig, position=(0.9, 0.9), zoom=0.15, box_alignment=(0.5, 0.5)):
    try:
        logo_img = plt.imread(LOGO_PATH)
        imagebox = OffsetImage(logo_img, zoom=zoom)
        ab = AnnotationBbox(
            imagebox,
            position,
            xycoords="figure fraction",
            frameon=False,
            box_alignment=box_alignment,
        )
        fig.add_artist(ab)
    except FileNotFoundError:
        fig.text(
            position[0],
            position[1],
            "AGUNSA",
            color=AGUNSA_RED,
            fontsize=18,
            fontweight="bold",
        )
# =================================================
# 2. Supuestos alineados con el informe estratégico
# =================================================
BASELINES = {
    "FUENTES": 300,   # fuentes iniciales monitoreadas
    "DOCS_MES": 18000,  # documentos por mes en dic-2025
    "DOCS_HIST": 50000, # registros previos acumulados
    "TEC": 100,       # tecnologías clasificadas
    "INITS": 80,      # iniciativas competitivas
    "SES": 40,        # sesiones concurrentes pico
}

def stepped_series(base_value, monthly_rate, step_increments=None):
    """Serie exponencial con saltos escalonados para reflejar nuevas olas."""
    series = base_value * (1 + monthly_rate) ** MONTH_INDEX
    if step_increments:
        for step_month, delta in step_increments:
            series[MONTH_INDEX >= step_month] += delta
    return series

# ----------------------------
# UPN: Fuente de información
# ----------------------------
# Cada valor representa la cantidad de webs/API/repositorios monitoreados.
# Comportamiento: crecimiento escalonado (nuevos países/sectores).
# Impacto posterior: más scraping programado, mayor polling de fuentes,
# y crecimiento de tráfico entrante.
fuentes = stepped_series(
    BASELINES["FUENTES"],
    monthly_rate=0.012,
    step_increments=[(3, 40), (9, 50), (15, 60), (21, 60)],
)

# --------------------------------
# UPN: Documento recolectado
# --------------------------------
# Se modela como documentos/mes (input directo a cómputo/almacenamiento).
# Comportamiento: fuerte crecimiento proporcional a las fuentes y un
# factor adicional (growth_factor) para llegar a 42k/mes en 2027.
# Impacto posterior: indexación (CPU), tamaño de índices (RAM/Storage),
# y tráfico de red por descargas.
target_docs = 42000
growth_factor = (target_docs / BASELINES["DOCS_MES"]) ** (1 / (TOTAL_MONTHS - 1))
docs_mes = (
    BASELINES["DOCS_MES"]
    * growth_factor ** MONTH_INDEX
    * (fuentes / fuentes[0]) ** 0.25
)
docs_mes = np.clip(docs_mes, BASELINES["DOCS_MES"], None)
docs_acumulados = BASELINES["DOCS_HIST"] + np.cumsum(docs_mes)

# -----------------------------------
# UPN: Tecnología verde registrada
# -----------------------------------
# Cada punto es una categoría tecnológica consolidada.
# Comportamiento: crecimiento con pulsos cuando aparecen nuevas oleadas.
# Impacto: nuevos nodos en ontología => RAM; reprocesos => CPU;
# comparativas => GPU (modeling) y CPU (analytics).
tec = stepped_series(
    BASELINES["TEC"],
    monthly_rate=0.01,
    step_increments=[(12, 15), (18, 20), (22, 15)],
)

# ---------------------------------------------
# UPN: Iniciativa competencia monitoreada
# ---------------------------------------------
# Representa proyectos verdes de competidores.
# Comportamiento: tendencia creciente casi lineal (sumamos paquetes).
# Impacto: más datos históricos (almacenamiento), más dashboards
# comparativos (GPU) y carga analítica (CPU).
inits = stepped_series(
    BASELINES["INITS"],
    monthly_rate=0.02,
    step_increments=[(6, 18), (14, 22), (20, 28)],
)

# --------------------------------
# UPN: Sesión de usuario concurrente
# --------------------------------
# Representa el número máximo de usuarios simultáneos.
# Comportamiento: tendencia creciente + estacionalidad (sinusoidal) para
# reflejar picos diarios/mensuales.
# Impacto: carga de CPU y RAM por sesión, credenciales y tráfico de red.
ses_base = BASELINES["SES"] * (1 + 0.03) ** MONTH_INDEX
seasonal = 1 + 0.18 * np.sin(2 * np.pi * MONTH_INDEX / 12) + 0.05 * np.sin(
    4 * np.pi * MONTH_INDEX / 12
)
ses = np.clip(ses_base * seasonal, BASELINES["SES"] * 0.6, None)

# =================================================
# 3. Consumos de recursos (alineados al informe)
# =================================================
CPU_CAPACITY = 5200  # horas mensuales disponibles en cluster

cpu_scraping = 0.9 * (fuentes / 100.0)
cpu_indexing = 0.0015 * docs_mes
cpu_analytics = 0.08 * (tec / 50.0) + 0.05 * (inits / 50.0)
cpu_sessions = 0.12 * (ses / 50.0)
cpu_components = cpu_scraping + cpu_indexing + cpu_analytics + cpu_sessions
# Escalamos para que el uso vaya de ~10% a ~70%
cpu_norm = (cpu_components - cpu_components.min()) / (
    cpu_components.max() - cpu_components.min()
)
cpu_saturation = 0.10 + cpu_norm * (0.70 - 0.10)
cpu_total = cpu_saturation * CPU_CAPACITY

# Almacenamiento (GB) – objetivo ~356 GB al 2027
DOC_SIZE_GB = 0.00045  # ~0.45 MB promedio
storage_docs = docs_acumulados * DOC_SIZE_GB
storage_indexes = 0.0009 * tec + 0.0004 * inits
storage_total = 5 + storage_docs + storage_indexes

# Ancho de banda (GB/mes) – 10 -> 25 GB
network_docs = docs_mes * DOC_SIZE_GB
network_polling = 0.015 * (fuentes / 50.0)
network_sessions = 0.02 * (ses / 40.0)
network_total = network_docs + network_polling + network_sessions

# RAM pico (GB) – 16 -> ~30
ram_norm = (docs_acumulados - docs_acumulados.min()) / (
    docs_acumulados.max() - docs_acumulados.min()
)
ram_peak = 16 + ram_norm * 10 + 0.05 * (ses / BASELINES["SES"])

# GPU reservada para dashboards comparativos
gpu_dashboards = 0.02 * (inits / 50.0)
gpu_modeling = 0.015 * (tec / 50.0)
gpu_total = gpu_dashboards + gpu_modeling

# KPI de latencia/alertas ligados al uso de CPU
latencia_seg = np.clip(1.7 + 3.2 * (cpu_saturation - 0.1) / 0.6, 1.5, 4.8)
alerta_seg = np.clip(18 + 32 * (cpu_saturation - 0.1) / 0.6, 12, 55)

# =================================================
# 4. DataFrame mensual
# =================================================
monthly_df = pd.DataFrame(
    {
        "Mes": MONTHS,
        "FuenteInformacion": fuentes,
        "Documentos_mes": docs_mes,
        "Docs_acumulados": docs_acumulados,
        "TecnologiaVerdeRegistrada": tec,
        "IniciativaCompetenciaMonitoreada": inits,
        "SesionUsuarioConcurrente": ses,
        "CPU_total_horas": cpu_total,
        "Storage_total_GB": storage_total,
        "Network_total_GB": network_total,
        "RAM_peak_GB": ram_peak,
        "GPU_total_horas": gpu_total,
        "Latencia_seg": latencia_seg,
        "Alerta_seg": alerta_seg,
    }
)
monthly_df["Dias_mes"] = monthly_df["Mes"].dt.days_in_month
monthly_df["Docs_promedio_dia"] = monthly_df["Documentos_mes"] / monthly_df["Dias_mes"]
monthly_df["CPU_horas_dia"] = monthly_df["CPU_total_horas"] / monthly_df["Dias_mes"]
monthly_df["Network_GB_dia"] = monthly_df["Network_total_GB"] / monthly_df["Dias_mes"]

display_cols = [
    "Mes",
    "FuenteInformacion",
    "Documentos_mes",
    "TecnologiaVerdeRegistrada",
    "IniciativaCompetenciaMonitoreada",
    "SesionUsuarioConcurrente",
    "CPU_total_horas",
    "Storage_total_GB",
    "Network_total_GB",
    "RAM_peak_GB",
    "Latencia_seg",
]
print(
    monthly_df.assign(Mes=monthly_df["Mes"].dt.strftime("%Y-%m"))[display_cols].round(2)
)

# =================================================
# 5. Dashboard mensual
# =================================================
fig, axes = plt.subplots(2, 5, figsize=(19, 8.5))
fig.patch.set_facecolor("#fdfdfd")
fig.suptitle(
    "Dashboard mensual - Plataforma CI + Vigilancia (AGUNSA Europa)",
    fontsize=18,
    color=ACCENT_GRAY,
    fontweight="bold",
)
fig.subplots_adjust(left=0.05, right=0.97, bottom=0.12, top=0.78, hspace=0.35, wspace=0.22)
month_locator = mdates.MonthLocator(interval=3)
month_formatter = mdates.DateFormatter("%Y-%m")
YEAR1_IDX = min(12, len(MONTHS) - 1)
YEAR2_IDX = min(24, len(MONTHS) - 1)

def format_value(val, precision=1):
    """Formateo compacto para anotaciones con precisión ajustable."""
    if abs(val) >= 1000:
        return f"{val/1000:.{precision}f}K"
    return f"{val:,.{precision}f}"

def format_with_auto_precision(val1, val2):
    """Formatea dos valores aumentando precisión si son iguales con 1 decimal."""
    # Empezamos con 1 decimal
    prec = 1
    while prec <= 3:
        fmt1 = format_value(val1, prec)
        fmt2 = format_value(val2, prec)
        # Si son diferentes, usamos esta precisión
        if fmt1 != fmt2:
            return fmt1, fmt2
        prec += 1
    # Si después de 3 decimales siguen iguales, devolvemos con 3
    return format_value(val1, 3), format_value(val2, 3)

series_info = [
    (fuentes, "Fuentes monitoreadas", "Cantidad", PALETTE["fuentes"]),
    (docs_mes / 1000, "Documentos por mes (miles)", "Miles", PALETTE["docs"]),
    (tec, "Tecnologias verdes", "Categorías", PALETTE["tec"]),
    (inits, "Iniciativas competencia", "Iniciativas", PALETTE["inits"]),
    (ses, "Sesiones concurrentes", "Sesiones", PALETTE["ses"]),
    (cpu_total, "CPU total (h/mes)", "Horas", PALETTE["cpu"]),
    (storage_total / 1000, "Almacenamiento (TB)", "TB", PALETTE["storage"]),
    (network_total, "Ancho de banda (GB/mes)", "GB", PALETTE["network"]),
    (ram_peak, "RAM pico (GB)", "GB", PALETTE["ram"]),
    (gpu_total, "GPU analitica (h/mes)", "Horas", PALETTE["gpu"]),
]

for ax, (series, title, ylabel, color) in zip(axes.flatten(), series_info):
    ax.plot(MONTHS, series, color=color, linewidth=2.4, marker="o", markersize=4)
    ax.fill_between(MONTHS, series, color=color, alpha=0.12)
    ax.set_title(title, pad=20)
    ax.set_ylabel(ylabel)
    ax.set_facecolor("#ffffff")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)
    ax.xaxis.set_major_locator(month_locator)
    ax.xaxis.set_major_formatter(month_formatter)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.set_xticks([])
    # Eliminamos anotación externa y nos quedamos con la tarjeta interna
    # Usamos precisión automática para distinguir valores que parecen iguales
    val_12m, val_24m = format_with_auto_precision(series[YEAR1_IDX], series[YEAR2_IDX])
    ax.text(
        0.02,
        0.85,
        f"12m: {val_12m}\n24m: {val_24m}",
        transform=ax.transAxes,
        fontsize=8.5,
        color=ACCENT_GRAY,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.65, edgecolor="none"),
    )
add_brand_logo(fig, position=(0.995, 0.97), zoom=0.045, box_alignment=(1.0, 1.0))
fig.text(
    0.03,
    0.03,
    "Valores mensuales 2025-12 a 2027-12 · Fuente: Planificación capacidad AGUNSA Europa",
    color="#6c6c6c",
    fontsize=9,
)
plt.tight_layout(rect=[0.04, 0.06, 0.96, 0.9])

plt.show()
