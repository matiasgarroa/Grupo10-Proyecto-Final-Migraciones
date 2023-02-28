import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import pandas_gbq
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px
import pickle
import numpy as np

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

modelos = []

# Cargar los modelos desde los archivos .pkl y añadirlos a la lista
for archivo in ['Modelos/Argentina_Migracion neta.pkl','Modelos/Argentina_PIB (US$ a precios actuales).pkl','Modelos/Argentina_PIB per capita (US$ a precios actuales).pkl','Modelos/Bolivia_Migracion neta.pkl','Modelos/Bolivia_PIB (US$ a precios actuales).pkl','Modelos/Bolivia_PIB per capita (US$ a precios actuales).pkl','Modelos/Brasil_Migracion neta.pkl','Modelos/Brasil_PIB (US$ a precios actuales).pkl','Modelos/Brasil_PIB per capita (US$ a precios actuales).pkl','Modelos/Chile_Migracion neta.pkl','Modelos/Chile_PIB (US$ a precios actuales).pkl','Modelos/Chile_PIB per capita (US$ a precios actuales).pkl','Modelos/Colombia_Migracion neta.pkl','Modelos/Colombia_PIB (US$ a precios actuales).pkl','Modelos/Colombia_PIB per capita (US$ a precios actuales).pkl','Modelos/Ecuador_Migracion neta.pkl','Modelos/Ecuador_PIB (US$ a precios actuales).pkl','Modelos/Ecuador_PIB per capita (US$ a precios actuales).pkl','Modelos/Paraguay_Migracion neta.pkl','Modelos/Paraguay_PIB (US$ a precios actuales).pkl','Modelos/Paraguay_PIB per capita (US$ a precios actuales).pkl','Modelos/Peru_Migracion neta.pkl','Modelos/Peru_PIB (US$ a precios actuales).pkl','Modelos/Peru_PIB per capita (US$ a precios actuales).pkl','Modelos/Uruguay_Migracion neta.pkl','Modelos/Uruguay_PIB (US$ a precios actuales).pkl','Modelos/Uruguay_PIB per capita (US$ a precios actuales).pkl','Modelos/Venezuela_Migracion neta.pkl','Modelos/Venezuela_PIB (US$ a precios actuales).pkl','Modelos/Venezuela_PIB per capita (US$ a precios actuales).pkl']:
    with open(archivo, 'rb') as f:
        modelo = pickle.load(f)
        modelos.append(modelo)

#Importamos datos

sql_hechos = """
SELECT * FROM `pi-soy-henry.migrations.hechos`
"""
hechos = read_dataframe(sql_hechos)
hechos = hechos.sort_values('anio' ,ascending=True)

label_indicators_dict = {'Migración Neta':'SM.POP.NETM','PIB (UMN a precios actuales)':'NY.GDP.MKTP.CN','PIB per cápita (UMN actual)':'NY.GDP.PCAP.CN','Idoneidad de los programas de trabajo y protección social (porcentaje del bienestar total de los hogares beneficiarios)':'per_allsp.adq_pop_tot','Idoneidad de los programas de seguro social (porcentaje del bienestar total de los hogares beneficiarios)':'per_si_allsi.adq_pop_tot','Remesas de trabajadores y compensación de empleados, pagadas (US$ a precios actuales)':'BM.TRF.PWKR.CD.DT','Crecimiento del PIB per cápita (porcentaje anual)':'NY.GDP.PCAP.KD.ZG','Crecimiento del PIB (porcentaje anual)':'NY.GDP.MKTP.KD.ZG','Consumo de sal iodada (porcentaje de hogares) ': 'SN.ITK.SALT.ZS','Entradas de población extranjera por nacionalidad ':'B11','Salidas de población extranjera por nacionalidad ':'B12','Stock de población nacida en el extranjero por país de nacimiento':'B14','Stock de población extranjera por nacionalidad':'B15'}

label_indicators_filtrados_dict = {'Migración Neta':'SM.POP.NETM','PIB (UMN a precios actuales)':'NY.GDP.MKTP.CN','PIB per cápita (UMN actual)':'NY.GDP.PCAP.CN','Idoneidad de los programas de trabajo y protección social (porcentaje del bienestar total de los hogares beneficiarios)':'per_allsp.adq_pop_tot','Idoneidad de los programas de seguro social (porcentaje del bienestar total de los hogares beneficiarios)':'per_si_allsi.adq_pop_tot','Remesas de trabajadores y compensación de empleados, pagadas (US$ a precios actuales)':'BM.TRF.PWKR.CD.DT','Crecimiento del PIB per cápita (porcentaje anual)':'NY.GDP.PCAP.KD.ZG','Crecimiento del PIB (porcentaje anual)':'NY.GDP.MKTP.KD.ZG'}

