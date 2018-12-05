import requests
from urllib.parse import urlencode

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


def getDataFromRank(currentPage,platform):
    params = {
        'platform': platform,
        'sort': 'rank',
        'order': 'asc',
        'page': currentPage
    }

    url = 'https://api.stateofthedapps.com/dapps?' + urlencode(params)

    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def getDappDetail(dappName):
    url = 'https://api.stateofthedapps.com/dapps/'+dappName
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def getCategories():
    url = 'https://api.stateofthedapps.com/categories'
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def getTags():
    url = 'https://api.stateofthedapps.com/tags?type=dapps'
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None