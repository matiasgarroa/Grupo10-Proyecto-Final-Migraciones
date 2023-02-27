# FLUJOS MIGRATORIOS PROYECTO END TO END</b>
### OBJETIVO GENERAL
El objetivo general del proyecto es proporcionar una herramienta útil y accesible
para ayudar a los emigrantes argentinos, y de igual manera a las personas que
desean emigrar a Argentina. A tomar decisiones informadas sobre su destino de
emigración. La herramienta se enfocará en datos objetivos y personalizados para
cada usuario, y sería un recurso valioso para aquellos que buscan un futuro mejor y
más estable.

### OBJETIVOS ESPECÍFICOS
1. Recopilar y analizar datos relevantes sobre diferentes destinos de emigración
para calificar y comparar sus fortalezas y debilidades en términos de
seguridad, economía, calidad de vida, cultura, accesibilidad a servicios
públicos y oportunidades de trabajo y educación.
2. Realizar Data Pipeline, para poder implementar una base de datos, para
montarlo en un servicio de cloud (google cloud).
3. Creación de Dashboards, KPIs y métricas que enseñen los principales
resultados sobre los factores que influyen en las migraciones.
4. Desarrollar un modelo de machine learning que permita a los usuarios
identificar sus prioridades y recibir recomendaciones personalizadas sobre el
destino de emigración más adecuado para ellos.
5. Producir un repositorio en la plataforma Github, disponiendo el proyecto a la
comunidad, para que esta expongan mejoras para futura versiones del
proyecto

### INGENIERIA DE DATOS.
### ARQUITECTURA
![](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones/blob/main/Semana%202/arquitectura%20GCP.png)
Al tener un área de "landing zone", se puede validar la calidad de los datos recibidos antes de que entren al proceso de ETL. Esto permite detectar y corregir errores o inconsistencias en los datos antes de que se procesen y almacenen en el sistema. Asimismo, al tener un área de "staging", se puede hacer una validación adicional y preparar los datos para su transformación, lo que ayuda a mejorar aún más la calidad de los datos procesados y cargados en el sistema final.

Flexibilidad y escalabilidad: Al tener un área de "landing zone" y un área de "staging", se puede diseñar un proceso de ETL escalable y flexible. Esto permite agregar nuevas fuentes de datos y transformaciones sin interrumpir el flujo de datos existente. Además, se pueden realizar pruebas y experimentos en el área de "staging" sin afectar los datos del sistema final, lo que facilita el desarrollo y mejora de nuevos procesos de ETL.

### FUENTE DE DATOS:
BANCO MUNDIAL y OCDE

### EXTRACCIÓN DE DATOS: 
Extraemos los datos mediante la API del banco mundial y de la OCDE
### TRANSFORMACIÓN DE DATOS
Realizamos una limpieza y transformamos los datos para asegurarnos de que estén estandarizados y sean coherentes con los estándares del Data Ware house.
### CARGA DE DATOS
Realizamos la carga de datos con Python y Pandas.
### MANTENIMIENTO Y ACTUALIZACIÓN:
garantizamos que el data Ware House esté actualizado, automatizando el proceso con Apache Airflow, generando con Python el proceso de extracción y transformación. Con la finalidad de tener la información disponible para respaldar los procesos de toma de decisiones.

### DATA ANALYTICS.
### KPIs:
1. Migración Neta sudamerica.
2. Crecimiento del PBI en % Anual
3. Crecimiento del PBI per capita.
4. Remesas.
5. Idoneidad de los programas de seguro social
##### flujo migratorios dashboards 
![](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones/blob/main/Semana%203/flow%20map.jpeg)
##### Visualización de los kpis 1,2 y 3 
![](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones/blob/main/Semana%203/dashboard%20kpi%20(PIB%2C%20MIGRACION%20NETA).JPG)