label_indicators_mapa = {'Entradas de población extranjera por nacionalidad ':'B11','Salidas de población extranjera por nacionalidad ':'B12','Stock de población nacida en el extranjero por país de nacimiento':'B14','Stock de población extranjera por nacionalidad':'B15'}

label_paises = {'Argentina', 'Uruguay', 'Colombia'}

datos_a_excluir = ['Africa Eastern', 'Africa Western', 'World', 'Early', 'dividend','Europe & Central Asia', 'European Union', 'Euro area', 'Fragile','Heavily', 'High', 'IBRD', 'IDA', 'Latin', 'Low', 'Middle', 'North America', 'OECD', 'Other small', 'Post-', 'Pre-', 'Upper', 'East Asia & Pacific', 'South Asia']
types = ["Media","Total","Mediana","Maximo","Minimo"]

paises_prediccion = {'Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Ecuador', 'Paraguay', 'Perú', 'Uruguay', 'Venezuela'}
label_predicciones = {'Migracion Neta':'Migracion neta', 'PBI': 'PIB (US$ a precios actuales)', 'PBI per capita': 'PIB per capita (US$ a precios actuales)'}


condicion_exclusion = False
for palabra in datos_a_excluir:
    condicion_exclusion = condicion_exclusion | hechos['pais'].str.contains(palabra)

mascara = ~condicion_exclusion
hechos = hechos.loc[mascara]

selected_paises = [] 

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
        df_find = df_find.loc[df_find['valor'] != 0]
        return_indicador_value_pais = df_find.nsmallest(1, 'valor')
    if(min_max == "Valor maximo"):
        return_indicador_value_pais = df_find.nlargest(1, 'valor')
    return return_indicador_value_pais

def group_measure_by_attribute(aspect,attribute,measure):
    df_data = df_pivot
    df_return = pd.DataFrame()
    if(measure == "Total"):
        if(attribute == "per_allsp.adq_pop_tot" or attribute == "per_si_allsi.adq_pop_tot" or attribute == "NY.GDP.PCAP.KD.ZG" or attribute == "NY.GDP.MKTP.KD.ZG"):
            measure = "Mean"
        else:
            df_return = df_data.groupby([aspect]).sum()            
    
    if(measure == "Media"):
        df_return = df_data.groupby([aspect]).mean()
        
    if(measure == "Mediana"):
        df_return = df_data.groupby([aspect]).median()
    
    if(measure == "Minimo"):
        df_return = df_data.groupby([aspect]).min()
    
    if(measure == "Maximo"):
        df_return = df_data.groupby([aspect]).max()
    
    df_return["aspect"] = df_return.index
    if aspect == "team":
        df_return = df_return.sort_values(by=[attribute], ascending = False)
    return df_return

########################
### ANALYSIS METHODS ###
########################

def plot_x_per_anio(attr,measure):
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 12,
          'axes.labelsize': 12,
          'xtick.labelsize': 12,
          'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### Goals
    attribute = label_indicators_filtrados_dict[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute("anio",attribute,measure)
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot, color = "#b80606")
    y_str = measure + " " + attr + " " + " por país]"
    if measure == "Total":
        y_str = measure + " " + attr
    if measure == "Minimo" or measure == "Maximo":
        y_str = measure + " " + attr + " por país"
        
    ax.set(xlabel = "Año", ylabel = y_str)
    if measure == "Media" or attribute in ["per_allsp.adq_pop_tot","per_si_allsi.adq_pop_tot","NY.GDP.PCAP.KD.ZG","NY.GDP.MKTP.KD.ZG"]:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 15),
                   textcoords = 'offset points')
    else:
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 15),
                   textcoords = 'offset points')
    st.pyplot(fig)

def plot_x_per_pais(attr,measure):
    rc = {'figure.figsize':(8,4.5),
          'axes.facecolor':'#0e1117',
          'axes.edgecolor': '#0e1117',
          'axes.labelcolor': 'white',
          'figure.facecolor': '#0e1117',
          'patch.edgecolor': '#0e1117',
          'text.color': 'white',
          'xtick.color': 'white',
          'ytick.color': 'white',
          'grid.color': 'grey',
          'font.size' : 8,
          'axes.labelsize': 12,
          'xtick.labelsize': 8,
          'ytick.labelsize': 12}
    
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    ### Goals
    attribute = label_indicators_filtrados_dict[attr]
    df_plot = pd.DataFrame()
    df_plot = group_measure_by_attribute("pais",attribute,measure)
    
    ax = sns.barplot(x="aspect", y=attribute, data=df_plot.reset_index(), color = "#b80606")
    y_str = measure + " " + attr + " " + "per Game"
    if measure == "Total":
        y_str = measure + " " + attr
    if measure == "Minimo" or measure == "Maximo":
        y_str = measure + " " + attr + "in a Game"
    ax.set(xlabel = "Pais", ylabel = y_str)
    plt.xticks(rotation=66,horizontalalignment="right")
    if measure == "Media" or attribute in ["per_allsp.adq_pop_tot","per_si_allsi.adq_pop_tot","NY.GDP.PCAP.KD.ZG","NY.GDP.MKTP.KD.ZG"]:
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
    else:
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 18),
                   rotation = 90,
                   textcoords = 'offset points')
    st.pyplot(fig)

