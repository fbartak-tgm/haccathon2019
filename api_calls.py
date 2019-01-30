import requests as rq
from pprint import pprint
import datetime
print()
today = datetime.datetime.now()

filme = rq.get("https://efs.film.at/api/v1/cfs/filmat/screenings/nested/movie/" + today.strftime("%Y-%m-%d") + "?city=Wien").json()["result"]


def get_film_by_genre(genre):
    results = []
    for film in filme:
        if "genres" in film["parent"]:
            if genre in film["parent"]["genres"]:
                results.append(film["parent"]["title"])
    return results

def get_film_at_time(time):
    filmlist = {}
    time = datetime.datetime.strptime(time, "%H:%M").replace(year=today.year, day=today.day, month=today.month)
    for film in filme:
        print(film["parent"]["title"])
        filmlistspielzeiten = {}
        if type(film["nestedResults"]) is list:
            for k in film["nestedResults"]:
                screenlist = []
                for screening in k["screenings"]:
                    if time.timestamp() - parsetime(screening["time"]).timestamp() < 0:
                        screenlist.append(parsetime(screening["time"]))
                        break
                if len(screenlist) > 0:
                    filmlistspielzeiten[k["parent"]["title"]] = screenlist

            print("\n\n")
        if len(filmlistspielzeiten.keys()) > 0:
            filmlist[film["parent"]["title"]] = filmlistspielzeiten
        else:
            pass
    return filmlist
def get_one_film(filmliste):
    for x in filmliste:
        for kino in filmliste[x]:
            print(x,kino)
            return x,kino,filmliste[x][kino]
def parsetime(apitime):
    return datetime.datetime.strptime(apitime,"%Y-%m-%dT%H:%M:%S+01:00") - datetime.timedelta(hours=1)

#time = datetime.datetime.strptime("15:30", "%H:%M").replace(year=today.year, day=today.day, month=today.month)
print(get_one_film(get_film_at_time("09:29")))