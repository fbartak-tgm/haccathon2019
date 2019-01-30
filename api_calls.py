import requests as rq
from pprint import pprint

r = rq.get("https://efs.film.at/api/v1/cfs/filmat/screenings/nested/movie/2019-01-31?city=Wien")
pprint(r)