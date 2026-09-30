import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob
import io

# ==============================================================================
# Identidad Visual y Colores de Marca: CLV México (clvmexico.com)
# ==============================================================================
CLV_PRIMARY = "#00B2FF"      # Azul Eléctrico / Cian Digital Oficial
CLV_NAVY = "#0F2942"         # Azul Marino Profundo Corporativo
CLV_DARK = "#0E0E0E"         # Negro Ónix del Logotipo
CLV_CYAN = "#38BDF8"         # Cian Claro de Acento
CLV_SLATE = "#1E293B"        # Gris Pizarra
CLV_LIGHT_BG = "#F8FAFC"     # Fondo Claro Ejecutivo
CLV_BORDER = "#E2E8F0"       # Bordes Sutiles

# Gradiente corporativo para gráficos cuantitativos continuos
CLV_GRADIENT = [[0.0, "#0F2942"], [0.5, "#0284C7"], [1.0, "#00B2FF"]]

# Paleta categórica armónica para variables cualitativas
CLV_QUALITATIVE = [
    "#00B2FF", "#0F2942", "#38BDF8", "#10B981", 
    "#6366F1", "#F59E0B", "#EC4899", "#64748B"
]

# Configuración de Plantilla Plotly para Modo Oscuro y Colores CLV
import plotly.io as pio
pio.templates["clv_dark"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        colorway=CLV_QUALITATIVE
    )
)
pio.templates.default = "plotly_dark+clv_dark"

# Ruta del Logo
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clv_logo.png")
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = "/Users/sonniafloresdelgado/Desktop/Concentración André/Despliegue/clv_logo.png"


