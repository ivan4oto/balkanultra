from ast import Bytes
from io import BytesIO
import json

import requests

from .mail_letters import Letter
from mailjet_rest import Client
from django.conf import settings

absolute_path = 'app/static/{year}{race}.json'


def join_results(path_mapping):
    results = {}

    for year, races in path_mapping.items():
        results[year] = {}
        for race in races:
            with open(absolute_path.format(year=str(year), race=race), 'r') as f:
                d = json.load(f)
                results[year][race] = d
    return(results)

class Mailjet_Letter_Service():
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')

    def send_letter(self, r_mail, r_name, r_family, r_link_a, r_link_b, r_distance):
        if r_distance == 'ultra':
            text_part = Letter.ULTRA_LETTER.format(
                f=r_name,
                l=r_family,
                m=r_mail,
                fl=r_link_a,
                sl=r_link_b
            )
        else:
            text_part = Letter.SKY_LETTER.format(
                f=r_name,
                l=r_family,
                m=r_mail
            )

        data = {
            'Messages': [
                {
                "From": {
                    "Email": "balkanultra@abv.bg",
                    "Name": "Ivan & Rosen"
                },
                "To": [
                    {
                    "Email": r_mail,
                    "Name": r_name
                    }
                ],
                "Subject": "Balkan Ultra success",
                "TextPart": text_part,
                "HTMLPart": "",
                "CustomID": r_mail
                }
            ]
        }

        result = self.mailjet.send.create(data=data)
        return result


def get_gpx_file(race: str) -> BytesIO:
    f = None
    print(race)
    if race == 'ultra':
        r = requests.get(settings.ULTRA_GPX_LINK)
        f = BytesIO(r.content)
        print(f)
    elif race == 'sky':
        r = requests.get(settings.SKY_GPX_LINK)
        f = BytesIO(r.content)

    return f




