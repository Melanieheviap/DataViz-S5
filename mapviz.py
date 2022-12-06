import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np

# Establecimiento de configuración de página de Streamlit
st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide"
)

# Creación de Caché de Streamlit a partir de una función (cosa que no se ejecute multiples veces cuando se haga el llamado a la función)
@st.cache
def carga_data():
  return pd.read_excel("carga-bip.xlsx", header=9)

# Se asigna la carga de los datos hacia una variable que representa un dataframe donde está todo el conjunto de datos qeu haya obtenido con el archivo excel
bip = carga_data()

# Elemento de sidebar de Streamlit (barrita de al lado izquierdo)
st.sidebar.write("Visualizaciones de Datos Geográficos en Internet")

# Escritura simple con Streamlit dentro de la página (títulos, subtítulos, etc)
st.write("# Visualizaciones Parte 2")

st.write("## Ejemplo de Visualización en Mapa")

# Obtener parte de la información. Filtro del dataframe inicial con ciertas columnas solamente. 
# Renombre de las columnas que tienen el encabezado mal
geo_puntos_comuna = bip[ ["CODIGO","NOMBRE FANTASIA", "CERRO BLANCO 625", "MAIPU", "LATITUD", "LONGITUD"]].rename(columns={
  "NOMBRE FANTASIA": "Negocio", 
  "CERRO BLANCO 625": "Dirección", 
  "MAIPU": "Comuna",
})
# Del dataframe que resulta del paso anterior, se le pueden quitar los daos en blanco a determinadas columnas, en este caso, columna "Comuna" que tiene campos vacios
geo_puntos_comuna.dropna(subset=["Comuna"], inplace=True)

# Bloque de operaciones asociado al sidebar:
with st.sidebar:
  # Obtención del listado de las comunas unicas y ordenadas para poder generar un 
  # control de multiselector que me permite interactuar o filtrar la información que voy a mostrar en la grilla del sidebar 
  # y también en el mapa que esta desplegado en la zona central 
  comunas = geo_puntos_comuna["Comuna"].sort_values().unique()

  comunas_seleccionadas = st.multiselect(
    label="Filtrar por Comuna", 
    options=comunas,
    help="Selecciona las comunas a mostrar",
    default=[] # También se puede indicar la variable "comunas", para llenar el listado
  )

# De no seleccionar ninguna comuna, se le asigna a una variable (geo_data) todo el conjunto de datos de este dataframe filtrado (geo_puntos_comuna)
geo_data = geo_puntos_comuna

# Si tengo algunas comunas seleccionadas, se filtra el resultado de geo_data a partir de este dataframe que ya tengo filtrado, para decir qué condición quiero
# obtener ahora un nuevo filtro de datos
if comunas_seleccionadas:
  geo_data = geo_puntos_comuna.query("Comuna == @comunas_seleccionadas")

# Escritura de la tabla en el sidebar, indicadno además que el indice de esta tabla de datos filtrados por el query corresponde a la columna de "CODIGO".
# permitiendo que la primera columna de esta tabla se muestre el codigo de cada registro
st.sidebar.write(geo_data.set_index("CODIGO"))

# Con las funciones de NumPy se obtiene el punto promedio entre todas las georeferencias
avg_lat = np.average(geo_data["LATITUD"])
avg_lng = np.average(geo_data["LONGITUD"])

# Generación un componente de mapa. Con una capa de información adicional (layers)
# La vista inicial del mapa va a estar centrada en base al punto promedio de lat y long que se obtuvo previamente.
puntos_mapa = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lng,
        zoom=10,
        pitch=10,
    ),
    layers=[
      pdk.Layer(
        "ScatterplotLayer",
        data = geo_data,
        pickable=True,
        get_position='[LONGITUD, LATITUD]',
        opacity=0.8,
        filled=True,
        radius_scale=2,
        radius_min_pixels=5,
        radius_max_pixels=50,
        line_width_min_pixels=0.01,
      )      
    ],
    # También se define la interación del mapa (tooltip), que dictamina qué pasa cuando se pase el mouse encima del mapa
    tooltip={
      "html": "<b>Negocio: </b> {Negocio} <br /> "
              "<b>Dirección: </b> {Dirección} <br /> "
              "<b>Comuna: </b> {Comuna} <br /> "
              "<b>Código: </b> {CODIGO} <br /> "
              "<b>Georeferencia (Lat, Lng): </b>[{LATITUD}, {LONGITUD}] <br /> "
    }
)

st.write(puntos_mapa)

