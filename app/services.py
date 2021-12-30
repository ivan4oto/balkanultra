import json

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