# ==============================================================================
# Configuración de la Página
# ==============================================================================
st.set_page_config(
    page_title="CLV México | Dashboard de Análisis Exploratorio Univariado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS adaptados para Modo Oscuro y temática CLV México
st.markdown("""
<style>
    /* Tipografía y Títulos adaptados a Modo Oscuro */
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    .sub-title {
        font-size: 1.02rem;
        color: #94A3B8 !important;
        margin-bottom: 1.2rem;
    }
    .header-badge {
        display: inline-block;
        background-color: #00B2FF;
        color: #0E0E0E;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 12px;
        border-radius: 9999px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    
    /* Pestañas (Tabs) con estilo CLV para Modo Oscuro */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #00B2FF;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        background-color: #1E293B !important;
        border-radius: 8px 8px 0px 0px;
        font-weight: 600;
        color: #94A3B8 !important;
        padding: 10px 18px;
        transition: all 0.2s ease-in-out;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2D3D52 !important;
        color: #FFFFFF !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00B2FF !important;
        color: #0E0E0E !important;
        font-weight: 700 !important;
    }
    
    /* Botón Primario de Acción */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00B2FF 0%, #0088CC 100%) !important;
        color: #0E0E0E !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(0, 178, 255, 0.28) !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0095D9 0%, #0077B3 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 6px 16px rgba(0, 178, 255, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Tarjetas de Métricas (st.metric) en Modo Oscuro Elegante */
    div[data-testid="stMetric"] {
        background: #131B26 !important;
        border: 1px solid #2A3649 !important;
        border-top: 4px solid #00B2FF !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.85rem !important;
    }
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] > div,
    div[data-testid="stMetricLabel"] p {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    
    /* Contenedor del Logo en Sidebar */
    .sidebar-logo-container {
        background-color: #0E0E0E;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 12px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado Principal con Logotipo y Título Corporativo
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
with col_h2:
    st.markdown('<span class="header-badge">Inteligencia de Datos CLV México</span>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Dashboard de Análisis Exploratorio Univariado</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Plataforma analítica corporativa para diagnóstico de calidad de datos y análisis univariado del socio formador CLV México.</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================================================================
# Funciones Auxiliares y de Procesamiento
# ==============================================================================

@st.cache_data(show_spinner=False)
def buscar_archivo_por_defecto():
    """Busca Datos_CLV_2026_Tec_v2.xlsx en la estructura de carpetas."""
    rutas_candidatas = [
        os.path.join(os.getcwd(), "Datos_CLV_2026_Tec_v2.xlsx"),
        os.path.join(os.path.dirname(os.getcwd()), "Reto", "Datos_CLV_2026_Tec_v2.xlsx"),
        os.path.join(os.path.dirname(os.getcwd()), "Datos_CLV_2026_Tec_v2.xlsx"),
    ]
    for r in rutas_candidatas:
        if os.path.exists(r):
            return r
    matches = glob.glob(os.path.join(os.path.dirname(os.getcwd()), "**", "Datos_CLV_2026_Tec_v2.xlsx"), recursive=True)
    if matches:
        return matches[0]
    return None

@st.cache_data(show_spinner=False)
def cargar_nombres_hojas(file_or_path):
    """Obtiene los nombres de hojas disponibles en el libro de Excel."""
    try:
        xls = pd.ExcelFile(file_or_path)
        return xls.sheet_names
    except Exception as e:
        return []

@st.cache_data(show_spinner=False)
def cargar_hoja_datos(file_or_path, sheet_name):
    """Carga los datos crudos de una hoja y sanitiza columnas mixtas para PyArrow."""
    df = pd.read_excel(file_or_path, sheet_name=sheet_name)
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: str(x) if pd.notna(x) else None)
    return df

def detectar_outliers_iqr(series: pd.Series):
    """Calcula límites de IQR y máscara de valores atípicos."""
    s = pd.to_numeric(series, errors='coerce').dropna()
    if len(s) == 0:
        return None, None, None, pd.Series(False, index=series.index)
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    mask_outliers = (series < lim_inf) | (series > lim_sup)
    return lim_inf, lim_sup, iqr, mask_outliers

def calcular_regla_sturges(series: pd.Series):
    """Calcula el número de clases y ancho de intervalo con la regla de Sturges."""
    s = pd.to_numeric(series, errors='coerce').dropna()
    n = len(s)
    if n == 0:
        return 5, 0, 0, 0
    k = int(np.ceil(1 + 3.322 * np.log10(n)))
    v_min = float(s.min())
    v_max = float(s.max())
    rango = v_max - v_min
    ancho = (rango / k) if k > 0 else 1.0
    return k, v_min, v_max, ancho

def generar_excel_descarga(df: pd.DataFrame) -> bytes:
    """Genera un archivo Excel en memoria para descarga."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Datos_Procesados")
    return output.getvalue()

# ==============================================================================
# Barra Lateral (Sidebar)
# ==============================================================================
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
    st.sidebar.markdown(
        "<div style='text-align: center; color: #94A3B8; font-size: 0.78rem; margin-top: -6px; margin-bottom: 14px; font-weight: 500;'>"
        "Soluciones Digitales en Odontología CAD-CAM"
        "</div>", 
        unsafe_allow_html=True
    )

st.sidebar.header("Configuración y Datos")

archivo_defecto = buscar_archivo_por_defecto()

uploaded_file = st.sidebar.file_uploader(
    "Cargar archivo Excel",
    type=['xlsx', 'xls'],
    help="Sube 'Datos_CLV_2026_Tec_v2.xlsx' u otro archivo Excel de datos"
)

fuente_datos = None
if uploaded_file is not None:
    fuente_datos = uploaded_file
    st.sidebar.success("Archivo personalizado subido con éxito.")
elif archivo_defecto is not None:
    fuente_datos = archivo_defecto
    st.sidebar.info(f"Usando archivo local por defecto:\n`{os.path.basename(archivo_defecto)}`")
else:
    st.warning("Por favor sube un archivo Excel para comenzar.")
    st.stop()

# Detección de hojas disponibles
hojas_disponibles = cargar_nombres_hojas(fuente_datos)
if not hojas_disponibles:
    st.error("No se pudieron leer las hojas del archivo Excel cargado.")
    st.stop()

# Selector de hoja
st.sidebar.markdown("---")
st.sidebar.subheader("Selección de Módulo / Hoja")
hoja_seleccionada = st.sidebar.selectbox(
    "Selecciona la hoja a analizar:",
    options=hojas_disponibles,
    index=1 if len(hojas_disponibles) > 1 and hojas_disponibles[0] == "Diccionario_Datos" else 0,
    help="Elige la tabla de datos correspondiente para ejecutar el análisis univariado"
)

# Opciones de procesamiento específicas
st.sidebar.markdown("---")
st.sidebar.subheader("Opciones de Procesamiento")

tratar_outliers = st.sidebar.checkbox(
    "Tratar valores atípicos (IQR + Mediana)",
    value=True,
    help="Aplica la metodología de la Actividad 2: reemplaza valores fuera de [Q1-1.5*IQR, Q3+1.5*IQR] por la mediana."
)

top_n = st.sidebar.slider(
    "Top N elementos en gráficos categóricos:",
    min_value=5,
    max_value=25,
    value=10,
    step=1
)

boton_ejecutar = st.sidebar.button("Ejecutar Análisis", type="primary", use_container_width=True)

# Guardar o actualizar en Session State
if boton_ejecutar or 'hoja_activa' not in st.session_state or st.session_state.get('hoja_activa') != hoja_seleccionada:
    st.session_state['hoja_activa'] = hoja_seleccionada
    st.session_state['tratar_outliers'] = tratar_outliers
    st.session_state['top_n'] = top_n
    st.session_state['ejecutado'] = True

# ==============================================================================
# Carga y Preparación de la Hoja Seleccionada
# ==============================================================================
with st.spinner(f"Cargando y procesando hoja '{hoja_seleccionada}'..."):
    df_raw = cargar_hoja_datos(fuente_datos, hoja_seleccionada)
    df_proc = df_raw.copy()

# Manejo especial para Diccionario de Datos
if hoja_seleccionada == "Diccionario_Datos":
    st.subheader("Diccionario de Datos del Proyecto")
    st.info("Esta hoja contiene las definiciones y metadatos de las variables del socio formador.")
    df_clean_dicc = df_raw.dropna(how='all').dropna(how='all', axis=1)
    st.dataframe(df_clean_dicc, use_container_width=True)
    st.stop()

# Pipeline de limpieza y preprocesamiento acorde a Actividad 2
nulos_antes = df_raw.isnull().sum()
outliers_info = {}

# 1. Ventas_CLV_2022_2026
if "ventas" in hoja_seleccionada.lower():
    if 'cp' in df_proc.columns and df_proc['cp'].isnull().any():
        moda_cp = df_proc['cp'].mode()[0] if not df_proc['cp'].mode().empty else "S/D"
        df_proc['cp'] = df_proc['cp'].fillna(moda_cp)
    
    cols_cuant = [c for c in ['precio_unitario', 'total_unidades', 'total_neto'] if c in df_proc.columns]
    for col in cols_cuant:
        lim_inf, lim_sup, iqr, mask = detectar_outliers_iqr(df_proc[col])
        conteo = mask.sum()
        outliers_info[col] = {
            'count': conteo, 'pct': (conteo / len(df_proc)) * 100 if len(df_proc) > 0 else 0,
            'lim_inf': lim_inf, 'lim_sup': lim_sup
        }
        if tratar_outliers and conteo > 0:
            mediana = df_proc[col].median()
            df_proc.loc[mask, col] = mediana

# 2. Existencias_04_09_2026
elif "existencias" in hoja_seleccionada.lower():
    cols_cuant = [c for c in ['existencias', 'valor_total_inventario'] if c in df_proc.columns]
    for col in cols_cuant:
        lim_inf, lim_sup, iqr, mask = detectar_outliers_iqr(df_proc[col])
        conteo = mask.sum()
        outliers_info[col] = {
            'count': conteo, 'pct': (conteo / len(df_proc)) * 100 if len(df_proc) > 0 else 0,
            'lim_inf': lim_inf, 'lim_sup': lim_sup
        }
        if tratar_outliers and conteo > 0:
            mediana = df_proc[col].median()
            df_proc.loc[mask, col] = mediana

# 3. Histórico_Compras
elif "compras" in hoja_seleccionada.lower():
    cols_cuant = [c for c in ['unidades', 'precio_unitario', 'precio_total_neto'] if c in df_proc.columns]
    for col in cols_cuant:
        lim_inf, lim_sup, iqr, mask = detectar_outliers_iqr(df_proc[col])
        conteo = mask.sum()
        outliers_info[col] = {
            'count': conteo, 'pct': (conteo / len(df_proc)) * 100 if len(df_proc) > 0 else 0,
            'lim_inf': lim_inf, 'lim_sup': lim_sup
        }
        if tratar_outliers and conteo > 0:
            mediana = df_proc[col].median()
            df_proc.loc[mask, col] = mediana

# 4. Ventas_Negadas_CRM
elif "negadas" in hoja_seleccionada.lower():
    if 'motivo_cierre_perdido' in df_proc.columns:
        df_proc['motivo_cierre_perdido'] = df_proc['motivo_cierre_perdido'].fillna("No especificado / Sin dato")

# 5. Salidas_Almacen
elif "salidas" in hoja_seleccionada.lower():
    if 'salidas' in df_proc.columns:
        lim_inf, lim_sup, iqr, mask = detectar_outliers_iqr(df_proc['salidas'])
        conteo = mask.sum()
        outliers_info['salidas'] = {
            'count': conteo, 'pct': (conteo / len(df_proc)) * 100 if len(df_proc) > 0 else 0,
            'lim_inf': lim_inf, 'lim_sup': lim_sup
        }
        if tratar_outliers and conteo > 0:
            df_proc.loc[mask, 'salidas'] = df_proc['salidas'].median()

# 6. Negocios_CRM
elif "negocios" in hoja_seleccionada.lower():
    if 'numero_actividades' in df_proc.columns:
        df_proc['numero_actividades'] = pd.to_numeric(df_proc['numero_actividades'], errors='coerce').fillna(0)
        lim_inf, lim_sup, iqr, mask = detectar_outliers_iqr(df_proc['numero_actividades'])
        outliers_info['numero_actividades'] = {
            'count': mask.sum(), 'pct': (mask.sum() / len(df_proc)) * 100 if len(df_proc) > 0 else 0,
            'lim_inf': lim_inf, 'lim_sup': lim_sup
        }

# 7. Metas
elif "metas" in hoja_seleccionada.lower():
    if 'meta' in df_proc.columns:
        df_proc['meta'] = pd.to_numeric(df_proc['meta'], errors='coerce')
        lim_inf, lim_sup, iqr, mask = detectar_outliers_iqr(df_proc['meta'])
        outliers_info['meta'] = {
            'count': mask.sum(), 'pct': (mask.sum() / len(df_proc)) * 100 if len(df_proc) > 0 else 0,
            'lim_inf': lim_inf, 'lim_sup': lim_sup
        }

# ==============================================================================
# Métricas Ejecutivas Principales (Cards)
# ==============================================================================
total_filas = len(df_proc)
total_columnas = len(df_proc.columns)
nulos_totales_antes = nulos_antes.sum()
nulos_totales_despues = df_proc.isnull().sum().sum()
total_outliers_detectados = sum(info['count'] for info in outliers_info.values())

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric(
        label="Total de Registros",
        value=f"{total_filas:,}",
        help="Número total de filas registradas en la hoja"
    )

with col_kpi2:
    st.metric(
        label="Variables / Columnas",
        value=f"{total_columnas}",
        help="Cantidad de atributos disponibles en esta tabla"
    )

with col_kpi3:
    nulos_resueltos = nulos_totales_antes - nulos_totales_despues
    st.metric(
        label="Valores Nulos Corregidos",
        value=f"{nulos_resueltos:,}",
        delta=f"Restantes: {nulos_totales_despues:,}",
        delta_color="inverse" if nulos_totales_despues > 0 else "normal",
        help="Cantidad de valores nulos imputados mediante las reglas definidas"
    )

with col_kpi4:
    st.metric(
        label="Atípicos (Outliers) IQR",
        value=f"{total_outliers_detectados:,}",
        delta="Imputados c/ Mediana" if tratar_outliers else "Sin Modificar",
        delta_color="normal" if tratar_outliers else "off",
        help="Valores atípicos detectados por la regla de Tukey (1.5 IQR)"
    )

st.markdown("---")

# ==============================================================================
# Separación de Columnas Cuantitativas y Categóricas
# ==============================================================================
columnas_excluir_categoricas = {'id', 'folio', 'articulo_id', 'id_negocio', 'fecha_id', 'meta_id'}
cols_todas = df_proc.columns.tolist()

cols_numericas = []
cols_categoricas = []

for c in cols_todas:
    c_lower = c.lower()
    if 'fecha' in c_lower or 'date' in c_lower:
        cols_categoricas.append(c)
    elif pd.api.types.is_numeric_dtype(df_proc[c]):
        if any(exc in c_lower for exc in ['id', 'folio', 'codigo', 'cp', 'anio', 'dia']):
            cols_categoricas.append(c)
        else:
            cols_numericas.append(c)
    else:
        cols_categoricas.append(c)

# ==============================================================================
# Tabs Principales del Dashboard
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Calidad y Resumen",
    "Análisis Categórico",
    "Análisis Cuantitativo",
    "Datos y Descarga"
])

