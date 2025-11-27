import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# ============================================================================
# Modelo de planeación de capacidad para la plataforma CI + Vigilancia.
# El objetivo es cuantificar cómo las tres UPN definidas (Fuentes,
# Documentos, Tecnologías verdes) evolucionan y cómo su crecimiento
# impacta en los recursos
# técnicos (CPU, almacenamiento, memoria y red).
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
    "cpu": "#ff7043",
    "storage": "#6d4c41",
    "network": "#26a69a",
    "ram": "#8e24aa",
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
# UPN: Documento ASG
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
# UPN: Tecnología verde
# -----------------------------------
# Cada punto es una categoría tecnológica consolidada.
# Comportamiento: crecimiento con pulsos cuando aparecen nuevas oleadas.
# Impacto: nuevos nodos en ontología => RAM; reprocesos => CPU;
# comparativas => CPU (analytics).
tec = stepped_series(
    BASELINES["TEC"],
    monthly_rate=0.01,
    step_increments=[(12, 15), (18, 20), (22, 15)],
)

# =================================================
# Impresión de UPNs y sus valores
# =================================================
print("\n" + "="*80)
print("UPNs - Unidades de Planificación de Negocio")
print("="*80)

print("\n1. UPN: Fuentes de Información")
print("-" * 80)
for i, (mes, valor) in enumerate(zip(MONTHS, fuentes)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} fuentes")

print("\n2. UPN: Documentos ASG (por mes)")
print("-" * 80)
for i, (mes, valor) in enumerate(zip(MONTHS, docs_mes)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} documentos/mes")

print("\n3. UPN: Tecnologías Verdes")
print("-" * 80)
for i, (mes, valor) in enumerate(zip(MONTHS, tec)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} tecnologías")

print("\n" + "="*80)
print("Resumen de UPNs:")
print("-" * 80)
print(f"Fuentes - Inicial: {fuentes[0]:.2f}, Final: {fuentes[-1]:.2f}, Promedio: {fuentes.mean():.2f}")
print(f"Documentos/mes - Inicial: {docs_mes[0]:.2f}, Final: {docs_mes[-1]:.2f}, Promedio: {docs_mes.mean():.2f}")
print(f"Tecnologías - Inicial: {tec[0]:.2f}, Final: {tec[-1]:.2f}, Promedio: {tec.mean():.2f}")
print("="*80 + "\n")

# =================================================
# 3. Consumos de recursos (alineados al informe)
# =================================================
CPU_CAPACITY = 5200  # horas mensuales disponibles en cluster

cpu_scraping = 0.9 * (fuentes / 100.0)
cpu_indexing = 0.0015 * docs_mes
cpu_analytics = 0.08 * (tec / 50.0)
cpu_components = cpu_scraping + cpu_indexing + cpu_analytics
# Escalamos para que el uso vaya de ~10% a ~70%
cpu_norm = (cpu_components - cpu_components.min()) / (
    cpu_components.max() - cpu_components.min()
)
cpu_saturation = 0.10 + cpu_norm * (0.70 - 0.10)
cpu_total = cpu_saturation * CPU_CAPACITY

# Almacenamiento (GB) – objetivo ~356 GB al 2027
DOC_SIZE_GB = 0.00045  # ~0.45 MB promedio
storage_docs = docs_acumulados * DOC_SIZE_GB
storage_indexes = 0.0009 * tec
storage_total = 5 + storage_docs + storage_indexes

# Ancho de banda (GB/mes) – 10 -> 25 GB
network_docs = docs_mes * DOC_SIZE_GB
network_polling = 0.015 * (fuentes / 50.0)
network_total = network_docs + network_polling

# RAM pico (GB) – 16 -> ~30
ram_norm = (docs_acumulados - docs_acumulados.min()) / (
    docs_acumulados.max() - docs_acumulados.min()
)
ram_peak = 16 + ram_norm * 10

# =================================================
# Impresión de Recursos y sus valores
# =================================================
print("\n" + "="*80)
print("CPU Total (horas/mes)")
print("="*80)
for i, (mes, valor) in enumerate(zip(MONTHS, cpu_total)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} horas/mes")
print(f"\nResumen - Inicial: {cpu_total[0]:.2f}, Final: {cpu_total[-1]:.2f}, Promedio: {cpu_total.mean():.2f}")
print("="*80)

print("\n" + "="*80)
print("Almacenamiento Total (GB)")
print("="*80)
for i, (mes, valor) in enumerate(zip(MONTHS, storage_total)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} GB")
print(f"\nResumen - Inicial: {storage_total[0]:.2f}, Final: {storage_total[-1]:.2f}, Promedio: {storage_total.mean():.2f}")
print("="*80)