def build_resultado_return_string(return_indicador_value_pais,min_max,attribute):
    df_find_result = return_indicador_value_pais
    anio = int(return_indicador_value_pais['anio'].iloc[0])
    pais = str(return_indicador_value_pais['pais'].iloc[0])
    valor = str(return_indicador_value_pais['valor'].iloc[0])
    string1 = ''
    if (min_max == 'Valor minimo'):
        min_max = 'valor minimo'
    else:
        min_max = 'valor maximo'

    if (attribute == 'Migración Neta'):
        string1 =  "Nuestra consulta nos remonta al año " + str(anio) + ", donde " + pais + " tuvo una migración neta con un " + min_max + " de " + str(valor)
    elif (attribute == 'Idoneidad de los programas de trabajo y protección social (porcentaje del bienestar total de los hogares beneficiarios)'):
        string1 =  "Nuestra consulta nos remonta al año " + str(anio) + ", donde  " + pais + " tuvo una idoneidad de los programas de trabajo y protección social con un " + min_max + " de " + str(valor)
    elif (attribute == 'Idoneidad de los programas de seguro social (porcentaje del bienestar total de los hogares beneficiarios)'):
        string1 =  "Nuestra consulta nos remonta al año " + str(anio) + ", donde  " + pais + " tuvo una idoneidad de los programas de seguro social con un " + min_max + " de " + str(valor)
    elif (attribute == 'Remesas de trabajadores y compensación de empleados, pagadas (US$ a precios actuales)'):
        string1 =  "Nuestra consulta nos remonta al año " + str(anio) + ", donde el " + min_max + " que " + pais + " pagó, fué de " + str(valor) + ' en remesas de trabajadores y compensación de empleados'    
    else:
        string1 =  "Nuestra consulta nos remonta al año " + str(anio) + ", donde  " + pais + " tuvo un " + attribute + " con un " + min_max + " de " + str(valor)
    
    st.markdown(string1)
    return df_find_result

def mapa_lat(pais, attr):
    
    attribute = label_indicators_mapa[attr]

    df_mapa = hechos.loc[(hechos['nationality'] == pais)]
    df_mapa = df_mapa.loc[(df_mapa['codigo_indicador'] == attribute)]

    fig = px.choropleth(df_mapa, 
                        locations='codigo_pais', 
                        color='valor',
                        title='Unión de ' + df_mapa['nationality'].iloc[0] + ' con otros países')

    st.plotly_chart(fig)
    return df_mapa

def hacer_prediccion(pais, model, anio):
    kpi = label_predicciones[model]
    
    with open(f'Modelos/{pais}_{kpi}.pkl', "rb") as f:
        modelo = pickle.load(f)

    dato_anio = np.array([2026]).reshape(1, -1)
    prediccion = modelo.predict(dato_anio)
    prediccion = str(prediccion[0][0])
    resultado = 'La predicción de ' + model + ' para ' + pais + ' en el año ' + anio + ' es de: '
    st.markdown(resultado)
    st.write(prediccion)
    return resultado


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
    st.markdown('Muestra el pais con el...')  

if all_paises_selected == 'Incluir todos los paises y regiones':

    row13_spacer1, row13_1, row13_spacer2, row13_2, row13_spacer3 = st.columns((.2, 2.3, .2, 5, .2))
    with row13_1:
        show_me_hi_lo = st.selectbox ("", ["Valor maximo","Valor minimo"], key = 'hi_lo') 
    with row13_2:
        show_me_aspect = st.selectbox ("", list(label_indicators_filtrados_dict.keys()), key = 'what')

    row14_spacer1, row14_1, row14_spacer2 = st.columns((.2, 7.1, .2))
    with row14_1:
        return_indicador_value_pais = find_indicador_value_pais(show_me_hi_lo,show_me_aspect)
        df_find_result = build_resultado_return_string(return_indicador_value_pais,show_me_hi_lo,show_me_aspect)

    row15_spacer1, row15_1, row15_2, row15_spacer2  = st.columns((0.5, 4.5, 1.5, 0.5))
    with row15_1:
        st.subheader(str(df_find_result.iloc[0]['pais']))
    with row15_2:
        st.subheader('Año ' + str(int(df_find_result.iloc[0]['anio'])))
