import humps

from servic_request_helper.abstracts import AbstractResponseFormatter


class FullResponseFormatter(AbstractResponseFormatter):

    def format(self, request):
        return request


class JsonResponseFormatter(AbstractResponseFormatter):

    def format(self, request):
        return request.json()


class JsonDecamelizeResponseFormatter(JsonResponseFormatter):

    def format(self, request):
        return humps.decamelize(super().format(request))


class FileResponseFormatter(AbstractResponseFormatter):

    def format(self, request):
        return request.content

