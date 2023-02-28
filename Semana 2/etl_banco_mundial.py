import wbdata
import pandas as pd
import urllib.request
import os
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
)

default_args = {
    'owner': 'gian_rivas',
}

#ruta de archivos de  datos que vienen de la api al data lake
indicadores_path = '/home/airflow/gcs/data/indicadores.csv'
hechos_input_data_path = "/home/airflow/gcs/data/tabla_hechos.csv"
list_inicators_path = "/home/airflow/gcs/data/lista_indicadores.txt"
list_get_indicators = ["{'SM.POP.NETM':'valor'}", "{'NY.GDP.MKTP.CN':'valor'}", 
                        "{'NY.GDP.PCAP.CN':'valor'}", "{'per_allsp.adq_pop_tot':'valor'}", 
                        "{'per_si_allsi.adq_pop_tot':'valor'}", "{'BM.TRF.PWKR.CD.DT':'valor'}", 
                        "{'NY.GDP.PCAP.KD.ZG':'valor'}", "{'NY.GDP.MKTP.KD.ZG':'valor'}", 
                        "{'SN.ITK.SALT.ZS':'valor'}"]
mig_input_data_path = "/home/airflow/gcs/data/MIG.csv"

#ruta de datos de archivos de salida despues de la transformacion

hechos_output_data_path='/home/airflow/gcs/data/staging_area/tabla_hechos.csv'
indicators_data_outpath = '/home/airflow/gcs/data/staging_area/tabla_indicadores.csv'
mig_output_data_path = '/home/airflow/gcs/data/staging_area/tabla_hechos_mig.csv'


#extrayendo datos de la API del banco Mundial
def get_data_migration_world_bank(list_get_indicators):
    ###extraemos codigo de pais y nombre pais en un dataframe #######
    countries = wbdata.get_country()
    # Crear un dataframe vacÃ­o con dos columnas: cÃ³digo y nombre
    df_countries = pd.DataFrame(columns=['cod_country', 'country'])

    # Iterar a travÃ©s de la lista de paÃ­ses y agregar una nueva fila al dataframe para cada paÃ­s
    for country in countries:
        codigo_pais = country['id']
        nombre_pais = country['name']
        df_countries = df_countries.append({'cod_country': codigo_pais, 'country': nombre_pais}, ignore_index=True)

    #### extrayendo nombre ,pais, fecha, valor, codigo indicador
    DATA = pd.DataFrame(columns=['country', 'date', 'valor', 'code_indicator'])
    lista_indicadores = list_get_indicators

    #iteraremos el string creado para obtener los indicadores y asi obtener los datos que queremos
    for indicators in lista_indicadores:

        indicators = eval(indicators)
        print(indicators)
        NEW_DATA = wbdata.get_dataframe(indicators, country="all", data_date=None, freq='Y', source=None, convert_date=False, keep_levels=True, cache=True)
        NEW_DATA = pd.DataFrame(NEW_DATA)

        NEW_DATA = NEW_DATA.reset_index()
        for valor in indicators:
            NEW_DATA["code_indicator "] = valor

        NEW_DATA = pd.merge(NEW_DATA,df_countries,  on='country')

        DATA = pd.concat([DATA,NEW_DATA])
    DATA = DATA.drop('code_indicator', axis=1)
    DATA.to_csv('/home/airflow/gcs/data/tabla_hechos.csv',index = False)

