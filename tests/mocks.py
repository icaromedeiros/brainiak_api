# -*- coding: utf-8 -*-
from urlparse import urlparse
from brainiak.utils.params import normalize_last_slash


class MockSimpleRequest(object):

    def __init__(self, status_code, json):
        self.status_code = status_code
        self._json = json

    def __call__(self, *args, **kw):
        return self

    def json(self):
        return self._json

    @property
    def text(self):
        return self._json


class MockRequest(object):

    def __init__(self,
                 uri="http://localhost:5100/ctx/klass/",
                 query_string="",
                 instance=""):
        self.query = query_string
        self.uri = uri
        if instance:
            self.uri = "%s%s" % (self.uri, instance)
        parsed_url = urlparse(self.uri)
        self.path = parsed_url.path
        self.protocol = parsed_url.scheme
        self.host = parsed_url.netloc
        self.base_url = "{0}://{1}{2}".format(self.protocol, self.host, normalize_last_slash(self.path))
        self.resource_url = self.base_url + "{resource_id}"
        self.headers = {'Host': self.host}
        if query_string:
            self.uri = "%s?%s" % (self.uri, query_string)

    def full_url(self):
        return self.uri


class MockHandler():

    def __init__(self, uri=None, **kw):
        self.kw = kw
        if uri is None:
            uri = 'http://mock.test.com/'

        _parsed_url = urlparse(uri)
        self._path = _parsed_url.path
        self._protocol = _parsed_url.scheme
        self._host = _parsed_url.netloc

    def get_argument(self, key):
        return self.kw.get(key)

    @property
    def request(self):
        class Dummy(object):
            @property
            def arguments(inner_self):
                return self.kw.keys()

            @property
            def protocol(inner_self):
                return self._protocol

            @property
            def host(inner_self):
                return self._host

            @property
            def path(inner_self):
                return self._path

        d = Dummy()
        return d
