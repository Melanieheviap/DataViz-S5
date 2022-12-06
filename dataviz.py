from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(
  page_icon=":thumbs_up:",
  layout="wide"
)

# esto es un decorador de cache de Streamlit
@st.cache
def carga_data():
  return pd.read_excel("carga-bip.xlsx", header=9)

# Se lee la información de forma óptima
bip = carga_data()

st.sidebar.write("## Visualizaciones de Datos en Internet")
btn_ver = st.sidebar.button("Ver gráficos")

st.write("# Visualizaciones Parte 2")

st.write("## Ejemplo de selección de múltiple")
# Obtener los nombres unicos de comunas
# Existe un punto de carga sin comuna
comunas = bip["MAIPU"].sort_values().unique() 

col_1, col_2 = st.columns(2, gap="medium")

with col_1:
  comunas_seleccionadas = st.multiselect(
    "Comunas", 
    options=comunas, 
    default=[]
  )

with col_2:
  st.write("Comunas seleccionadas: ")
  st.info(comunas_seleccionadas)

st.write("## Ejemplos de Gráficos :star-struck: ")

if not btn_ver:
  st.warning("Presiona el botón **Ver gráficos** de la barra lateral")
else:
  # Obtener el total de puntos por comuna
  puntos_comuna = bip.groupby(by=["MAIPU"]).size()

  # Grafico de barras
  barra = plt.figure()
  puntos_comuna.plot.bar(
    xlabel="Comunas",
    ylabel="Puntos de carga"
  ).plot()

  # Gráfico de area
  area = plt.figure()
  puntos_comuna.plot.area(
    xlabel="Comunas",
    ylabel="Puntos de carga"
  ).plot()

  # Gráfico de línea
  linea = plt.figure()
  puntos_comuna.plot.line(
    xlabel="Comunas",
    ylabel="Puntos de carga"
  ).plot()

  # Gráfico de pie
  pie = plt.figure()
  puntos_comuna.plot.pie(
    xlabel="Comunas",
    ylabel="Puntos de carga"
  ).plot()

  graf1, graf2 = st.columns(2)
  graf3, graf4 = st.columns([2,3])

  with graf1:
    st.write("### Grafico de Barra")
    st.pyplot(barra)
    
  with graf2:
    st.write("### Grafico de Área")
    st.pyplot(area)
    
  with graf3:
    st.write("### Grafico de Línea")
    st.pyplot(linea)
    
  with graf4:
    st.write("### Grafico de Torta")
    st.pyplot(pie)
    