import streamlit as st
import sqlite3
import pandas as pd



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

st.markdown(
        """
        <style>
            [class="step-up st-emotion-cache-zbmw0q e116k4er1"]{

                display: none;
            }
            [class="eyeqlp51 st-emotion-cache-bubqsq ex0cdmw0"]{

                display: none;
            }
        """,
        unsafe_allow_html=True,
    )
def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")
# Crear la conexión a la base de datos SQLite
conn = sqlite3.connect('gestor_gastos.db')
cursor = conn.cursor()

# Crear tabla para gastos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        importe REAL,
        fecha DATE
    )
''')

# Crear tabla para ingresos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingresos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cantidad REAL,
        fecha DATE
    )
''')

# Función para agregar un gasto a la base de datos
def agregar_gasto(producto, importe, fecha):
    cursor.execute('INSERT INTO gastos (producto, importe, fecha) VALUES (?, ?, ?)', (producto, importe, fecha))
    conn.commit()

# Función para agregar un ingreso a la base de datos
def agregar_ingreso(cantidad, fecha):
    cursor.execute('INSERT INTO ingresos (cantidad, fecha) VALUES (?, ?)', (cantidad, fecha))
    conn.commit()

# Función para obtener el saldo actual
def obtener_saldo():
    # Obtener la suma de ingresos
    total_ingresos = cursor.execute('SELECT COALESCE(SUM(cantidad), 0) FROM ingresos').fetchone()[0]

    # Obtener la suma de gastos
    total_gastos = cursor.execute('SELECT COALESCE(SUM(importe), 0) FROM gastos').fetchone()[0]

    # Calcular el saldo restando los gastos de los ingresos
    saldo = total_ingresos - total_gastos

    return saldo

# Función para obtener gastos entre dos fechas y el total del importe gastado
def obtener_gastos_entre_fechas(fecha_inicio, fecha_fin):
    gastos_entre_fechas = cursor.execute('''
        SELECT * FROM gastos
        WHERE fecha BETWEEN ? AND ?
    ''', (fecha_inicio, fecha_fin)).fetchall()

    total_importe = cursor.execute('''
        SELECT COALESCE(SUM(importe), 0)
        FROM gastos
        WHERE fecha BETWEEN ? AND ?
    ''', (fecha_inicio, fecha_fin)).fetchone()[0]

    return gastos_entre_fechas, total_importe

# Página principal
st.title("Control de  Gastos Diarios")
egreso, ingreso, consulta = st.tabs(["Gastos", "Ingreso de Dinero", "Consultas"])

with ingreso:
    # Sección para agregar ingresos mensuales
    st.header("Ingresos Mensuales")
    cantidad_ingreso = st.number_input("Ingrese la cantidad de dinero:", min_value=0.0, step=1.0)
    fecha_ingreso = st.date_input("Ingrese la fecha del ingreso:", pd.to_datetime('today').date())
    if st.button("Agregar Ingreso"):
        agregar_ingreso(cantidad_ingreso, fecha_ingreso)
        st.info("Ingreso Agregado")

with egreso:
    # Sección para agregar gastos diarios
    st.header("Gastos Diarios")
    producto = st.text_input("Nombre del Producto:")
    importe = st.number_input("Importe del Gasto:", min_value=0.0, step=1.0)
    fecha_gasto = st.date_input("Fecha del Gasto:", pd.to_datetime('today').date())
    if st.button("Agregar Gasto"):
        agregar_gasto(producto, importe, fecha_gasto)
        st.info("Gasto Agregado")
with consulta:
    # Sección para consultar gastos entre fechas
    st.header("Consultar Gastos entre Fechas")
    fecha_inicio_consulta = st.date_input("Fecha de Inicio:", pd.to_datetime('today').date())
    fecha_fin_consulta = st.date_input("Fecha de Fin:", pd.to_datetime('today').date())
    if st.button("Consultar Gastos"):
        gastos_entre_fechas, total_importe = obtener_gastos_entre_fechas(fecha_inicio_consulta, fecha_fin_consulta)
        if gastos_entre_fechas:
            df_gastos_entre_fechas = pd.DataFrame(gastos_entre_fechas, columns=['ID', 'Producto', 'Importe', 'Fecha'])
            st.dataframe(df_gastos_entre_fechas)
            st.write(f"Total del importe gastado entre las fechas seleccionadas: ${total_importe}")
        else:
            st.warning("No hay gastos entre las fechas seleccionadas.")

# Mostrar saldo actual
st.header("Saldo Actual")
saldo_actual = obtener_saldo()
st.header(f"Tu saldo actual es: ${saldo_actual}")

# Cerrar la conexión a la base de datos
conn.close()
