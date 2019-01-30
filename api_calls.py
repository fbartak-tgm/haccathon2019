import requests as rq
from pprint import pprint

filme = rq.get("https://efs.film.at/api/v1/cfs/filmat/screenings/nested/movie/2019-01-30?city=Wien").json()["result"]


def get_film_by_genre(genre):
    results = []
    for film in filme:
        if "genres" in film["parent"]:
            if genre in film["parent"]["genres"]:
                results.append(film["parent"]["title"])
    return results
