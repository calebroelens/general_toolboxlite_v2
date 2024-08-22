import xmlrpc.client
import functools


class OdooClient:

    def __init__(self, host, port, database, user, password):
        self.__host = host
        self.__port = port
        self.__database = database
        self.__user = user
        self.__password = password

        # Setup calculated props
        self.__uid = None
        self.__common_proxy = None
        self.__common_proxy_info = None
        self.__object_proxy = None
        self.__model_names = []

    def start(self):
        """
        Start of the client
        :return:
        """
        self.__set_common()

    def get_proxy(self, proxy_type) -> str:
        """
        Get the proxy type
        :param proxy_type:
        :return:
        """
        return f"{self.__host}{':' + str(self.__port) if self.__port else ''}/xmlrpc/2/{proxy_type}"

    def login(self):
        """
        Attempt to authenticate the connection
        :return:
        """
        try:
            self.__uid = self.__common_proxy.authenticate(self.__database, self.__user, self.__password, {})
        except Exception as e:
            raise ConnectionError(f"Failed to authenticate: {e}")
        if not self.__uid:
            raise ConnectionError(f"Failed to authenticate: Invalid user or password.")
        # Attempt to create model execute object
        try:
            self.__object_proxy = xmlrpc.client.ServerProxy(self.get_proxy('object'))
        except Exception as e:
            raise ConnectionError(f"Failed to create model proxy: {e}")
        return self.__uid

    def __set_common(self):
        self.__common_proxy = xmlrpc.client.ServerProxy(self.get_proxy('common'))
        self.__common_proxy_info = self.__common_proxy.version()

    def execute_kw_models(self, model_name: str, method: str, *args):
        """
        Execute the kw_models function on a model with a method params and additional arguments.
        :param model_name:
        :param method:
        :param args:
        :return:
        """
        return self.__object_proxy.execute_kw(self.__database, self.__uid, self.__password, model_name, method, *args)
