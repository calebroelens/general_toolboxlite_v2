import xmlrpc.client
import socket


class DatabaseInfo:

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def __proxy(self, proxy_type: str):
        if self.__port:
            return f"{self.__host}:{self.__port}/xmlrpc/2/{proxy_type}"
        else:
            return f"{self.__host}/xmlrpc/2/{proxy_type}"

    def list_databases(self, throw_exception=False):
        if not throw_exception:
            try:
                db = xmlrpc.client.ServerProxy(self.__proxy('db'))
                return db.list()
            except socket.gaierror as e:
                print(e)
                return []
            except Exception as e:
                print(e)
                return []
        else:
            return xmlrpc.client.ServerProxy(self.__proxy('db')).list()

    def get_info(self):
        try:
            db = xmlrpc.client.ServerProxy(self.__proxy('common'))
            return db.version()
        except socket.gaierror as e:
            return {}
        except Exception as e:
            return {}

    def is_available(self):
        try:
            xmlrpc.client.ServerProxy(self.__proxy('common'))
            return True
        except Exception as e:
            return False
