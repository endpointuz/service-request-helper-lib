import humps

from servic_request_helper.abstracts import AbstractResponseFormatter
from servic_request_helper.types import ResponseFile


class FullResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return response


class JsonResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return response.json()


class JsonDecamelizeResponseFormatter(JsonResponseFormatter):

    def format(self, response):
        return humps.decamelize(super().format(response))


class ContentResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return response.content


class FileResponseFormatter(AbstractResponseFormatter):

    def format(self, response):
        return ResponseFile(response.content, response.headers)
