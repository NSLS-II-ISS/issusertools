import pandas as pd
import requests
import numpy as np




def get_user_visits(file = '/home/xf08id/Repos/issusertools/issusertools/user_visits.xlsx'):
    _visits =pd.read_excel(file)
    return _visits

visits = get_user_visits()


def extract_users_by_proposal(visits):
    user_visits_list = []
    headers = {'accept': 'application/json', }
    for row in visits.iterrows():
        row = row[1]
        try:
            _proposal = str(int(row['Proposal ID']))
        except:
            print('>>>>>>>>>>>>>>>>>')
            break
        proposal_info = requests.get(f'https://api-staging.nsls2.bnl.gov/proposal/{_proposal}', headers=headers).json()
        if 'error_message' in proposal_info.keys():
            print(f'Proposal  {_proposal} not found')
        else:
            users = proposal_info['users']
            for user in users:
                _user_dict = {}
                _user = user['first_name'] + ' ' + user['last_name']
                _user_dict[_user] = {'proposal': row['Proposal ID'],
                                    'date': str(row['Stop Time']),
                                    'shifts': row['Shifts Used'],
                                    }
                user_visits_list.append(_user_dict)
    return user_visits_list

user_visits_list = extract_users_by_proposal(visits)


def extract_unique_user_visits(user_visits_list):
    unique_user_visits = {}
    user_list = []
    for _visit in user_visits_list:
        for _key in _visit.keys():
            user_list.append(_key)

    unique_user_list = list(np.unique(user_list))

    no_unique_users = len(unique_user_list)
    print(no_unique_users)

    for index,user in enumerate(unique_user_list):
        print(f'{index/no_unique_users*100}% {user}')
        for visit in user_visits_list:
            if user in visit.keys():
                if user in unique_user_visits:
                    unique_user_visits[user].append(visit[user])
                else:
                    unique_user_visits[user] = [visit[user]]


    for _key in  unique_user_visits.keys():
        _visit_list = unique_user_visits[_key]
        unique_user_visits[_key] = pd.DataFrame(_visit_list).drop_duplicates().to_dict('r')


    return unique_user_visits


unique_user_visits = extract_unique_user_visits(user_visits_list)



def load_current_proposal(file = '/home/xf08id/Repos/issusertools/proposals 2023-3.xlsx'):
    current_proposal_dict = {}
    current_proposal_list = pd.read_excel(file)

    for row in current_proposal_list.iterrows():
        try:
            current_proposal_dict[row[1]['Proposal_ID']] = row[1]['Experimenter_Names'].split(',')
        except:
            pass
    return current_proposal_dict


current_proposal_dict = load_current_proposal()






