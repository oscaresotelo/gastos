import streamlit as st
import sqlite3
from st_pages import Page, show_pages, add_page_title


col1, col2, col3 = st.columns([2,3,2])
# Create a cursor

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
                     .container {
                display: flex;
            }
            .logo-text {
                font-weight:700 !important;
                font-size:30px !important;
                color: black !important;
                padding-top: 50px !important;
            }
            .logo-img {
                float:right;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# st.markdown(
#     f"""
#     <div class="container">
#         <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}" > <br>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
with col1:
    
    st.info("mensaje")
with col2:
    st.title("Ingreso Sistema Principal")

    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    if "ingreso" not in st.session_state:
        st.session_state.ingreso = ""

    if "usuario" not in st.session_state:
        st.session_state.usuario = ""
    if "idusuario" not in st.session_state:
        st.session_state.idusuario = ""
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def login(user):
        st.session_state.ingreso = "ok"
        
        st.session_state.usuario = user
        
        st.write(st.session_state.usuario)
        if user == 'Oscar':
            
            st.success("Bienvenido Administrador!")
            
            show_pages([
                Page("inicio.py", "Cargar Gastos"),
                Page("login.py", "Login"),
                     
            ])
        

    # Create the login form

    if st.session_state.ingreso == "ok":
        st.title("Salir del Sistema")
        if st.button("salir"):
            del st.session_state.ingreso
            st.info("Salio Exitosamente del Sistema")
    else:
        st.header("Ingrese")
        placeholder = st.empty()
        with placeholder.form("Login"):
            username = st.text_input("Usuario")
            password = st.text_input("Password", type="password")
            ingresar = st.form_submit_button("Ingresar")
        if ingresar:
            if username == "Oscar":
    	        user = username

    	        if user is not None:
    	            login(user)
    	            placeholder.empty()
    	        else:
    	            st.error("Usuario o Contraseña Incorrecta")

    # Add a submit button
local_css("estilos.css")

    # Ejecutar la consulta SQL
with col3:
    
    st.info("segunda")