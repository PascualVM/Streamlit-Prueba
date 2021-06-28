import streamlit as st
import pandas as pd

header = st.beta_container()
datac = st.beta_container()
form = st.beta_container()
geocontext = st.beta_container()





with header:
    st.title('Hola')

with datac:
    st.header('Prueba de tabla')
    com_data = pd.read_csv('comunidadesIndigenasCorregido.txt',encoding='latin-1')
    st.write(com_data.head(5))



with form:
    st.header('Formulario')

    sel_col, disp_col = st.beta_columns(2)
    lista_comunas = list(set(com_data['Com']))
    lista_comunas.sort()
    input_comuna = sel_col.selectbox('Seleccione su comuna', options=lista_comunas)
    filtro_comuna = (com_data['Com'] == input_comuna)
    lista_comunidades = list(set(com_data.loc[filtro_comuna,'COMUNIDAD']))
    lista_comunidades.sort()
    input_comunidad = sel_col.selectbox('Nombre de la comunidad', options=lista_comunidades)
    filtro_comunidad = (com_data['COMUNIDAD'] == input_comunidad)
    latlon = com_data.loc[filtro_comunidad,['lat','lon']]
    # st.write(latlon)
    sel_col.text('Seleccione radio para evaluar contexto geográfico')

    input_radio = sel_col.slider('Seleccione radio de busqueda geográfica (km)', min_value=5, max_value=100, value=25, step=5)


    disp_col.subheader('Ubicación de la comunidad')

    disp_col.map(latlon)


with geocontext:
    st.header('Geocontexto de la comunidad')
    id_comunidad = com_data.loc[filtro_comunidad]['FID'].index[0]
    geo_data = pd.read_csv('comunidadesIndigenas_geoContexto100km.txt',encoding='latin-1')
    filtro_geo = (geo_data['IN_FID'] == id_comunidad)
    geo_data_filtrada = geo_data.loc[filtro_geo]
    geo_data_interes = geo_data_filtrada[geo_data_filtrada.NEAR_FC.isin(['Subestaciones','Lineas_de_Transmision','Reservas_Nacionales'])]
    filtro_distancia = (geo_data_interes['NEAR_DIST'] <= input_radio/100)
    geo_data_distancia = geo_data_interes.loc[filtro_distancia]
    infra = st.beta_expander('Infraestructura Electrica')
    with infra:
        col_1, col_2= st.beta_columns(2)
        filtro_subestaciones = (geo_data_distancia['NEAR_FC'] == 'Subestaciones')
        filtro_transmision = (geo_data_distancia['NEAR_FC'] == 'Lineas_de_Transmision')
        col_1.text('Subestacion')
        if geo_data_distancia[filtro_subestaciones].empty:
            col_2.text('No hay a menos de '+ str(input_radio) +' km')
        else:
            subestaciones = geo_data_distancia[filtro_subestaciones]
            dist = subestaciones['NEAR_DIST'].min()
            col_2.text(str("{:.2f}".format(dist*100)) + ' km')
        col_1.text('Lineas de Transmision')
        if geo_data_distancia[filtro_transmision].empty:
            col_2.text('No hay a menos de '+ str(input_radio) +' km')
        else:
            lineas = geo_data_distancia[filtro_transmision]
            dist = lineas['NEAR_DIST'].min()
            col_2.text(str("{:.2f}".format(dist*100)) + ' km')
    protec = st.beta_expander('Áreas Protegidas')
    with protec:
        col_1, col_2= st.beta_columns(2)
        filtro_reservas = (geo_data_distancia['NEAR_FC'] == 'Reservas_Nacionales')
        col_1.text('Resesrvas Nacionales')
        if geo_data_distancia[filtro_reservas].empty:
            col_2.text('No hay a menos de '+ str(input_radio) +' km')
        else:
            reservas = geo_data_distancia[filtro_reservas]
            dist = reservas['NEAR_DIST'].min()
            col_2.text(str("{:.2f}".format(dist*100)) + ' km')
