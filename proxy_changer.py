import db_request
import proxy
import requests
import json


def get_proxy():
    def get_cache_proxy():
        sql_request = db_request.make_request("SELECT * FROM cache_proxy LIMIT 1;")
        ip, port = db_request.execute(sql_request)[0]
        cache_proxy = proxy.make_proxy(ip, port)

        sql_request = db_request.make_request("DELETE FROM cache_proxy WHERE ip=?;",
                                              data=(proxy.ip(cache_proxy), ))
        db_request.execute(sql_request)
        return cache_proxy

    url_api = 'http://pubproxy.com/api/proxy?type=https'
    # Если бот попал в бан, то переходим на кэшированные прокси
    try:
        response = requests.get(url_api).json()
    except json.decoder.JSONDecodeError:
        cache_proxy = get_cache_proxy()
        return cache_proxy

    current_proxy = proxy.make_proxy(
        response['data'][0]['ip'], response['data'][0]['port'])
    return current_proxy


def write_proxy(current_proxy):
    sql_requests = ["UPDATE proxy SET ip=?, port=? WHERE state='current_proxy';",
                    "INSERT INTO cache_proxy VALUES (?, ?);"]
    sql_request_data = (proxy.ip(current_proxy), proxy.port(current_proxy))

    for sql_request_body in sql_requests:
        request_to_db = db_request.make_request(
            sql_request_body, data=sql_request_data)
        db_request.execute(request_to_db)


def read_proxy():
    request = db_request.make_request("SELECT ip, port FROM proxy;")
    ip, port = db_request.execute(request)[0]

    current_proxy = proxy.make_proxy(ip, port)
    return current_proxy


def set_proxy(current_proxy):
    return {'https': f'https://{proxy.ip(current_proxy)}:{proxy.port(current_proxy)}'}


def proxy_info(current_proxy):
    url_api = f'http://free.ipwhois.io/json/{proxy.ip(current_proxy)}?lang=ru'
    response = requests.get(url_api).json()

    info = {'ip': response['ip'],
            'country': response['country'], 'city': response['city']}
    return info
