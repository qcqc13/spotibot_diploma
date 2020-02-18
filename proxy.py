def make_proxy(ip, port):
    def cons_proxy(data_obtain):
        if data_obtain == 'ip':
            return ip
        elif data_obtain == 'port':
            return port
        else:
            return None
    return cons_proxy


def ip(proxy):
    return proxy('ip')


def port(proxy):
    return proxy('port')
