import streamlit as st

# Configurar el tema de Streamlit
st.set_page_config(
    page_title="Control de Ruta",
    page_icon=":DirectionBus:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS para personalizar el estilo
st.markdown("""
    <style>
        /* Fondo y texto principal */
        .main {
            background-color: #f1f1f1;
            color: #000000;
            
        }
        /* Texto y elementos */
        .stSelectbox label, .stButton button, .stSlider label, .stTextInput label {
            color: #000000;
        }
        h1, h2, h3, h4 {
            color: #000000;
        }
        /* Títulos de los gráficos */
        .css-1ekf893 {
            background-color: #1f77b4;
        }
        .st-dx, .st-cn, .st-at {
            border: 2px solid #1f77b4;
            border-radius: 10px;
            padding: 10px;
        }
        /* Barra superior */
        header.css-18ni7ap {
            background-color: #505C72;
        }
            
        .css-1aumxhk {
        background-color: #505C72; /* Cambia el color del menú de páginas */
        
        /* Configuración y texto de la barra superior */
        header.css-18ni7ap .css-1v0mbdj, header.css-18ni7ap .css-1rs6os {
            color: #505C72;
        }
    </style>
""", unsafe_allow_html=True)

# st.title("Expreso Girardota S.A.")
st.image("img/fondo.png", width=600)
# st.markdown("""
#     <div style="text-align: center; font-size: 18px; color: #F9FA;">
#         Disfruta de nuestro contenido
#     </div>
# """, unsafe_allow_html=True)
# st.write("Elizabeth Restrepo" )
# st.write("Richard Blanco")
# st.write("Norbey Hernandez")