def get_mig_data(mig_input_data_path):
    dls = 'https://stats.oecd.org/SDMX-JSON/data/MIG/AFG+ALB+DZA+AND+AGO+ATG+ARG+ARM+AUS+AUT+AZE+BHS+BHR+BGD+BRB+BLR+BEL+BLZ+BEN+BMU+BTN+BOL+BIH+BWA+BRA+BRN+BGR+BFA+BDI+KHM+CMR+CAN+CPV+CAF+TCD+CHL+CHN+COL+COM+COG+COK+CRI+CIV+HRV+CUB+CYP+CZE+PRK+COD+DNK+DJI+DMA+DOM+ECU+EGY+SLV+GNQ+ERI+EST+ETH+FJI+FIN+CSK+SUN+YUCS+FRA+GAB+GMB+GEO+DEU+GHA+GRC+GRD+GUM+GTM+GIN+GNB+GUY+HTI+HND+HKG+HUN+ISL+IND+IDN+IRN+IRQ+IRL+ISR+ITA+JAM+JPN+JOR+KAZ+KEN+KIR+KOR+KWT+KGZ+LAO+LVA+LBN+LSO+LBR+LBY+LIE+LTU+LUX+MAC+MKD+MDG+MWI+MYS+MDV+MLI+MLT+MHL+MRT+MUS+MEX+FSM+MDA+MCO+MNG+MNE+MAR+MOZ+MMR+NAM+NRU+NPL+NLD+NZL+NIC+NER+NGA+NIU+NOR+OMN+PAK+PLW+PSE+PAN+PNG+PRY+PER+PHL+POL+PRT+PRI+QAT+ROU+RUS+RWA+KNA+LCA+VCT+WSM+SMR+STP+SAU+SEN+SCG+SYC+SLE+SRB+SGP+SVK+SVN+SLB+SOM+ZAF+ESP+LKA+SDN+SUR+SWZ+SWE+CHE+SYR+TWN+TJK+TZA+THA+TLS+TGO+TKL+TON+TTO+TUN+TUR+TKM+TUV+UGA+UKR+ARE+GBR+USA+URY+UZB+VUT+VEN+VNM+YEM+ZMB+ZWE+TOT+NS+UUU+YYY.B11+B12+B14+B15+B16.TOT.AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA/all?contentType=csv'
    #outfilename= 'MIG_DESCARGA.CSV'
    proxy = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy)
    opener.addheaders = [
        ('User-Agent', ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) "
                        "AppleWebKit/603.1.30 (KHTML, like Gecko) "
                        "Version/10.1 Safari/603.1.30"
                        ))]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url=dls, filename=mig_input_data_path)


def create_staging_area():
    if  not os.path.exists('/home/airflow/gcs/data/staging_area'):
        os.mkdir('/home/airflow/gcs/data/staging_area')

################################ iniciando con la transformaciÃ³n de los datos ###########################

def transform_data_world_bank(hechos_input_data_path, hechos_output_data_path):
    tabla_hechos = pd.read_csv(hechos_input_data_path)
    #agregar transformaciones
    tabla_hechos.to_csv(hechos_output_data_path, index=False)

def transform_data_indicators(indicadores_path,indicators_data_outpath):
    tabla_indicadores = pd.read_csv(indicadores_path, sep = ';')
    #agregar indicadores_path
    tabla_indicadores.to_csv(indicators_data_outpath, index = False)

def transform_data_mig(mig_input_data_path,mig_output_data_path):
    tabla_hechos_mig = pd.read_csv(mig_input_data_path, sep= ',')
    campos = ['Country','Year','Value','VAR','COU','CO2','Country of birth/nationality']
    tabla_hechos_mig =tabla_hechos_mig[campos]

    tabla_hechos_mig.rename(columns={'Country':'country','Year':'date',
                        'Value':'valor','VAR':'code_indicator','COU':'cod_country','CO2':'cod_nationality','Country of birth/nationality':'nationality'},
                        inplace=True)
    tabla_hechos_mig.to_csv(mig_output_data_path,index=False)


