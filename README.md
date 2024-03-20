# Analisis de datos de la plataforma STEAM

Este es mi proyecto de ciencia de datos para la etapa de labs del bootcamp de soy henry donde buscaremos implementar las habilidades obtenidas durante la etapa de aprendizaje.
## Descripción

Tomando el rol de cientifico de datos de la plataforma STEAM en este proyecto que tiene como objetivo crear un sistema de recomendacion de los juegos basado en los datos suministrados por la plataforma. Se llevaran acabo 3 diferentes procesos, desde la extraccion y tratamiento de los datos pasando por un analisis de los mismos hasta la implementacion del sistema de recomendacion.

## Herramientas usadas
- Pycharm como editor de codigo
- Python como lenguaje de programacion
- GitHub como repositorio del proyecto
- FastAPI como framework
- Docker para empaquetar la aplicacion para su respectivo despligue
- Render para el despliegue publica del API

## Etapa de ingenieria de datos
Durante la fase de ingeniería de datos, se llevó a cabo un procedimiento de ETL (extracción, transformación y carga), en el cual se manejaron tres archivos JSON. Estos archivos contenían datos sobre videojuegos, jugadores y sus respectivas críticas.
- #### Link: https://github.com/rrobles9112/Steam-MLOPS/tree/master/Notebooks/ETL_games.ipynb

- #### Link: https://github.com/rrobles9112/Steam-MLOPS/tree/master/Notebooks/ETL_items.ipynb

- #### Link: https://github.com/rrobles9112/Steam-MLOPS/tree/master/Notebooks/ETL_reviews.ipynb



### Fuente de los datos 
https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj

## Etapa de analisis exploratorio de los datos
En esta etapa se realizo el EDA, analisis exploratorio de datos donde empezamos con una conversion de los datos verificanddo datos nulos, duplicados, outliers y el formato de los datos para posteriormente realizar el analisis de estos mediante garficos.
#### Link: https://github.com/rrobles9112/Steam-MLOPS/tree/master/Notebooks/EDA.ipynb

## Sistema de recomendacion
Una vez completadas las  etapas anteriores los datos se encuentran preparados para realazar las respectivas funciones y el sistema de recomendacion los cuales podran ser consultados mediante el framework FastAPI 
#### Linkl FastAPI : https://my-jupyter-app-latest.onrender.com/docs

    def PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.


    def UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.


    def UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)


    def UsersWorstDeveloper( año : int ): Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)


    def sentiment_analysis( empresa desarrolladora : str ): Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.






## Video
En el siguiente enlace podras encontrar un video con un pequeño resumen acerca del proyecto
#### Link: https://www.youtube.com/channel/UCrR9T1nEFfQpWviNudpueBw

## Requisitos

Asegúrate de tener instaladas las siguientes bibliotecas antes de ejecutar el código:

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

Puedes instalarlos usando el siguiente comando:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Para ejecutar este proyecto en cualquier sistema operativo mediante docker se debe de seguir los siguientes pasos:


```bash
docker pull rrobles9112/my-jupyter-app:latest
```

#### Para el depligue en render escogi la opcion de conectar con repositorio docker
