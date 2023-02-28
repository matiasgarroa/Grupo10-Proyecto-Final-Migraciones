<h1 align="center"> Informe de análisis de datos :bar_chart: 	:mag: </h1>

<p align="center">
   <img width="700" height="300" src="Imagenes/portada.png">
   </p>


# Tabla de contenidos
* [Introducción](#Introducción)

* [Objetivos](#Objetivos)

* [Metas](#Metas)

* [Público objetivo](#Público-objetivo)

* [Proceso preliminar](#Proceso-preliminar)

* [Dashboard](#Dashboard)

* [Principales tecnologías utilizadas](#Principales-tecnologías-utilizadas)

* [Información del proyecto](#Información-del-proyecto)

* [Conclusiones](#Conclusiones)

# Introducción
Para nuestro análisis de los flujos migratorios en Sudamérica, en la primera semana nos planteamos unos objetivos generales y específicos que nos sirven de guía en el desarrollo de este proyecto. Es importante tenerlos presentes en todo momento con el fin de concentrar esfuerzos y lograr el cumplimiento de dichos objetivos.

# Objetivos

A grandes rasgos tenemos tres objetivos:

* analizar los patrones y comportamientos asociados a los flujos migratorios en los países de Sudamérica tales como Brasil, Uruguay, Paraguay, Argentina, Colombia y Perú.
* Realizar un análisis comparativo entre los diferentes países de Sudamérica mencionados para identificar las similitudes y diferencias en los flujos migratorios, incluyendo las razones detrás de los movimientos migratorios.
* Crear un mapa interactivo que  indique cuales son los mejores lugares para emigrar y/o inmigrar de acuerdo al país en el que resida el ciudadano.

# Metas
Este proyecto tiene como objetivo extraer información a través de herramientas de visualización de datos para que las partes interesadas del proyecto puedan analizar y tomar decisiones informadas.


# Público objetivo

Los análisis hechos para este proyecto tienen como objetivo presentar a nuestro PO (Product Owner) las principales estadísticas de los flujos migratorios en los países de Sudamérica, para la toma de decisiones de la ONG internacional que nos contrató. Y por otro lado, disponibilizar una mapa interactivo para todos los habitantes de Sudamérica que deseen emigrar.
# Proceso preliminar

Una vez los datos procesados y subidos a la Base de datos que esta en GCP los conectamos con Power Bi para usar las tablas. Se aplico cierta limpieza a cada tabla para normalizarlas Se realizaron los siguientes cambios antes del análisis:

**Tablas**

* `hechos` 
    + Cambiamos el type de dato a la columna 'anio'
    + Cambiamos el nombre de la columna 'codigo_indicador' por 'indicator_code'
    + Quitamos los vacíos de la columna 'nationality
* `Indicadores`
    + Esta tabla no requería ningún cambio.

# Dashboard

* Contexto:
Para la creación del Dashboard se utilizó el software PowerBI, donde se crearon 2 Dashboards diferentes y un mapa interactivo, el primero enfocado en las estadísticas de las inmigraciones y el segundo en las estadísticas de las emigraciones.\
Para más información sobre los `KPIs`, puede ingresar al siguiente link [diccionario de KPIs](https://github.com/matiasgarroa/Grupo10-Proyecto-Final-Migraciones/blob/main/Semana%203/diccionario%20KPIs.md).

**Dashboard mapa interactivo**

Esta dashboard interactivo muestra los principales sitios a los que se puede viajar de acuerdo al país de residencia.
<p align="center">
   <img width="800" height="400" src="Imagenes/dashboard flow map.png">
   </p>

**Dashboard enfocado a inmigraciones:**

Esta dashboard resume las principales estadísticas de las inmigraciones en Sudamérica, así mismo muestra los KPIs que nos ayudan a ver el creciemiento económico de los países más atractivos para inmigrar.
<p align="center">
   <img width="800" height="400" src="Imagenes/dashboard inmigracion.png">
   </p>
En base a los kpis realizados se puede ver un crecimiento en el PBI per cápita del 172% respecto al año 171% con respecto al año anterior, lo cual muestra que estos países tienen economías fuertes y sostenibles.

+ Sugerencia: Los mejores países para inmigrar en sudamérica son Chile y Argentina que son los países con mayor numero de inmigrantes a través del tiempo.

**Dashboard enfocado a emigraciones:**

Esta dashboard resume las principales estadísticas de las emigraciones en Sudamérica, así mismo muestra los KPIs que nos ayudan a ver el creciemiento económico de los países más atractivos para inmigrar.
<p align="center">
   <img width="800" height="400" src="Imagenes/dashboard emigracion.png">
   </p>
En base a los kpis realizados se puede ver un decrecimiento en el PBI anual del -240% respecto al año anterior, las remesas enviadas a sus países de origen bajaron en 9,65% con respecto al año anterior, lo cual muestra que estos países tienen economías débiles.

+ Sugerencia: Entre los países que mayor emigración presentan a través del tiempo se encuentran países como Peru, Venezuela y Colombia los cuales se han visto afectados por distintos factores políticos, sociales, económicos, etc.
