import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide"
)

@st.cache
def carga_data():
  return pd.read_excel("carga-bip.xlsx", header=9)

# Se lee la información de forma óptima
bip = carga_data()

st.sidebar.write("Visualizaciones de Datos Geográficos en Internet")

st.write("# Visualizaciones Parte 2")

st.write("## Ejemplo de Visualización en Mapa")

# Obtener parte de la información
geo_puntos_comuna = bip[ ["CODIGO","NOMBRE FANTASIA", "CERRO BLANCO 625", "MAIPU", "LATITUD", "LONGITUD"]].rename(columns={
  "NOMBRE FANTASIA": "Negocio", 
  "CERRO BLANCO 625": "Dirección", 
  "MAIPU": "Comuna",
})
geo_puntos_comuna.dropna(subset=["Comuna"], inplace=True)

with st.sidebar:
  # Obtener los nombres unicos de comunas
  comunas = geo_puntos_comuna["Comuna"].sort_values().unique()

  comunas_seleccionadas = st.multiselect(
    label="Filtrar por Comuna", 
    options=comunas,
    help="Selecciona las comunas a mostrar",
    default=[] # También se puede indicar la variable "comunas", para llenar el listado
  )


geo_data = geo_puntos_comuna

# Aplicar filtro de Comuna
if comunas_seleccionadas:
  geo_data = geo_puntos_comuna.query("Comuna == @comunas_seleccionadas")

st.sidebar.write(geo_data.set_index("CODIGO"))

# Obtener el punto promedio entre todas las georeferencias
avg_lat = np.average(geo_data["LATITUD"])
avg_lng = np.average(geo_data["LONGITUD"])

puntos_mapa = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lng,
        zoom=10,
        pitch=20,
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
    tooltip={
      "html": "<b>Negocio: </b> {Negocio} <br /> "
              "<b>Dirección: </b> {Dirección} <br /> "
              "<b>Comuna: </b> {Comuna} <br /> "
              "<b>Código: </b> {CODIGO} <br /> "
              "<b>Georeferencia (Lat, Lng): </b>[{LATITUD}, {LONGITUD}] <br /> "
    }
)

st.write(puntos_mapa)

