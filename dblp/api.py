import requests
import pandas as pd

from urllib.parse import urlencode
from importlib.resources import open_binary

BASE_URL = 'https://dblp.org/search/publ/api'


def add_ccf_class(results: list[dict]) -> list[dict]:
    def get_ccf_class(venue: str | None, catalog: pd.DataFrame) -> str | None:
        if venue is None:
            return
        if len(series := catalog.loc[catalog.get('abbr').str.lower() == venue.lower(), 'class']) > 0:
            return series.item()
        elif len(series := catalog.loc[catalog.get('url').str.contains(f'/{venue.lower()}/'), 'class']) > 0:
            return series.item()

    catalog = pd.read_csv(open_binary('dblp.data', 'ccf_catalog.csv'))
    for result in results:
        result['ccf_class'] = get_ccf_class(result.get('venue'), catalog=catalog)
    return results


def search(queries: list[str]) -> list[dict]:
    results = []
    for query in queries:
        entry = {
            'query': query,
            'title': None,
            'year': None,
            'venue': None,
            'doi': None,
            'url': None,
            'bibtex': None,
        }
        options = {
            'q': query,
            'format': 'json',
            'h': 1
        }
        r = requests.get(f'{BASE_URL}?{urlencode(options)}').json()
        hit = r.get('result').get('hits').get('hit')
        if hit is not None:
            info = hit[0].get('info')
            entry['title'] = info.get('title')
            entry['year'] = info.get('year')
            entry['venue'] = info.get('venue')
            entry['doi'] = info.get('doi')
            entry['url'] = info.get('ee')
            entry['bibtex'] = f'{info.get("url")}?view=bibtex'
        results.append(entry)
    return results

def query_for_top_venues(query: str, year_list: list[str] = ['2023'], ccf_class_list: list[str] = ['A']) -> list[dict]:
    results = [] 
    assert year_list is not None, 'year is required to be a list, not None'
    assert ccf_class_list is not None, 'ccf_class is required to be a list, not None'

    # open ccf catalog file
    catalog = pd.read_csv(open_binary('dblp.data', 'ccf_catalog.csv'))

    # find the venues that match the ccf_class
    target_venues = catalog.loc[catalog['class'].isin(ccf_class_list), 'abbr']
    target_venues = set(target_venues)

    # send a pilot query to get the total number of results
    options = {
        'q': query,
        'format': 'json',
        'h': 1
    }
    endpoint = f'{BASE_URL}?{urlencode(options)}'
    r = requests.get(endpoint).json()
    num_records = int(r.get('result').get('hits').get('@total'))
    
    # get search results for the query
    last_record_idx = 0
    while last_record_idx < num_records:
        options = {
            'q': query,
            'format': 'json',
            'h': 1000,
            'f': last_record_idx
        }
        r = requests.get(f'{BASE_URL}?{urlencode(options)}').json()
        records = r.get('result').get('hits').get('hit')
        if records is None:
            break
        for record in records:
            info = record.get('info')
            venue = info.get('venue')
            year = info.get('year')
            if type(venue) == list:
                if not any([v in target_venues for v in venue]):
                    continue
            else:
                if venue not in target_venues:
                    continue
            if year not in year_list:
                continue
            author_list_raw = info.get('authors').get('author')
            author_list = []
            for author_raw in author_list_raw:
                author = author_raw.get('text')
                author_list.append(author)
            entry = {
                'title': info.get('title'),
                'authors': author_list,
                'year': info.get('year'),
                'venue': info.get('venue'),
                'doi': info.get('doi'),
                'url': info.get('ee'),
                'bibtex': f'{info.get("url")}?view=bibtex'
            }
            results.append(entry)
        last_record_idx += 1000
    return results


