import pandas as pd
import numpy as np
import os


def carga_datos():
    data_dir = os.path.join(os.path.dirname(__file__),
                            '..', 'dataset')

    df_endpoints1_2 = pd.read_parquet(
        os.path.join(data_dir, 'df_endpoints1_2.parquet'))
    df_endpoints3_4_5 = pd.read_parquet(
        os.path.join(data_dir, 'df_endpoints3_4_5.parquet'))
    df_similitud_items = pd.read_parquet(
        os.path.join(data_dir, 'df_similitud_items.parquet'))
    df_similitud_usuarios = pd.read_parquet(
        os.path.join(data_dir, 'df_similitud_usuarios.parquet'))
    df_matrix = pd.read_parquet(
        os.path.join(data_dir, 'matrix.parquet'))

    return df_endpoints1_2, df_endpoints3_4_5, df_similitud_items, df_matrix, df_similitud_usuarios


df_pseudo_db1, df_pseudo_db2, df_item_sim, df_matrix, df_similitud_usuarios = carga_datos()


async def PlayTimeGenre(genre: str):

    if genre.upper() == "RPG":
        genre = genre.upper()
    else:
        genre = genre.title()

    if genre not in df_pseudo_db1.columns:
        return None

    df_genre = df_pseudo_db1[genre].reset_index()

    playtime_by_year = df_genre.groupby('release_year')[genre].sum()

    max_playtime_year = (playtime_by_year.idxmax())
    response = {
        f"Year with the most hours played for Genre {genre}": int(max_playtime_year)}

    return response


async def UserForGenre(genre: str):
    if genre.upper() == "RPG":
        genre = genre.upper()
    else:
        genre = genre.title()

    if genre not in df_pseudo_db1.columns:
        return None

    df_genre = df_pseudo_db1[genre].reset_index()
    user_max_hours = df_genre.groupby('user_id')[genre].sum().idxmax()
    playtime_by_year = df_genre[df_genre['user_id'] == user_max_hours].groupby(
        'release_year')[genre].sum().reset_index()
    playtime_by_year.columns = ['Year', 'Hours']
    playtime_by_year = playtime_by_year[playtime_by_year['Hours'] > 0]
    playtime_by_year['Hours'] = playtime_by_year['Hours'].round().astype(int)

    response = {
        f"User with most hours played for Genre {genre} ": user_max_hours,
        "Playtime": playtime_by_year.to_dict('records')
    }

    return response


async def UsersRecommend(year: int):

    if ~df_pseudo_db2['posted_year'].isin([year]).any():
        return None

    df_year = df_pseudo_db2[(df_pseudo_db2['posted_year'] == year) & (
        df_pseudo_db2['recommend'] == True) & (df_pseudo_db2['sentiment_analysis'] > 0)]

    recommendations = df_year.groupby('item_name').size()

    top_games = recommendations.sort_values(ascending=False).head(3)

    response = [{"Rank {}".format(i+1): game}
                for i, game in enumerate(top_games.index)]

    return response


async def UsersWorstDeveloper(year: int):

    if ~df_pseudo_db2['posted_year'].isin([year]).any():
        return None

    df_year = df_pseudo_db2[(df_pseudo_db2['posted_year'] == year) & (
        df_pseudo_db2['recommend'] == False) & (df_pseudo_db2['sentiment_analysis'] == 0)]

    if df_year.empty:
        return {f"No non-recommended games were found for the year {year}"}

    not_recommendations = df_year.groupby('developer').size()

    top_games = not_recommendations.sort_values(ascending=False).head(3)

    response = [{"Rank {}".format(i+1): game}
                for i, game in enumerate(top_games.index)]

    return response


async def get_sentiment_by_developer(developer: str):

    developer_lower = developer.lower()

    df_dev = df_pseudo_db2[df_pseudo_db2["developer"].str.lower()
                           == developer_lower]

    if df_dev.empty:

        return None

    sentiment_counts = df_dev['sentiment_analysis'].value_counts()
    negative_reviews = sentiment_counts.get(0, 0)
    neutral_reviews = sentiment_counts.get(1, 0)
    positive_reviews = sentiment_counts.get(2, 0)

    response = {
        developer_lower.capitalize(): [
            {"Negative": int(negative_reviews)},
            {"Neutral": int(neutral_reviews)},
            {"Positive": int(positive_reviews)}
        ]
    }

    return response


async def get_game_recommender(item_name: str):

    if item_name not in df_item_sim.index:
        return None

    row = df_item_sim.loc[item_name]

    row_sorted = row.sort_values(ascending=False)

    similar_games = row_sorted.index[1:6]

    recommendations = {}

    for i, juego in enumerate(similar_games, start=1):
        recommendations[i] = juego

    return recommendations


async def get_user_recommendation(user_id: str):
    np.seterr(divide='ignore', invalid='ignore')

    if user_id in df_matrix.index:

        fila_usuario = df_matrix.loc[user_id]

        juegos_no_jugados = []

        for juego, rating in fila_usuario.items():

            if rating == 0:

                juegos_no_jugados.append(juego)

        predicciones = []

        for juego in juegos_no_jugados:

            columna_juego = df_item_sim.loc[juego]

            producto = np.dot(fila_usuario, columna_juego)

            suma_sim = np.sum(columna_juego[fila_usuario != 0])

            prediccion = producto / suma_sim

            predicciones.append((juego, prediccion))

        predicciones_ordenadas = sorted(
            predicciones, key=lambda x: x[1], reverse=True)
        diccionario = {}

        for i, tupla in enumerate(predicciones_ordenadas[:5], start=1):

            diccionario[i] = (tupla[0])

        return diccionario

    else:

        return None


