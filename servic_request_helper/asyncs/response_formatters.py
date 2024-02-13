import humps

from servic_request_helper.abstracts import AbstractResponseFormatter


class FullResponseFormatter(AbstractResponseFormatter):

    async def format(self, request):
        return request


class JsonResponseFormatter(AbstractResponseFormatter):

    async def format(self, request):
        return await request.json()


class JsonDecamelizeResponseFormatter(JsonResponseFormatter):

    async def format(self, request):
        return humps.decamelize(await super().format(request))


class FileResponseFormatter(AbstractResponseFormatter):

    async def format(self, request):
        return await request.read()

