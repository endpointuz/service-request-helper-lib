import humps

from servic_request_helper.abstracts import AbstractResponseFormatter
from servic_request_helper.types import ResponseFile


class FullResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return response


class JsonResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return await response.json()


class JsonDecamelizeResponseFormatter(JsonResponseFormatter):

    async def format(self, response):
        return humps.decamelize(await super().format(response))


class ContentResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return await response.read()


class FileResponseFormatter(AbstractResponseFormatter):

    async def format(self, response):
        return ResponseFile(await response.read(), response.headers)
