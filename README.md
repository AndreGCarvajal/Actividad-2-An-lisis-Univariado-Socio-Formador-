# Actividad 2: Análisis Univariado y Dashboard Interactivo - Socio Formador CLV México

Este repositorio contiene el preprocesamiento, limpieza de datos, análisis exploratorio univariado (EDA) y la aplicación web interactiva en **Streamlit** desarrollada para el socio formador **CLV México**.

---

## Contenido del Repositorio

### 1. Cuadernos de Jupyter (Jupyter Notebooks)
* `CLV_Valores_Nulos.ipynb`: Tratamiento inicial de valores faltantes e imputación en CRM y almacén.
* `1_Analisis_Ventas.ipynb`: Preprocesamiento, detección de outliers (IQR) y frecuencias de ventas.
* `2_Analisis_Existencias.ipynb`: Análisis univariado y distribución de existencias de inventario.
* `3_Analisis_Compras.ipynb`: Análisis temporal de órdenes de compra, estacionalidad mensual y distribución de unidades.
* `4_Analisis_Articulos.ipynb`: Taxonomía y clasificación de artículos (Flujo, Macro-categorías y Subcategorías).
* `5y6_Salidas_Almacen_y_Ventas_Negadas_CRM.ipynb`: Motivos de pérdida de venta y agrupación por regla de Sturges.
* `7_Negocios_CRM.ipynb`: Embudo comercial, etapas de prospección y actividades.
* `8_Metas.ipynb`: Distribución y cumplimiento de metas por región.

---

### 2. Dashboard Interactivo en Streamlit (`dashboard_univariado.py`)
Aplicación web corporativa con diseño profesional inspirado en **CLV México** (tecnología dental CAD-CAM):

* **Carga de Archivo Excel y Selección de Hojas:** Selector dinámico de cualquier tabla del libro de datos.
* **Diagnóstico de Calidad de Datos:** Visualización y conteo de valores nulos y outliers detectados por Rango Intercuartílico (IQR).
* **Análisis Categórico Univariado:** Tablas de frecuencia, porcentaje y gráficas interactivas con Plotly (barras, donas, treemaps).
* **Análisis Cuantitativo y Regla de Sturges:** Boxplots combinados con histogramas y cálculo automático de intervalos de clase.
* **Descarga de Datos:** Exportación directa de bases tratadas a CSV y Excel.

---

## Cómo Ejecutar el Dashboard

1. Instalar dependencias necesarias:
```bash
pip install streamlit pandas numpy plotly openpyxl
```

2. Ejecutar la aplicación:
```bash
streamlit run dashboard_univariado.py
```