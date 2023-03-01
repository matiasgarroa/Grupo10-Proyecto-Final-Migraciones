<h1 align="center"> Modelos de Machine Learning  </h1>

<p align="center">
   <img width="700" height="400" src="Imagenes/portada ML.png">
   </p>


# Tabla de contenidos
* [Introducción](#Introducción)

* [Objetivos](#Objetivos)

* [Selección modelo](#Selección-modelo)

* [Tecnologías utilizadas](#Tecnologías-utilizadas)

# Introducción
En esta parte del proyecto, hemos desarrollado modelos de prediccion usando herramientas de aprendizaje automático son de gran importancia para predecir el desarrollo económico en Suramérica. 

# Objetivos
El objetivo del modelo de Machine Learning realizado es brindar información predictiva al usuario, esta será referida al valor del PBI y la cantidad de migrantes que poseerá el país que elija para los años futuros que solicite, con el objetivo de poner a su disposición información complementaria.
 
 ## Selección del modelo
 Para poder realizar nuestro objetivo hemos decidido utilizar un modelo de Regresión Lineal Simple. Dicho modelo fue seleccionado debido a la naturaleza de los datos que hemos podido recolectar de la API del Banco Mundial. En el análisis de los mismos detectamos una correlación lineal entre la variable independiente y la variable objetivo. Debido también a que los datos disponibles son del año 1962 al año 2021, tenemos poca cantidad de datos relacionada al tiempo de los indicadores, lo que no nos permitió optar  por un modelo mas flexible ante la naturaleza humana, como podría haber sido un modelo de Redes Neuronales.
## Principales tecnologías
Se decidió trabajar con Python de manera local para realizar el modelo, debido a falta de recursos un Google Cloud, lo que nos permitió el ahorro cluster y una optima realización del trabajo.
Las librerias utlizadas fueron:
1. Matplotlib
2. Sklearn
3. Pandas
4. Numpy