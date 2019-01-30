import requests
from pprint import pprint




def alle_genres():
    daten = requests.get("https://efs.film.at/api/v1/cfs/filmat/screenings/nested/movie/2019-01-30?city=Wien")
    filme = daten.json()["result"]
    liste = []

    for elm in filme:
        if "genres" in elm["parent"]:
            for etwas in elm["parent"]["genres"]:
                liste.append(etwas)

    return set(liste)

print(alle_genres())

"""
def get_film_by_genre(genre):
    results = []
    for film in filme:
        if "genres" in film["parent"]:
            if genre in film["parent"]["genres"]:
                results.append(film["parent"]["title"])
    return results

def get_film_at_time(time):
    for film in filme:
        pprint(film)

get_film_at_time(None)
"""
