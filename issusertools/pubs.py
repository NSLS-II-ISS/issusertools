import requests
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
def create_journal_impact_factor(file = '/Users/elistavitski/Repos/issusertools/issusertools/JCR-Eli.xlsx'):
    journal_list = pd.read_excel(file)
    impact_factor_dict = {}
    for index, row in journal_list.iterrows():
        if not np.isnan(row['2021 JIF']) :
            impact_factor_dict[row['Journal name'].lower()] = int(row['2021 JIF'])
        else:
            impact_factor_dict[row['Journal name'].lower()] = 1
    return impact_factor_dict

impact_factor_dict = create_journal_impact_factor()

def open_publication_list(file = '/Users/elistavitski/Repos/issusertools/issusertools/publications.txt'):
    with open(file, 'r')as f:
        _p = f.read()
    _p = _p.split('\n')
    _pub_list = []
    for pub in _p:
        if pub:
            _pub_list.append(pub)
    return _pub_list

unformatted_pub_list = open_publication_list()

def parse_publication_list(unformatted_pub_list, impact_factor_dict):
    publications_dict ={}
    for index, pub in enumerate(unformatted_pub_list):
        _is_doi = pub.split('doi:')
        if len(_is_doi) > 1:
            doi = pub.split('[')[-1].split(']')[0].split('doi: ')[1]
            link = f'http://api.crossref.org/works/{doi}'
            _r = requests.get(link)
            if _r.status_code == 200:
                _p_dict = {}

                _p_dict['date'] = _r.json()['message']['published']['date-parts'][0]
                _journal = _r.json()['message']['container-title'][0].lower()
                if '&amp;' in _journal:
                    _journal = _journal.replace('&amp;', '&')
                _p_dict['journal'] = _journal
                try:
                    _p_dict['jif'] = impact_factor_dict[_journal]
                except:
                    _p_dict['jif'] = 1
                authors_list = []
                authors = _r.json()['message']['author']
                for author in authors:
                    _author = f"{author['family']}, {author['given']}"
                    authors_list.append(_author)
                _p_dict['authors'] = authors_list

                if 'HIGH IMPACT' in pub:
                    _p_dict['high_impact'] = True
                if 'CITED' in pub:
                    _p_dict['cited'] = int(pub.split('CITED ')[1].split(' TIME')[0])
                publications_dict[doi] =_p_dict
    return publications_dict

formatted_publication_dict= parse_publication_list(unformatted_pub_list, impact_factor_dict)

def save_publication_list(formatted_publication_dict, file = '/Users/elistavitski/Repos/issusertools/issusertools/formatted_publications.txt'):
    with open(file, 'w') as f:
        json.dump(formatted_publication_dict, f)

save_publication_list(formatted_publication_dict)

def create_user_publications_list(publications_dict):
    unique_authors= {}
    for key in publications_dict.keys():
        for _author in publications_dict[key]['authors']:
            if _author in unique_authors.keys():
                unique_authors[_author].append(key)
            else:
                unique_authors[_author]= [key]

    return unique_authors













