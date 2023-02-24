import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import pandas_gbq

st.set_page_config(layout="wide")

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10000 min.
@st.cache_data(ttl=60000)
def read_dataframe(query):
    dataframe = pandas_gbq.read_gbq(query, project_id= "pi-soy-henry", credentials=credentials)
    return dataframe

#Importamos datos

sql_hechos = """
SELECT * FROM `pi-soy-henry.migrations.hechos`
"""
hechos = read_dataframe(sql_hechos)
hechos = hechos.sort_values('anio' ,ascending=True)

label_indicators_dict = {'Migración Neta':'SM.POP.NETM','PIB (UMN a precios actuales)':'NY.GDP.MKTP.CN','PIB per cápita (UMN actual)':'NY.GDP.PCAP.CN','Idoneidad de los programas de trabajo y protección social (porcentaje del bienestar total de los hogares beneficiarios)':'per_allsp.adq_pop_tot','Idoneidad de los programas de seguro social (porcentaje del bienestar total de los hogares beneficiarios)':'per_si_allsi.adq_pop_tot','Remesas de trabajadores y compensación de empleados, pagadas (US$ a precios actuales)':'BM.TRF.PWKR.CD.DT','Crecimiento del PIB per cápita (porcentaje anual)':'NY.GDP.PCAP.KD.ZG','Crecimiento del PIB (porcentaje anual)':'NY.GDP.MKTP.KD.ZG','Consumo de sal iodada (porcentaje de hogares) ': 'SN.ITK.SALT.ZS','Entradas de población extranjera por nacionalidad ':'B11','Salidas de población extranjera por nacionalidad ':'B12','Stock de población nacida en el extranjero por país de nacimiento':'B14','Stock de población extranjera por nacionalidad':'B15'}

label_indicators_filtrados_dict = {'Migración Neta':'SM.POP.NETM','PIB (UMN a precios actuales)':'NY.GDP.MKTP.CN','PIB per cápita (UMN actual)':'NY.GDP.PCAP.CN','Idoneidad de los programas de trabajo y protección social (porcentaje del bienestar total de los hogares beneficiarios)':'per_allsp.adq_pop_tot','Idoneidad de los programas de seguro social (porcentaje del bienestar total de los hogares beneficiarios)':'per_si_allsi.adq_pop_tot','Remesas de trabajadores y compensación de empleados, pagadas (US$ a precios actuales)':'BM.TRF.PWKR.CD.DT','Crecimiento del PIB per cápita (porcentaje anual)':'NY.GDP.PCAP.KD.ZG','Crecimiento del PIB (porcentaje anual)':'NY.GDP.MKTP.KD.ZG'}

datos_a_excluir = ['Africa Eastern', 'Africa Western', 'World', 'Early', 'dividend','Europe & Central Asia', 'European Union', 'Euro area', 'Fragile','Heavily', 'High', 'IBRD', 'IDA', 'Latin', 'Low', 'Middle', 'North America', 'OECD', 'Other small', 'Post-', 'Pre-', 'Upper', ]

### Helper Methods ###
def get_unique_anios(df_data):
    #devuelve los valores unicos de hechos['anio'] en forma de lista
    unique_anios = df_data['anio'].unique().tolist()
    return unique_anios

def get_unique_pais(df_data):
    #devuelve los valores unicos de hechos['pais'] en forma de lista
    unique_pais = df_data['pais'].unique().tolist()
    unique_pais = sorted(unique_pais)
    return unique_pais

def get_unique_nationality(df_data):
    #devuelve los valores unicos de hechos['nationality'] en forma de lista
    unique_nationality = df_data['nationality'].tolist()
    unique_nationality = unique_nationality.unique()
    return unique_nationality

def get_unique_cod_indicador(df_data):
    #devuelve los valores unicos de hechos['cod_indicador'] en forma de lista
    unique_cod_indicador = df_data['cod_indicador'].tolist()
    unique_cod_indicador = unique_cod_indicador.unique()
    return unique_cod_indicador

def filter_anio(df_data):
    df_filtered_anios = pd.DataFrame()
    anios = df_data['anio'].unique().tolist() #season list "13-14"
    start_raw = start_anio
    end_raw = end_anio
    start_index = anios.index(start_raw)
    end_index = anios.index(end_raw)+1
    anios_selected = anios[start_index:end_index]
    df_filtered_anios = df_data[df_data['anio'].isin(anios_selected)]
    return df_filtered_anios

def filter_pais(df_data):
    df_filtered_pais = pd.DataFrame()
    if all_paises_selected == 'Seleccionar paises y regiones manualmente':
        df_filtered_pais = df_data[df_data['pais'].isin(selected_paises)]
        return df_filtered_pais
    return df_data

def find_indicador_value_pais(min_max,attribute):
    df_find = df_data_filtered
    condicion_exclusion = False
    for palabra in datos_a_excluir:
        condicion_exclusion = condicion_exclusion | df_find['pais'].str.contains(palabra)

    mascara = ~condicion_exclusion
    df_find = df_find.loc[mascara]

    search_attribute = label_indicators_dict[attribute]
    
    df_find = df_find.loc[df_find['codigo_indicador'] == search_attribute]

    if(min_max == "Valor minimo"):
        return_indicador_value_pais = df_find(df_find.nsmallest(1, 'valor') & df_find['valor'] != 0)
    if(min_max == "Valor maximo"):
        return_indicador_value_pais = df_find.nlargest(1, 'valor')
    return return_indicador_value_pais