# ------------------------------------------------------------------------------
# TAB 1: Calidad y Resumen
# ------------------------------------------------------------------------------
with tab1:
    st.subheader(f"Diagnóstico de Calidad de Datos - Hoja: `{hoja_seleccionada}`")
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.markdown("##### Valores Faltantes (Nulos) por Columna")
        df_nulos = pd.DataFrame({
            'Variable': df_raw.columns,
            'Nulos Originales': nulos_antes.values,
            'Nulos Finales': df_proc.isnull().sum().values
        })
        df_nulos['% Faltante Inicial'] = (df_nulos['Nulos Originales'] / total_filas * 100).round(2)
        
        df_nulos_plot = df_nulos[df_nulos['Nulos Originales'] > 0].sort_values('Nulos Originales', ascending=True)
        if not df_nulos_plot.empty:
            fig_nulos = px.bar(
                df_nulos_plot,
                x='Nulos Originales',
                y='Variable',
                orientation='h',
                text='Nulos Originales',
                color='Nulos Originales',
                color_continuous_scale=[[0, '#FCA5A5'], [1, '#DC2626']],
                title="Columnas con Valores Nulos (Antes de Limpieza)"
            )
            fig_nulos.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
            st.plotly_chart(fig_nulos, use_container_width=True)
        else:
            st.success("Esta hoja no presenta valores nulos en ninguna de sus columnas.")
        
        st.dataframe(df_nulos, use_container_width=True, hide_index=True)

    with col_c2:
        st.markdown("##### Diagnóstico de Valores Atípicos (Regla IQR)")
        if outliers_info:
            df_out_summary = pd.DataFrame([
                {
                    'Variable': k,
                    'Atípicos Detectados': v['count'],
                    '% del Total': f"{v['pct']:.2f}%",
                    'Límite Inferior': f"{v['lim_inf']:.2f}",
                    'Límite Superior': f"{v['lim_sup']:.2f}"
                }
                for k, v in outliers_info.items()
            ])
            st.dataframe(df_out_summary, use_container_width=True, hide_index=True)
            
            fig_out = px.bar(
                df_out_summary,
                x='Variable',
                y='Atípicos Detectados',
                text='Atípicos Detectados',
                color='Atípicos Detectados',
                color_continuous_scale=CLV_GRADIENT,
                title="Cantidad de Registros Atípicos por Variable Numérica"
            )
            fig_out.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
            st.plotly_chart(fig_out, use_container_width=True)
        else:
            st.info("No se configuraron variables cuantitativas con outliers en esta hoja o no aplican.")

