import requests as rq
import datetime
today = datetime.datetime.now()
import random
import json

filme = json.loads(json.dumps(rq.get("https://efs.film.at/api/v1/cfs/filmat/screenings/nested/movie/" + today.strftime("%Y-%m-%d") + "?city=Wien").json()["result"]).lower().replace("&","und"))
genres = ['Fantasy', 'Romanze', 'Kurzfilm', 'Science Fiction', 'Biografie', 'Erotik', 'Sport',
     'Krimi', 'Tragikomödie', 'Animation', 'Geschichtsfilm', 'Drama', 'Kinderfilm', 'Western', 'Kultfilme', 'Action',
     'Dokumentation', 'Literaturverfilmung', 'Abenteuer', 'Horror', 'Komödie', 'Thriller']

time = datetime.datetime.now().replace(year=today.year, day=today.day, month=today.month)

def get_film_by_genre(genre):
    results = []
    for film in filme:
        if "genres" in film["parent"]:
            if genre in film["parent"]["genres"]:
                results.append(film["parent"]["title"])
    return results

def get_film_at_time(time=None):
    filmlist = {}
    if not time == None:
        time = datetime.datetime.strptime(time, "%H:%M").replace(year=today.year, day=today.day, month=today.month)
    for film in filme:
        filmlistspielzeiten = []

        if type(film["nestedresults"]) is list:
            for k in film["nestedresults"]:
                mvrating = None
                #mvrating = check_rating(k["parent"]["title"])
                screenlist = []
                for screening in k["screenings"]:
                        if time == None or time.timestamp() - parsetime(screening["time"]).timestamp() < 0:
                            if mvrating == None:
                                screenlist.append(parsetime(screening["time"]).strftime("%H Uhr %M").replace(" Uhr 00"," Uhr "))
                            break
                if len(screenlist) > 0:
                    filmlistspielzeiten.append((k["parent"]["title"],screenlist))
        if len(filmlistspielzeiten) > 0:
            filmlist[film["parent"]["title"]] = filmlistspielzeiten
        else:
            pass
    return filmlist

def get_one_film(filmliste):
    for x in filmliste:
        for kino in filmliste[x]:
            return x,kino[0],kino[1][0],check_rating(x)

def parsetime(apitime):
    return datetime.datetime.strptime(apitime,"%Y-%m-%dT%H:%M:%S+01:00") - datetime.timedelta(hours=1)

def random_movie(filmliste):
    x = random.choice(list(filmliste.keys()))
    kino = random.choice(list(filmliste[x]))
    return x,kino[0],kino[1][0],check_rating(x)

def search_movie_by_genre(query,time=None):
    movies_in_genre = get_film_by_genre(query)
    filme = get_film_at_time(time=time)
    filmelemente = []
    for x in movies_in_genre:
        if x in filme:
            filmelemente.append((x,filme[x][0][0],filme[x][0][1][0],check_rating(x)))
    return filmelemente

def check_rating(title):
    mv = rq.get("https://www.omdbapi.com/?apikey=dc083806&t=" + title).json()
    if "Error" in mv:
        return None
    return float(mv["Ratings"][0]["Value"].split("/")[0])

def random_genres():
    g = [random.choice(genres),random.choice(genres),random.choice(genres)]
    return g

def weather_clear():
    w = rq.get("https://api.openweathermap.org/data/2.5/weather?q=vienna&APPID=fd9fa1baba434b74b359c8112aef30bf").json()
    return w["weather"][0]["main"] == "Clear"


# print(get_one_film(get_film_at_time("09:29")))
# print(random_movie(get_film_at_time("09:29")))
# print(search_movie_by_genre("horror","12:00"))
# print(random_genres())
# print(weather_clear())