####################
### INTRODUCCIÓN ###
####################

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('Grupo10 - Analizador de Migraciones')
with row0_2:
    st.text("")
    st.subheader('Streamlit App')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("La migración es un fenómeno global que afecta a muchas personas en todo el mundo. Hay muchas razones por las que la gente decide emigrar, incluyendo motivos económicos, políticos, sociales y de seguridad. Algunos de los desafíos más comunes que enfrentan los migrantes incluyen la discriminación, la falta de recursos, apoyo, y la separación de sus seres queridos. ")
    st.markdown("Queremos proporcionarte una herramienta útil y accesible, para ayudarte tomar decisiones informadas sobre tu destino de emigración.")
    st.markdown("Podrás encontrar el codigo fuente en [PF Henry GitHub Repository](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones)")

#################
### SELECTION ###
#################

st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

### YEAR RANGE ###
st.sidebar.markdown("**Aquí puedes filtrar datos** 👇")
unique_dates = get_unique_anios(hechos)
start_anio, end_anio = st.sidebar.select_slider('Seleccione el periodo de años que desea incluir: ', unique_dates, value= [ 1960 , 2021 ])
df_data_filtered_anio = filter_anio(hechos)  

### COUNTRY SELECTION ###
unique_paises = get_unique_pais(df_data_filtered_anio)
all_paises_selected = st.sidebar.selectbox('¿Quieres incluir paises o regiones en específico? Si tu respuesta es sí, cliquea en la caja debajo y selecciona los paises en el nuevo campo.', ['Incluir todos los paises y regiones','Seleccionar paises y regiones manualmente'])
if all_paises_selected == 'Seleccionar paises y regiones manualmente':
    selected_paises = st.sidebar.multiselect("Selecciona los paises y regiones que deseas incluir en el analysis. Puedes borrar la actual selección clickeando el boton X a la derecha", unique_paises, default = unique_paises)
df_data_filtered = filter_pais(df_data_filtered_anio)   

### SEE DATA ###
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader("Datos actualmente seleccionados:")

row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5   = st.columns((.2, 1.6, .2, 1.6, .2, 1.6, .2, 1.6, .2))
with row2_1:
    unique_anios_in_df = df_data_filtered.anio.nunique()
    str_anios = "🗓️ " + str(unique_anios_in_df) + " Años diferentes"
    st.markdown(str_anios)
with row2_2:
    unique_paises_in_df = len(df_data_filtered['pais'].unique().tolist())
    t = " Paises/Regiones"
    if(unique_paises_in_df==1):
        t = " Pais/Región"
    str_paises = "🌎 " + str(unique_paises_in_df) + t
    st.markdown(str_paises)
with row2_3:
    total_data_in_df = df_data_filtered['pais'].count()
    str_data = "📊 " + str(total_data_in_df) + " Datos"
    st.markdown(str_data)

row3_spacer1, row3_1, row3_spacer2 = st.columns((.2, 7.1, .2))
with row3_1:
    st.markdown("")
    see_data = st.expander('Puedes hacer click aquí para ver los datos sin procesar 👉')
    with see_data:
        st.dataframe(data=df_data_filtered.reset_index(drop=True))
st.text('')

################
### ANALYSIS ###
################

### DATA EXPLORER ###
row12_spacer1, row12_1, row12_spacer2 = st.columns((.2, 7.1, .2))
with row12_1:
    st.subheader('Encontrar KPI')
    st.markdown('Muestra el pais (o los paises) con...')  

if all_paises_selected == 'Incluir todos los paises y regiones':

    row13_spacer1, row13_1, row13_spacer2, row13_2, row13_spacer3, row13_3, row13_spacer4   = st.columns((.2, 2.3, .2, 2.3, .2, 2.3, .2))
    with row13_1:
        show_me_hi_lo = st.selectbox ("", ["Valor maximo","Valor minimo"], key = 'hi_lo') 
    with row13_2:
        show_me_aspect = st.selectbox ("", list(label_indicators_filtrados_dict.keys()), key = 'what')

    row14_spacer1, row14_1, row14_spacer2 = st.columns((.2, 7.1, .2))
    with row14_1:
        return_indicador_value_pais = find_indicador_value_pais(show_me_hi_lo,show_me_aspect)
        st.write(return_indicador_value_pais)
    #    df_match_result = build_matchfacts_return_string(return_indicador_value_pais,show_me_hi_lo,show_me_aspect)
#
    #row15_spacer1, row15_1, row15_2, row15_3, row15_4, row15_spacer2  = st.columns((0.5, 1.5, 1.5, 1, 2, 0.5))
    #with row15_1:
    #    st.subheader(" ")
    #with row15_2:
    #    st.subheader(str(df_match_result.iloc[0]['pais']))
    #with row15_3:
    #    end_result = str(df_match_result.iloc[0]['goals']) + " : " +str(df_match_result.iloc[1]['goals'])
    #    ht_result = " ( " + str(df_match_result.iloc[0]['ht_goals']) + " : " +str(df_match_result.iloc[1]['ht_goals']) + " )"
    #    st.subheader(end_result + " " + ht_result)  
    #with row15_4:
    #    st.subheader(str(df_match_result.iloc[1]['pai']))
else:
    row17_spacer1, row17_1, row17_spacer2 = st.columns((.2, 7.1, .2))
    with row17_1:
        st.warning('Unfortunately this analysis is only available if all teams are included')
