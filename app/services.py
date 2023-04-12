from io import BytesIO
import json

import requests

from django.conf import settings
from django.core.files.storage import default_storage


absolute_path = 'app/static/{year}{race}.json'


def join_results(path_mapping):
    results = {}
    for year, races in path_mapping.items():
        results[year] = {}
        for race in races:
            file_path = f'{year}{race}.json'
            if default_storage.exists(file_path):
                with default_storage.open(file_path, 'r') as f:
                    d = json.load(f)
                    results[year][race] = d
    return(results)


def get_gpx_file(race: str) -> BytesIO:
    f = None
    print(race)
    if race == 'ultra':
        r = requests.get(settings.ULTRA_GPX_LINK)
        f = BytesIO(r.content)
    elif race == 'sky':
        r = requests.get(settings.SKY_GPX_LINK)
        f = BytesIO(r.content)

    return f