print("\n" + "="*80)
print("Ancho de Banda Total (GB/mes)")
print("="*80)
for i, (mes, valor) in enumerate(zip(MONTHS, network_total)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} GB/mes")
print(f"\nResumen - Inicial: {network_total[0]:.2f}, Final: {network_total[-1]:.2f}, Promedio: {network_total.mean():.2f}")
print("="*80)

print("\n" + "="*80)
print("RAM Pico (GB)")
print("="*80)
for i, (mes, valor) in enumerate(zip(MONTHS, ram_peak)):
    print(f"  Mes {i+1:2d} ({mes.strftime('%Y-%m')}): {valor:8.2f} GB")
print(f"\nResumen - Inicial: {ram_peak[0]:.2f}, Final: {ram_peak[-1]:.2f}, Promedio: {ram_peak.mean():.2f}")
print("="*80 + "\n")

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
        "CPU_total_horas": cpu_total,
        "Storage_total_GB": storage_total,
        "Network_total_GB": network_total,
        "RAM_peak_GB": ram_peak,
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
    "CPU_total_horas",
    "Storage_total_GB",
    "Network_total_GB",
    "RAM_peak_GB",
]
print(
    monthly_df.assign(Mes=monthly_df["Mes"].dt.strftime("%Y-%m"))[display_cols].round(2)
)

# =================================================
# 5. Dashboard mensual
# =================================================
fig = plt.figure(figsize=(19, 8.5))
fig.patch.set_facecolor("#fdfdfd")
fig.suptitle(
    "Dashboard mensual - Plataforma CI + Vigilancia (AGUNSA Europa)",
    fontsize=18,
    color=ACCENT_GRAY,
    fontweight="bold",
)

# Usar gridspec para centrar los 3 gráficos de arriba
# Grid de 2 filas x 10 columnas: cada gráfico ocupa 2 columnas
# Fila 1: espacio izquierdo (2 cols) + 3 gráficos (6 cols) + espacio derecho (2 cols)
# Fila 2: espacio izquierdo (1 col) + 4 gráficos centrados (8 cols, 2 cols cada uno) + espacio derecho (1 col)
gs = gridspec.GridSpec(2, 10, figure=fig, left=0.05, right=0.97, bottom=0.12, top=0.78, 
                       hspace=0.35, wspace=0.22)

# Crear los ejes: fila 1 tiene espacios a los lados, fila 2 tiene 4 gráficos centrados
axes = []
# Fila 1: espacio izquierdo (cols 0-1), 3 gráficos (cols 2-3, 4-5, 6-7), espacio derecho (cols 8-9)
axes.append(fig.add_subplot(gs[0, 2:4]))  # Fuentes (ocupa cols 2-3)
axes.append(fig.add_subplot(gs[0, 4:6]))  # Documentos (ocupa cols 4-5)
axes.append(fig.add_subplot(gs[0, 6:8]))  # Tecnologías (ocupa cols 6-7)
# Fila 2: 4 gráficos centrados (cada uno ocupa 2 columnas)
axes.append(fig.add_subplot(gs[1, 1:3]))  # CPU (cols 1-2)
axes.append(fig.add_subplot(gs[1, 3:5]))  # Almacenamiento (cols 3-4)
axes.append(fig.add_subplot(gs[1, 5:7]))  # Ancho de banda (cols 5-6)
axes.append(fig.add_subplot(gs[1, 7:9]))  # RAM (cols 7-8)

# Ocultar los espacios vacíos de la fila 1 (un gráfico a cada lado)
ax_left = fig.add_subplot(gs[0, 0:2])
ax_left.axis('off')
ax_right = fig.add_subplot(gs[0, 8:10])
ax_right.axis('off')
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

# Organizar gráficos: fila 1 tiene 3 UPN centradas, fila 2 tiene los 4 gráficos de recursos
series_info = [
    (fuentes, "Fuentes monitoreadas", "Cantidad", PALETTE["fuentes"]),  # Fila 1, gráfico 0
    (docs_mes / 1000, "Documentos por mes (miles)", "Miles", PALETTE["docs"]),  # Fila 1, gráfico 1
    (tec, "Tecnologias verdes", "Categorías", PALETTE["tec"]),  # Fila 1, gráfico 2
    (cpu_total, "CPU total (h/mes)", "Horas", PALETTE["cpu"]),  # Fila 2, gráfico 0
    (storage_total / 1000, "Almacenamiento (TB)", "TB", PALETTE["storage"]),  # Fila 2, gráfico 1
    (network_total, "Ancho de banda (GB/mes)", "GB", PALETTE["network"]),  # Fila 2, gráfico 2
    (ram_peak, "RAM pico (GB)", "GB", PALETTE["ram"]),  # Fila 2, gráfico 3
]

for ax, (series, title, ylabel, color) in zip(axes, series_info):
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
