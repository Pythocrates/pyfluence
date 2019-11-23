# -*- coding: utf-8 -*-

from .exceptions import UnknownHTTPRequestError


class RESTWrapper:
    def __init__(self, host, path, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__host = host
        self.__path = path
        self.__session = session

    def __getattr__(self, path):
        return self.__class__(
            host=self.__host,
            path=self.__path + [path],
            session=self.__session)

    def __getitem__(self, path):
        return getattr(self, str(path))

    def __call__(self, **kwargs):
        try:
            request_function = {
                'GET': self.__session.get,
                'POST': self.__session.post,
                'PUT': self.__session.put,
                'DELETE': self.__session.delete,
            }[self.__path[-1]]
        except KeyError:
            raise UnknownHTTPRequestError(self.__path[-1])
        else:
            response = request_function(
                http_request_uri='/'.join([self.__host] + self.__path[:-1]),
                **kwargs)
            try:
                assert(response.status_code // 100 == 2)
            except AssertionError:
                print(response.__dict__)
                raise

        return response

    def read_from_path(self, path):
        return self.__session.read(url=self.__host + path)

    def download(self, url, file_path):
        return self.__session.download(url, file_path)
