from fastapi import FastAPI, APIRouter, Path
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
from jinja2 import Template
import os

from web_server.funcionesAPI import (
    PlayTimeGenre,
    UserForGenre,
    UsersRecommend,
    UsersWorstDeveloper,
    get_sentiment_by_developer,
    get_game_recommender,
    get_user_recommendation
)


# Models
class Message(BaseModel):
    message: str


class SentimentCount(BaseModel):
    Negative: int
    Neutral: int
    Positive: int


class SentimentAnalysis(BaseModel):
    Dict[str, SentimentCount]


# Endpoints Router
router = APIRouter()


@router.get(
    "/PlayTimeGenre/{genre}",
    responses={
        404: {"model": Message, "description": "El genero no se encontró"},
        200: {
            "description": "Devuelve año con mas horas jugadas para dicho género.",
            "content": {
                "application/json": {
                    "example": {
                        "El año con más horas jugadas para Género X": 2013
                    }
                }
            },
        },
    },
)
async def play_time_genre(
        genre: str = Path(..., description="Ingrese un genero", example="Simulation")
):
    """
    Returns the year with the most hours played for a given genre.
    """
    response = await PlayTimeGenre(genre)
    if response is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"Genero {genre} no encontrado, por favor, intenta de nuevo."},
        )

    return response


@router.get(
    "/UserForGenre/{genre}",
    responses={
        404: {"model": Message, "description": "El genero no se encontró"},
        200: {
            "description": "Retorna el Usuario con mas horas jugadas por genero y lista de horas jugadas por año",
            "content": {
                "application/json": {
                    "example": {
                        "Usuario con más horas jugadas para Género X": "us213ndjss09sdf",
                        "Playtime": [
                            {"Year": 2013, "Hours": 203},
                            {"Year": 2012, "Hours": 100},
                            {"Year": 2011, "Hours": 23},
                        ],
                    }
                }
            },
        },
    },
)
async def user_for_genre(
        genre: str = Path(description="Ingrese un genero", example="RPG")
):
    """
    Returns the user who has accumulated the most played hours for the given genre and a list of accumulated playtime by release year.
    """
    response = await UserForGenre(genre)

    if response is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"Genero {genre} no encontrado, por favor, intenta de nuevo."},
        )

    return response


@router.get(
    "/UsersRecommend/{year}",
    responses={
        404: {"model": Message, "description": "El año no se encontró"},
        200: {
            "description": "Retorna el top 3 de juegos mas recomendados por usuarios para el año dado.",
            "content": {
                "application/json": {
                    "example": [
                        {"Rank 1": "X"},
                        {"Rank 2": "Y"},
                        {"Rank 3": "Z"},
                    ]
                }
            },
        },
    },
)
async def users_recommend(
        year: int = Path(description="Ingrese el año", example=2013)
):
    """
    Returns the top 3 games MOST recommended by users for the given year.
    """
    response = await UsersRecommend(year)
    if response is None:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"El año {year} no tiene reviews para calcular el ranking de los juegos con más recomendaciones. Por favor, intenta de nuevo con otro año.",
            },
        )
    return response


@router.get(
    "/UsersWorstDeveloper/{year}",
    responses={
        404: {"model": Message, "description": "El año no se encontró"},
        200: {
            "description": "Retorna el top 3 de juegos MENOS recomendados por usuarios para el año dado",
            "content": {
                "application/json": {
                    "example": [
                        {"Rank 1": "X"},
                        {"Rank 2": "Y"},
                        {"Rank 3": "Z"},
                    ]
                }
            },
        },
    },
)
async def users_worst_developer(
        year: int = Path(description="Ingrese el año", example=2011)
):
    """
    Returns the top 3 developers with the LEAST recommended games by users for the given year.
    """
    response = await UsersWorstDeveloper(year)
    if response is None:
        return JSONResponse(
            status_code=404,
            content={
                "mensaje": f"El año {year} no tiene reviews para calcular el ranking de los desarrolladores con menos recomendaciones. Por favor, intenta de nuevo con otro año.",
            },
        )
    return response


@router.get(
    "/SentimentAnalysis/{developer}",
    responses={
        404: {"model": Message, "description": "El desarrollador no se encontró"},
        200: {
            "description": "Analisis de sentimiento para un desarrollador dado. Retornando una lista con la cantidad de reseñas de usuarios que se encuentren categorizados, en función del sentimiento positivo, negativo o neutral.",
            "content": {
                "application/json": {
                    "example": {
                        "Valve": [
                            {"Negative": 1352},
                            {"Neutral": 2202},
                            {"Positive": 4840},
                        ]
                    }
                }
            },
        },
    },
)
async def sentiment_analysis(
        developer: str = Path(description="Ingrese el nombre del desarrollador", example="Ubisoft")
):
    """
    Returns a developer with the total number of users reviews records categorized with a sentiment analysis.
    """

    response = await get_sentiment_by_developer(developer)
    if response is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"Desarrolador {developer} no encontrado. Por favor, intenta de nuevo."},
        )
    return response


# Recommender Router
recommender = APIRouter()


@recommender.get(
    "/GameRecommender/{game}",
    responses={
        404: {"model": Message, "description": "El juego no se encontró"},
        200: {
            "description": "Juegos recomendados por juego",
            "content": {
                "application/json": {
                    "example": {
                        1: "Hotline Miami 2: Wrong Number",
                        2: "Dino D-Day",
                        3: "BattleBlock Theater®",
                        4: "The Forest",
                        5: "Yet Another Zombie Defense",
                    }
                }
            },
        },
    },
)
async def game_recommender(
        game: str = Path(description="Entre el nombre del juego", example="APB Reloaded")
):
    """
    Returns 5 recommended games similar to a given game.
    """
    response = await get_game_recommender(game)
    if response is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"El juego {game} no se encuentra. Por favor, intenta de nuevo."},
        )
    return response


@recommender.get(
    "/UserRecommender/{user_id}",
    responses={
        404: {"model": Message, "description": "Usuario no encontrado"},
        200: {
            "description": "Juegos recomendados por usuario",
            "content": {
                "application/json": {
                    "example": {
                        1: "8BitMMO",
                        2: "A Story About My Uncle",
                        3: "Aliens vs. Predator™",
                        4: "ARMA: Cold War Assault",
                        5: "APB Reloaded",
                    }
                }
            },
        },
    },
)
async def user_recommender(
        user_id: str = Path(description="Entre el ID del usuario", example="yoshipowerz")
):
    """
    Returns the 5 games with the highest predicted rating for the user.
    """
    response = await get_user_recommendation(user_id)
    if response is None:
        return JSONResponse(
            status_code=404,
            content={"message": f"El usuario {user_id} no se encuentra. Por favor, intenta de nuevo."},
        )
    return response


# Main FastAPI App
app = FastAPI(
    title="RecSys API para los juegos Steam Games",
    version="0.2.0",
    description="Esta API te permite acceder a datos de Steam, una plataforma de videojuegos líder, y obtener recomendaciones de juegos personalizadas basadas en un modelo de aprendizaje automático. Con esta API, puedes consultar información sobre géneros de juegos, usuarios, desarrolladores y reseñas, además de recibir sugerencias de juegos similares o adecuados para ti u otros usuarios.",
)


@app.get("/", tags=["Home"], status_code=200, response_class=HTMLResponse)
def index():
    # Carga la plantilla HTML con la ruta absoluta del archivo index.html
    template = Template(open(os.path.dirname(__file__) + "/index.html").read())

    # Renderiza la plantilla HTML
    return template.render()


app.include_router(router, tags=["Endpoints"])
app.include_router(recommender, tags=["Recomendador"])