# ------------------------------------------------------------------------------
# TAB 2: Análisis Univariado Categórico
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Análisis de Frecuencias de Variables Categóricas")
    
    # Manejo específico para Clasificación_Articulos (Jerarquías Nivel 1, 2 y 3 de la Actividad 2)
    if "clasificaci" in hoja_seleccionada.lower() and 'categoria' in df_proc.columns:
        st.info("Vista especializada de Clasificación de Artículos (Niveles de Taxonomía de la Actividad 2).")
        
        macro_cats = ['Consumible', 'Refaccion', 'Equipo', 'Accesorio', 'Software']
        flujos = ['Digital', 'Analogo']
        
        c_art1, c_art2 = st.columns(2)
        with c_art1:
            st.markdown("#### Nivel 1: Flujo de Trabajo")
            df_flujo = df_proc[df_proc['categoria'].isin(flujos)]['categoria'].value_counts().reset_index()
            df_flujo.columns = ['Flujo', 'Cantidad']
            fig_flujo = px.pie(
                df_flujo, names='Flujo', values='Cantidad',
                hole=0.45,
                color_discrete_sequence=[CLV_PRIMARY, CLV_NAVY],
                title="Proporción por Flujo de Trabajo"
            )
            fig_flujo.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_flujo, use_container_width=True)
            
        with c_art2:
            st.markdown("#### Nivel 2: Categorías Macro Oficiales")
            df_macro = df_proc[df_proc['categoria'].isin(macro_cats)]['categoria'].value_counts().reset_index()
            df_macro.columns = ['Categoría', 'Cantidad']
            fig_macro = px.pie(
                df_macro, names='Categoría', values='Cantidad',
                hole=0.45,
                color_discrete_sequence=CLV_QUALITATIVE,
                title="Distribución de Categorías Macro"
            )
            fig_macro.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_macro, use_container_width=True)
            
        st.markdown("#### Nivel 3: Subcategorías más Frecuentes")
        df_subcat = df_proc[~df_proc['categoria'].isin(flujos + macro_cats)]['categoria'].value_counts().head(top_n).reset_index()
        df_subcat.columns = ['Subcategoría', 'Frecuencia']
        fig_sub = px.bar(
            df_subcat, x='Frecuencia', y='Subcategoría', orientation='h',
            text='Frecuencia', color='Frecuencia', color_continuous_scale=CLV_GRADIENT
        )
        fig_sub.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
        st.plotly_chart(fig_sub, use_container_width=True)

    else:
        # Selector de variable categórica estándar
        if not cols_categoricas:
            st.warning("No se encontraron variables categóricas para graficar en esta hoja.")
        else:
            col_cat_sel = st.selectbox(
                "Selecciona una variable categórica para analizar:",
                options=cols_categoricas,
                index=0
            )
            
            # Tabla de frecuencias
            serie_cat = df_proc[col_cat_sel].astype(str)
            tabla_freq = serie_cat.value_counts().reset_index()
            tabla_freq.columns = [col_cat_sel, 'Frecuencia Absoluta']
            tabla_freq['Frecuencia Relativa (%)'] = (tabla_freq['Frecuencia Absoluta'] / len(serie_cat) * 100).round(2)
            tabla_freq['% Acumulado'] = tabla_freq['Frecuencia Relativa (%)'].cumsum().round(2)
            
            top_freq = tabla_freq.head(top_n)
            
            col_g1, col_g2 = st.columns([3, 2])
            
            with col_g1:
                st.markdown(f"##### Gráfico de Frecuencias: Top {top_n} `{col_cat_sel}`")
                tipo_grafico = st.radio(
                    "Tipo de Gráfico:",
                    options=["Barras Horizontales", "Barras Verticales", "Gráfica de Pastel / Dona"],
                    horizontal=True
                )
                
                if tipo_grafico == "Barras Horizontales":
                    fig_cat = px.bar(
                        top_freq,
                        x='Frecuencia Absoluta',
                        y=col_cat_sel,
                        orientation='h',
                        text='Frecuencia Absoluta',
                        color='Frecuencia Absoluta',
                        color_continuous_scale=CLV_GRADIENT,
                        title=f"Top {top_n} Categorías más Frecuentes"
                    )
                    fig_cat.update_layout(yaxis={'categoryorder': 'total ascending'}, height=450)
                elif tipo_grafico == "Barras Verticales":
                    fig_cat = px.bar(
                        top_freq,
                        x=col_cat_sel,
                        y='Frecuencia Absoluta',
                        text='Frecuencia Absoluta',
                        color='Frecuencia Absoluta',
                        color_continuous_scale=CLV_GRADIENT,
                        title=f"Top {top_n} Categorías más Frecuentes"
                    )
                    fig_cat.update_layout(height=450)
                else:
                    fig_cat = px.pie(
                        top_freq,
                        names=col_cat_sel,
                        values='Frecuencia Absoluta',
                        hole=0.4,
                        color_discrete_sequence=CLV_QUALITATIVE,
                        title=f"Distribución Top {top_n} ({col_cat_sel})"
                    )
                    fig_cat.update_traces(textposition='inside', textinfo='percent+label')
                    fig_cat.update_layout(height=450)
                
                st.plotly_chart(fig_cat, use_container_width=True)
                
            with col_g2:
                st.markdown(f"##### Tabla de Frecuencias")
                st.dataframe(tabla_freq.head(top_n), use_container_width=True, hide_index=True)
                
                n_unicos = df_proc[col_cat_sel].nunique()
                moda_val = df_proc[col_cat_sel].mode()[0] if not df_proc[col_cat_sel].mode().empty else "N/A"
                st.info(f"""
                **Resumen de la variable:**
                - Categorías distintas: **{n_unicos:,}**
                - Categoría más frecuente (Moda): **{moda_val}**
                - Frecuencia de la moda: **{tabla_freq.iloc[0]['Frecuencia Absoluta']:,}** ({tabla_freq.iloc[0]['Frecuencia Relativa (%)']}%)
                """)

    # Análisis temporal especializado si la hoja tiene compras o fechas
    if "compras" in hoja_seleccionada.lower() and 'fecha' in df_proc.columns:
        st.markdown("---")
        st.markdown("### Análisis de Estacionalidad y Temporalidad (Compras)")
        df_proc['fecha_dt'] = pd.to_datetime(df_proc['fecha'], errors='coerce')
        
        c_temp1, c_temp2 = st.columns(2)
        with c_temp1:
            df_anios = df_proc['fecha_dt'].dt.year.value_counts().sort_index().reset_index()
            df_anios.columns = ['Año', 'Órdenes de Compra']
            fig_anios = px.bar(
                df_anios, x='Año', y='Órdenes de Compra',
                text='Órdenes de Compra', color='Órdenes de Compra',
                color_continuous_scale=CLV_GRADIENT,
                title="Distribución Anual de Órdenes de Compra"
            )
            st.plotly_chart(fig_anios, use_container_width=True)
            
        with c_temp2:
            meses_map = {1:'Ene', 2:'Feb', 3:'Mar', 4:'Abr', 5:'May', 6:'Jun',
                         7:'Jul', 8:'Ago', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dic'}
            df_meses = df_proc['fecha_dt'].dt.month.map(meses_map).value_counts().reindex(meses_map.values()).reset_index()
            df_meses.columns = ['Mes', 'Órdenes de Compra']
            fig_meses = px.line(
                df_meses, x='Mes', y='Órdenes de Compra',
                markers=True, line_shape='spline',
                title="Estacionalidad Mensual de Órdenes (Ene - Dic)"
            )
            fig_meses.update_traces(line_color=CLV_PRIMARY, line_width=3, marker_size=8, marker_color=CLV_NAVY)
            st.plotly_chart(fig_meses, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: Análisis Univariado Cuantitativo
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Distribución de Variables Cuantitativas")
    
    if not cols_numericas:
        st.warning("No se identificaron variables numéricas continuas en esta hoja para análisis cuantitativo.")
    else:
        col_num_sel = st.selectbox(
            "Selecciona una variable cuantitativa para explorar:",
            options=cols_numericas,
            index=0
        )
        
        serie_num = pd.to_numeric(df_proc[col_num_sel], errors='coerce').dropna()
        
        # 1. Resumen Estadístico Completo
        st.markdown("##### Estadísticas Descriptivas")
        desc = serie_num.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]).to_frame().T
        desc['IQR'] = desc['75%'] - desc['25%']
        desc['Sesgo (Skewness)'] = serie_num.skew()
        desc['Curtosis'] = serie_num.kurtosis()
        
        st.dataframe(desc.style.format("{:,.2f}"), use_container_width=True)
        
        # 2. Visualización combinada (Boxplot + Histograma con colores CLV)
        st.markdown("##### Distribución Visual (Diagrama de Caja e Histograma)")
        
        fig_comb = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.3, 0.7],
            subplot_titles=[f"Boxplot de {col_num_sel}", f"Histograma de Distribución de {col_num_sel}"]
        )
        
        # Boxplot con azul cian CLV
        fig_comb.add_trace(
            go.Box(
                x=serie_num, name="", orientation='h', 
                marker_color=CLV_PRIMARY, line_color=CLV_PRIMARY, 
                fillcolor='rgba(0, 178, 255, 0.25)', boxpoints='outliers'
            ),
            row=1, col=1
        )
        
        # Histograma con azul marino corporativo CLV
        fig_comb.add_trace(
            go.Histogram(
                x=serie_num, name="Frecuencia", 
                marker_color=CLV_NAVY, marker_line_color=CLV_PRIMARY, 
                marker_line_width=1, opacity=0.85
            ),
            row=2, col=1
        )
        
        fig_comb.update_layout(
            height=500,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x'
        )
        st.plotly_chart(fig_comb, use_container_width=True)
        
        # 3. Agrupación en Clases mediante Regla de Sturges (Actividad 2)
        st.markdown("---")
        st.markdown("##### Agrupación en Clases (Regla de Sturges)")
        
        k_sturges, v_min, v_max, ancho_int = calcular_regla_sturges(serie_num)
        
        col_sturg1, col_sturg2, col_sturg3, col_sturg4 = st.columns(4)
        col_sturg1.metric("Número de Clases (k)", f"{k_sturges}")
        col_sturg2.metric("Valor Mínimo", f"{v_min:,.2f}")
        col_sturg3.metric("Valor Máximo", f"{v_max:,.2f}")
        col_sturg4.metric("Ancho del Intervalo (i)", f"{ancho_int:,.2f}")
        
        cortes = np.linspace(v_min, v_max, k_sturges + 1)
        clases = pd.cut(serie_num, bins=cortes, include_lowest=True)
        tabla_clases = clases.value_counts().sort_index().reset_index()
        tabla_clases.columns = ['Intervalo de Clase', 'Frecuencia']
        tabla_clases['Frecuencia (%)'] = (tabla_clases['Frecuencia'] / len(serie_num) * 100).round(2)
        tabla_clases['Intervalo de Clase'] = tabla_clases['Intervalo de Clase'].astype(str)
        
        col_t1, col_t2 = st.columns([1, 1])
        with col_t1:
            st.dataframe(tabla_clases, use_container_width=True, hide_index=True)
        with col_t2:
            fig_clases = px.bar(
                tabla_clases,
                x='Intervalo de Clase',
                y='Frecuencia',
                text='Frecuencia',
                color='Frecuencia',
                color_continuous_scale=CLV_GRADIENT,
                title="Frecuencia por Intervalo de Sturges"
            )
            fig_clases.update_layout(xaxis_tickangle=-45, height=350, showlegend=False)
            st.plotly_chart(fig_clases, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 4: Datos y Descarga
# ------------------------------------------------------------------------------
with tab4:
    st.subheader(f"Vista Detallada de Datos Procesados: `{hoja_seleccionada}`")
    
    st.markdown("Puedes filtrar, ordenar y explorar las filas resultantes de esta hoja:")
    st.dataframe(df_proc, use_container_width=True)
    
    st.markdown("---")
    st.markdown("##### Exportar Datos Limpios")
    
    col_d1, col_d2, _ = st.columns([1, 1, 2])
    
    # Descargar CSV
    csv_bytes = df_proc.to_csv(index=False).encode('utf-8')
    with col_d1:
        st.download_button(
            label="Descargar como CSV",
            data=csv_bytes,
            file_name=f"{hoja_seleccionada}_procesada.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    # Descargar Excel
    with col_d2:
        excel_bytes = generar_excel_descarga(df_proc)
        st.download_button(
            label="Descargar como Excel",
            data=excel_bytes,
            file_name=f"{hoja_seleccionada}_procesada.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
