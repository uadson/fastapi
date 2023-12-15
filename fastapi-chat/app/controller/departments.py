import requests


def departments_list(url):
    """
        :url: url da api que lista todas as secretarias
    """
    
    data = requests.get(url)
    return data.json()
