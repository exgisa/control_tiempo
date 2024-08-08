import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import io
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
        /* Estilo para centrar la tabla */
        table.dataframe {
            width: 100%;
            text-align: center !important;
        }
        /* Alineación central para las celdas de la tabla */
        table.dataframe td {
            text-align: center !important;
        }
        /* Alineación central para los encabezados de la tabla */
        table.dataframe th {
            text-align: center !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Control de Tiempo")

multi = '''***Con esta aplicación se puede verificar el cumplimiento de tiempos en una ruta determinada***

'''
st.markdown(multi)



# Especificar la ruta del archivo CSV
file_path = 'static/datasets/julio10.csv'

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

df['CONTROL'] = df['CONTROL'].replace({'C1': 'Comfama','C2': 'Haceb','C3': 'HomeCenter','C4': 'Terminal Tte.','C5': 'Cotrafa','C6': 'Villanueva'})

# Convertir la columna 'INICIO' a datetime
#df['INICIO'] = pd.to_datetime(df['INICIO'], format='%H:%M', errors='coerce').dt.time

# Crear un diccionario con las correspondencias
nro_interno = {str(i): f'B{i:03}' for i in range(1, 58)}

# Aplicar el reemplazo en la columna VEHICULO
df['VEHICULO'] = df['VEHICULO'].astype(str).replace(nro_interno)

# Obtener las opciones únicas de cada filtro
rutasU = sorted(df['RUTA'].unique())
vehiculosU = sorted(df['VEHICULO'].unique())
estadosU = sorted(df['ESTADO'].unique())
fechasU = sorted(df['FECHA'].unique())
conductoresU = sorted(df['CONDUCTOR'].unique())
horas_inicioU = sorted(df['INICIO'].unique())

# Configurar las columnas y selectores
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

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
    fechasU.insert(0,"Todas")
    optionFecha = st.selectbox('Fecha', (fechasU))

with col5:
    conductoresU.insert(0,"Todos")
    optionConductor = st.selectbox('Conductor', (conductoresU))     

with col6:
    horas_inicioU.insert(0, "Todas")
    optionHoraInicio = st.selectbox('Hora inicio', horas_inicioU)

with col7:
    horas_inicioU.insert(0, "Todas")
    optionHoraFin = st.selectbox('Hora fin', horas_inicioU)

# Filtrar los datos según las opciones seleccionadas
filtered_data = df
if optionRuta != "Todas":
    filtered_data = filtered_data[filtered_data['RUTA'] == optionRuta]

if optionVehiculo != "Todos":
    filtered_data = filtered_data[filtered_data['VEHICULO'] == optionVehiculo]

if optionEstado != "Todos":
    filtered_data = filtered_data[filtered_data['ESTADO'] == optionEstado]

if optionFecha != "Todas":
    filtered_data = filtered_data[filtered_data['FECHA'] == optionFecha]

if optionConductor != "Todos":
    filtered_data = filtered_data[filtered_data['CONDUCTOR'] == optionConductor]     

# if hora_inicio != "Todos":
#     filtered_data = filtered_data[filtered_data(filtered_data['INICIO'] >= hora_inicio) & (filtered_data['INICIO'] <= hora_fin)]

# if hora_fin != "Todos":
#     filtered_data = filtered_data[(filtered_data['INICIO'] >= hora_inicio) & (filtered_data['INICIO'] <= hora_fin)]

# Filtrar los datos según el rango de horas
if optionHoraInicio != "Todas" and optionHoraFin != "Todas":
    filtered_data = filtered_data[
    (filtered_data['INICIO'] >= optionHoraInicio) & (filtered_data['INICIO'] <= optionHoraFin)
]

# Crear un gráfico de barras para la cantidad de registros por ESTADO
registros_por_estado = filtered_data['ESTADO'].value_counts().reset_index()
registros_por_estado.columns = ['Estado', 'Cantidad']
fig_bar = px.bar(registros_por_estado, x='Estado', y='Cantidad', title='Cantidad de Registros por Estado')

# Crear un gráfico de pastel para la proporción de registros por ESTADO
fig_pie = px.pie(registros_por_estado, names='Estado', values='Cantidad', title='Proporción de Registros por Estado')

# Mostrar los gráficos
st.plotly_chart(fig_bar, use_container_width=True)
st.plotly_chart(fig_pie, use_container_width=True)

if len(filtered_data) > 0:
    st.write(filtered_data, use_container_width=True) 
    st.markdown('<style>table.dataframe {text-align: center;}</style>', unsafe_allow_html=True)
   
else:
    st.write("No hay datos disponibles con los filtros seleccionados.")

# Filtro para mostrar los conductores con más de 60 registros cuyo estado sea "caída"
if st.checkbox('Mostrar conductores con más de 60 registros en estado "Caída"'):
    conductores_caida = filtered_data[filtered_data['ESTADO'] == 'Caida'].groupby('CONDUCTOR').size().reset_index(name='Cantidad')
    conductores_caida = conductores_caida[conductores_caida['Cantidad'] > 60]    
    st.write(conductores_caida[['CONDUCTOR', 'Cantidad']], use_container_width=True)
