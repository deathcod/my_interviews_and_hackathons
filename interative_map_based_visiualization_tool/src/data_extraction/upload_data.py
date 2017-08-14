import requests

from arrange_data import arrange_data


def upload(DEPLOY=False):
    ad = arrange_data(DEPLOY=DEPLOY)
    ad.start()

    url = 'https://interative-map-based-visiualiz.herokuapp.com/query' if DEPLOY else 'http://127.0.0.1:5000/query'
    print requests.post(url, json={'main_id': '1', 'id': '2', 'data': ad.COUNTRY}).text
    print requests.post(url, json={'main_id': '1', 'id': '1', 'data': ad.AFRICAN_CUP}).text
    print requests.post(url, json={'main_id': '1', 'id': '3', 'data': ad.STADIUM}).text
    print requests.post(url, json={'main_id': '1', 'id': '4', 'data': ad.PLAYER}).text
    print requests.post(url, json={'main_id': '1', 'id': '5', 'data': ad.RELATION_CUP_STADIUM}).text
    print requests.post(url, json={'main_id': '1', 'id': '6', 'data': ad.RELATION_CUP_COUNTRY_PLAYER}).text
    print requests.post(url, json={'main_id': '1', 'id': '7', 'data': ad.RELATION_CUP_COUNTRY}).text
    pass


if __name__ == '__main__':
    upload(DEPLOY=True)
    pass