else:
    row17_spacer1, row17_1, row17_spacer2 = st.columns((.2, 7.1, .2))
    with row17_1:
        st.warning('Este analisis solo está disponible seleccionando todos los paises')

if all_paises_selected == 'Incluir todos los paises y regiones':
    row16_spacer1, row16_1, row16_2, row16_spacer2  = st.columns((0.5, 4.5, 1.5, 0.5))
    with row16_1:
        st.markdown('Migración Neta')
        st.markdown('PIB (UMN a precios actuales)')
        st.markdown("Crecimiento del PIB")
        st.markdown('PIB per cápita (UMN actual)')
        st.markdown("Crecimiento del PIB per cápita")
        st.markdown("Idoneidad de los programas de trabajo y protección social")
        st.markdown("Idoneidad de los programas de seguro social")
        st.markdown("Remesas de trabajadores y compensación de empleados")
        st.markdown("*nan = Valor Faltante")

    with row16_2:
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'SM.POP.NETM'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'NY.GDP.MKTP.CN'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'NY.GDP.PCAP.KD.ZG'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'NY.GDP.PCAP.CN'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'NY.GDP.MKTP.KD.ZG'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'per_allsp.adq_pop_tot'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'per_si_allsi.adq_pop_tot'), 'valor'].values[0]))
        st.markdown(" " + str(df_data_filtered.loc[(df_data_filtered['anio'] == df_find_result.iloc[0]['anio']) &   (df_data_filtered['codigo_indicador'] == 'BM.TRF.PWKR.CD.DT'), 'valor'].values[0]))

### PAIS ###
#Cambiamos formato del df (los valores de 'codigo_pais' ahora son columnas)
df_pivot = df_data_filtered.pivot(index=['pais', 'anio','codigo_pais','codigo_nacionalidad','nationality'], columns='codigo_indicador', values='valor')
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Analisis por país')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row5_1:
    st.markdown('Consulta una variedad de estadísticas sobre distintos paises. ')    
    plot_x_per_pais_selected = st.selectbox ("¿Qué atributo deseas analizar?", list(label_indicators_filtrados_dict.keys()), key = 'attribute_pais')
    plot_x_per_pais_type = st.selectbox ("¿Qué medida deseas analizar?", types, key = 'measure_pais')
with row5_2:
    if len(selected_paises) > 0 and len(selected_paises) <= 10:
        plot_x_per_pais(plot_x_per_pais_selected, plot_x_per_pais_type)
    if len(selected_paises) > 10 or all_paises_selected == 'Incluir todos los paises y regiones':
        st.warning('Selecciona maximo 10 paises')
    else:
        st.warning('Por favor selecciona al menos un pais')

if selected_paises:
    st.write(type(selected_paises))

### ANIO ###
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Analisis por año')
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row7_1:
    st.markdown('Consulta una variedad de estadísticas por año.')    
    plot_x_per_anio_selected = st.selectbox ("¿Qué atributo deseas analizar?", list(label_indicators_filtrados_dict.keys()), key = 'attribute_anio')
    plot_x_per_anio_type = st.selectbox ("¿Qué medida deseas analizar?", types, key = 'measure_anio')
with row7_2:
    if len(selected_paises) > 0 and len(selected_paises) <= 10:
        plot_x_per_anio(plot_x_per_anio_selected,plot_x_per_anio_type)
    if len(selected_paises) > 10 or all_paises_selected == 'Incluir todos los paises y regiones':
        st.warning('Selecciona maximo 10 paises')
    else:
        st.warning('Por favor selecciona al menos un pais')

#########

### MAPA ###
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Paises mas visitados por latinoamericanos')
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row7_1:
    st.markdown('Consulta cuales son los paises latinoamericanos mas elegidos a la hora de migrar.')    
    paises_lat = st.selectbox ("¿Qué pais deseas visualizar?", label_paises, key = 'pais_mapa')
    pais_indicador = st.selectbox ("¿Qué atributo deseas analizar?", list(label_indicators_mapa.keys()), key = 'codigo_indicador')
    
with row7_2:
    mapa_lat(paises_lat, pais_indicador)
    
### MACHINE LEARNING ###
row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Predicciones con Machine Learning')
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
with row7_1:
    st.markdown('Realiza estimaciones hacerca de Migraciones y PBI de paises latinoamericanos.')    
    pais_predict = st.selectbox ("¿En qué pais deseas realizar la predicción?", paises_prediccion, key = 'paises_prediccion')
    modelo_predict = st.selectbox ("¿Qué prediccion deseas ejecutar?", list(label_predicciones.keys()), key = 'label_predicciones')
    anio_predict = st.slider ("Escoge el año de tu predicción:", 2022, 2030)
    
with row7_2:
    hacer_prediccion(pais_predict, modelo_predict, anio_predict)