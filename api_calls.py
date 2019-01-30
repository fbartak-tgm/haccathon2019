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

def get_film_at_time(time):
    for film in filme:
        for kino in film:
            if type(film[kino]) is list:
                for k in film[kino]:
                    for screening in k["screenings"]:
                        print(screening,"\n\n\n")

            else:
                print(type(film[kino]))

print(get_film_at_time(None))