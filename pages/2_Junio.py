import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
# Configurar el tema de Streamlit
st.set_page_config(
    page_title="Control de Tiempo",
    page_icon="img/fondo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

image = Image.open('img/fondo.png')

# CSS para personalizar el estilo
st.markdown("""
    <style>
        .main {
            background-color: #B8CFE5;
            color: #02153B;
        }
        .stSelectbox label, .stButton button, .stSlider label, .stTextInput label {
            color: #02153B;
        }
        h1, h2, h3, h4 {
            color: #02153B;
        }
        .css-1ekf893 {
            background-color: #1f77b4;
        }
        .st-dx, .st-cn, .st-at {
            border: 2px solid #1f77b4;
            border-radius: 10px;
            padding: 10px;
        }
        header.css-18ni7ap {
            background-color: #0C1449;
        }
        header.css-18ni7ap .css-1v0mbdj, header.css-18ni7ap .css-1rs6os {
            color: #f0f2f6;
        }
        table.dataframe {
            text-align: center;
            margin-left: auto;
            margin-right: auto;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Control de Tiempo")

multi = '''***Con esta aplicación se puede verificar el cumplimiento de tiempos en una ruta determinada***

'''
st.markdown(multi)



# Especificar la ruta del archivo CSV
file_path = 'static/datasets/controlruta.csv'

# Leer el archivo CSV
try:
    df = pd.read_csv(file_path, encoding='utf-8', sep=';')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1', sep=';')

# Asegurarse de que los nombres de las columnas no tengan espacios al principio o al final
df.columns = df.columns.str.strip()

# Convertir la columna 'Fecha' a datetime
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%d/%m/%Y', errors='coerce')

# Filtrar las filas con fechas no convertibles
df = df.dropna(subset=['FECHA'])

df['CONTROL'] = df['CONTROL'].replace({'C1': 'Comfama'})
df['CONTROL'] = df['CONTROL'].replace({'C2': 'Haceb'})
df['CONTROL'] = df['CONTROL'].replace({'C3': 'HomeCenter'})
df['CONTROL'] = df['CONTROL'].replace({'C4': 'Terminal Tte.'})
df['CONTROL'] = df['CONTROL'].replace({'C5': 'Cotrafa'})
df['CONTROL'] = df['CONTROL'].replace({'C6': 'Villanueva'})

# Obtener las opciones únicas de cada filtro
rutasU = sorted(df['RUTA'].unique())
vehiculosU = sorted(df['VEHICULO'].unique())
estadosU = sorted(df['ESTADO'].unique())
fechasU = sorted(df['FECHA'].unique())
conductoresU = sorted(df['CONDUCTOR'].unique())

# Configurar las columnas y selectores
col1, col2, col3, col4, col5, = st.columns(5)

with col1:
    rutasU.insert(0, "Todas")
    optionRuta = st.selectbox('Ruta', (rutasU))

with col2:
    vehiculosU.insert(0, "Todos")
    optionVehiculo = st.selectbox('Vehículo', (vehiculosU))

with col3:
    estadosU.insert(0, "Todos")
    optionEstado = st.selectbox('Estado', (estadosU))

with col4:
    fechasU.insert(0,"Todos")
    optionFecha = st.selectbox('Fecha', (fechasU))

with col5:
    conductoresU.insert(0,"Todos")
    optionConductor = st.selectbox('Conductor', (conductoresU))       

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionRuta != "Todas":
    filtered_data = filtered_data[filtered_data['RUTA'] == optionRuta]

if optionVehiculo != "Todos":
    filtered_data = filtered_data[filtered_data['VEHICULO'] == optionVehiculo]

if optionEstado != "Todos":
    filtered_data = filtered_data[filtered_data['ESTADO'] == optionEstado]

if optionFecha != "Todos":
    filtered_data = filtered_data[filtered_data['FECHA'] == optionFecha]

if optionConductor != "Todos":
    filtered_data = filtered_data[filtered_data['CONDUCTOR'] == optionConductor]        

# Crear un gráfico de barras para la cantidad de registros por ESTADO
registros_por_estado = filtered_data['ESTADO'].value_counts().reset_index()
registros_por_estado.columns = ['Estado', 'Cantidad']
fig_bar = px.bar(registros_por_estado, x='Estado', y='Cantidad', title='Cantidad de Registros por Estado')

# Crear un gráfico de líneas para la diferencia de tiempo (DIFERENCIA) a lo largo del tiempo (FECHA)
#fig_line = px.line(filtered_data, x='FECHA', y='DIFERENCIA', title='Diferencia de Tiempo a lo Largo del Tiempo')

# Crear un gráfico de pastel para la proporción de registros por ESTADO
fig_pie = px.pie(registros_por_estado, names='Estado', values='Cantidad', title='Proporción de Registros por Estado')

# Mostrar los gráficos
st.plotly_chart(fig_bar, use_container_width=True)
#st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)

if len(filtered_data) > 0:
    st.write(filtered_data, use_container_width=True)
else:
    st.write("No hay datos disponibles con los filtros seleccionados.")

# Filtro para mostrar los conductores con más de 60 registros cuyo estado sea "caída"
if st.checkbox('Mostrar conductores con más de 60 registros en estado "Caída"'):
    conductores_caida = filtered_data[filtered_data['ESTADO'] == 'Caida'].groupby('CONDUCTOR').size().reset_index(name='Cantidad')
    conductores_caida = conductores_caida[conductores_caida['Cantidad'] > 60]    
    st.write(conductores_caida[['CONDUCTOR', 'Cantidad']], use_container_width=True)

# Mostrar la tabla filtrada
# st.write("Datos filtrados", filtered_data)