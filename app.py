import pandas as pd
import streamlit as st
import plotly.express as px

# ************* CARGA DE LOS DATOS **************
ruta = 'https://github.com/Jorge-Hugo-Duarte-Guzman/practica-github/raw/refs/heads/main/data_sint_oper_pred_clas.csv'
df = pd.read_csv(ruta)

##########################################################################################################
#                           ANÁLISIS Y PROCESAMIENTO
##########################################################################################################

# ESTADÍSTICAS DE LA COLUMNA 'TIPO_VUELO'
df_tipo_vuelo = df['TIPO_VUELO'].value_counts().reset_index()
df_tipo_vuelo.columns = ['TIPO_VUELO', 'count']
estadisticos = df_tipo_vuelo['count'].describe()
maximo = estadisticos['max']
minimo = estadisticos['min']
media = estadisticos['mean']

# TOP 5 AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
df_top5_ops_aeropuertos = df['AEROPUERTO_OPERACION'].value_counts().reset_index().head(5)
df_top5_ops_aeropuertos.columns = ['AEROPUERTO', 'COUNT']

# TPO 10 RUTAS CON MAYOR NÚMERO DE OPERACIONES
df['RUTA'] = df['ORIGEN'] + ' - ' + df['DESTINO']
df_top10_rutas = df['RUTA'].value_counts().reset_index().head(10)
df_top10_rutas.columns = ['RUTA', 'CANTIDAD']

################################################################################
#                  CONFIGURACIÓN DE LA PÁGINA DE STREAMLIT
################################################################################

# Configuración de la página
st.set_page_config(
    page_title='Operaciones Acumuladas',
    layout='centered',
    initial_sidebar_state='collapsed'
)

# # Ajuste del ancho máximo del contenedor principal a 1200px
st.markdown(
    '''
    <style>
        .block-container {
            max-width: 1800px;
        }
    </style>
    ''',
    unsafe_allow_html=True
)             

#********* VISUALIZACION DE LOS DATOS *********
st.image('encabezado.png', use_container_width=True)
st.title('Datos Operaciones')

whit st.container(border):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Mínimo', f'{minimo:.0f}', border=True)
    with col2:
        st.metric('Media', f'{media:.0f}', border=True)
    with col3:
        st.metric('Máximo', f'{maximo:.0f}', border=True)

with st.expander('Ver Matriz de Datos'):
    st.dataframe(df)

with st.expander('Top 5 Aeropuertos con Mayor Número de Operaciones'):
    st.dataframe(df_top5_ops_aeropuertos)

with st.expander('Top 10 Rutas con Mayor Número de Operaciones'):
    st.dataframe(df_top10_rutas)

col4, col5 = st.columns(2)

with col4:
    #_______________________________________________________________________________________
    # ANÁLISIS AEROPUERTOS CON MAYOR NÚMERO DE OPERACIONES
    fig_barras = px.bar(
        df_top5_ops_aeropuertos, 
        x='AEROPUERTO', 
        y='COUNT', 
        title='Top 5 Aeropuertos con Mayor Número de Operaciones',
        labels={
            'AEROPUERTO': 'Aeropuerto',
            'COUNT': 'Número de Operaciones'
        },
        color='AEROPUERTO',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )   
    fig_barras.update_layout(showlegend=False)
    # Mostrar la gráfica de barras en Streamlit
    st.plotly_chart(fig_barras, use_container_width=True)

with col5:
    # # ANÁLISIS DE RUTAS
    fig_rutas = px.bar(
        df_top10_rutas.sort_values('CANTIDAD', ascending=True),
        x='CANTIDAD', 
    y='RUTA', 
    title='Top 10 Rutas con Mayor Número de Operaciones',
    color='CANTIDAD',
    color_continuous_scale='tealgrn'
    )
    fig_rutas.update_coloraxes(showscale=False)
    st.plotly_chart(fig_rutas, use_container_width=True)
# Opciones de personalización para las barras en cuanto al que 'showcale=False' es para oculta la barra de colores, 'color_continuous_scale' define la paleta de colores para las barras, y 'update_coloraxes' se utiliza para aplicar la configuración de color a la gráfica.

