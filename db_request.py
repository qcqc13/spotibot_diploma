import sqlite3


def make_request(sql_request, data=None):
    def cons_request(data_obtain):
        if data_obtain == 'request':
            return sql_request
        elif data_obtain == 'request_data':
            return data
        else:
            return None
    return cons_request


def request_body(request):
    return request('request')


def data(request):
    return request('request_data')


def execute(request):
    connection = sqlite3.connect('spotify.db')
    cursor = connection.cursor()

    data_request = data(request)
    if data_request is None:
        response = cursor.execute(request_body(request)).fetchall()
    else:
        response = cursor.execute(request_body(request), data_request).fetchall()
    connection.commit()
    connection.close()

    if not response:
        return None
    return response