with DAG(
    'proyecto_grupal_henry',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@weekly',
    tags=['etl','proyecto_grupal']
) as dag:
    dag.doc_md = "tareas_de_proyecto_grupal"

    t0 = PythonOperator(
        task_id='crear_staging_area',
        python_callable=create_staging_area,
    )

    t2 = PythonOperator(
        task_id='obtener_datos_de_API_world_bank',
        python_callable=get_data_migration_world_bank,
        op_kwargs={'list_get_indicators': list_get_indicators},
    )
    t3 = PythonOperator(
        task_id='obtener_datos_de_API_MIG',
        python_callable=get_mig_data,
        op_kwargs={'mig_input_data_path': mig_input_data_path},
    )

    t4 = PythonOperator(
        task_id='transformar_indicadores',
        python_callable=transform_data_indicators,
        op_kwargs={'indicadores_path': indicadores_path, 'indicators_data_outpath':indicators_data_outpath},
    )

    t5 = PythonOperator(
        task_id='transformar_hechos_banco_mundial',
        python_callable=transform_data_world_bank,
        op_kwargs={'hechos_input_data_path': hechos_input_data_path, 'hechos_output_data_path':hechos_output_data_path},
    )
    t6 = PythonOperator(
        task_id='transformar_hechos_mig',
        python_callable=transform_data_mig,
        op_kwargs={'mig_input_data_path': mig_input_data_path, 'mig_output_data_path':mig_output_data_path},
    )


    t7 = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset", 
        dataset_id='migrations'
    )

    t8 = BigQueryCreateEmptyTableOperator(
        task_id="crear_tabla_hechos",
        dataset_id='migrations',
        table_id="hechos",
        schema_fields=[
            {
                'mode': 'NULLABLE',
                'name': 'pais',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'anio',
                'type': 'FLOAT'
            },
            {
                'mode': 'NULLABLE',
                'name': 'valor',
                'type': 'FLOAT'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_indicador',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_pais',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_nacionalidad',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'nationality',
                'type': 'STRING'
            },
        ],
    )
    t9 = BigQueryCreateEmptyTableOperator(
        task_id="crear_tabla_indicadores",
        dataset_id='migrations',
        table_id="indicadores",
        schema_fields=[
            {
                'mode': 'NULLABLE',
                'name': 'indicator_code',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'indicator_name',
                'type': 'STRING'
            },

        ],
    )

    t10 = GCSToBigQueryOperator(
        task_id='LoadHechosToBigquery',
        bucket='us-central1-pg-migraciones-4d61f533-bucket',
        source_objects=['data/staging_area/tabla_hechos.csv'],
        field_delimiter =',',
        destination_project_dataset_table='migrations.hechos',
        skip_leading_rows=1,
        schema_fields=[
            {
                'mode': 'NULLABLE',
                'name': 'pais',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'anio',
                'type': 'FLOAT'
            },
            {
                'mode': 'NULLABLE',
                'name': 'valor',
                'type': 'FLOAT'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_indicador',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_pais',
                'type': 'STRING'
            },
        ],
        write_disposition='WRITE_APPEND',
    )
    t11 = GCSToBigQueryOperator(
        task_id='LoadMigDataToBigquery',
        bucket='us-central1-pg-migraciones-4d61f533-bucket',
        source_objects=['data/staging_area/tabla_hechos_mig.csv'],
        field_delimiter =',',
        destination_project_dataset_table='migrations.hechos',
        skip_leading_rows=1,
        schema_fields=[
            {
                'mode': 'NULLABLE',
                'name': 'pais',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'anio',
                'type': 'FLOAT'
            },
            {
                'mode': 'NULLABLE',
                'name': 'valor',
                'type': 'FLOAT'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_indicador',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_pais',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'codigo_nacionalidad',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'nationality',
                'type': 'STRING'
            },
        ],
        write_disposition='WRITE_APPEND',
    )
    t12 = GCSToBigQueryOperator(
        task_id='LoadIndicatorsToBigquery',
        bucket='us-central1-pg-migraciones-4d61f533-bucket',
        source_objects=['data/staging_area/tabla_indicadores.csv'],
        field_delimiter =',',
        destination_project_dataset_table='migrations.indicadores',
        skip_leading_rows=1,
        schema_fields=[
            {
                'mode': 'NULLABLE',
                'name': 'indicator_code',
                'type': 'STRING'
            },
            {
                'mode': 'NULLABLE',
                'name': 'indicator_name',
                'type': 'STRING'
            },
        ],
        write_disposition='WRITE_APPEND',
    )



    t0>> t2
    t2 >> t5
    t5 >> t10

    t0 >> t4
    t4 >> t7
    t7 >> t8
    t8 >> t10
    t8 >> t11
    t7 >> t9 
    t9 >> t12

    t0 >> t3
    t3 >> t6
    t6 >> t11