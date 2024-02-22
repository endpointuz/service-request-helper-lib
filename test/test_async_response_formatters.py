import os
import unittest
from unittest.mock import Mock, AsyncMock

from servic_request_helper.asyncs import response_formatters as formatters
from servic_request_helper.types import ResponseFile


class AbstractTestJsonResponse(unittest.IsolatedAsyncioTestCase):

     def get_formatted_mock_response(self, formatter):
         mock_response = Mock()
         mock_response.status_code = 200
         mock_response.json = AsyncMock(return_value={
             "testField": "testValue",
             "nestedField": {
                 "inner1": "inner_1",
                 "innerTwo": "inner_two",
             }
         })

         return formatter.format(mock_response)


class TestFullResponseFormatter(AbstractTestJsonResponse):

    async def test(self):
        formatted_mock_response = await self.get_formatted_mock_response(formatters.FullResponseFormatter())

        self.assertEqual(formatted_mock_response.status_code, 200)
        self.assertDictEqual(
            await formatted_mock_response.json(),
            {
                "testField": "testValue",
                "nestedField": {
                    "inner1": "inner_1",
                    "innerTwo": "inner_two",
                }
            })


class TestJsonResponseFormatter(AbstractTestJsonResponse):

    async def test(self):
        formatted_mock_response = await self.get_formatted_mock_response(formatters.JsonResponseFormatter())

        self.assertDictEqual(
            formatted_mock_response,
            {
                "testField": "testValue",
                "nestedField": {
                    "inner1": "inner_1",
                    "innerTwo": "inner_two",
                }
            })



class TestJsonDecamelizeResponseFormatter(AbstractTestJsonResponse):

    async def test(self):
        formatted_mock_response = await self.get_formatted_mock_response(formatters.JsonDecamelizeResponseFormatter())

        self.assertDictEqual(
            formatted_mock_response,
            {
                "test_field": "testValue",
                "nested_field": {
                    "inner1": "inner_1",
                    "inner_two": "inner_two",
                }
            })


class AbstractTestContentResponse(unittest.IsolatedAsyncioTestCase):

    def get_formatted_mock_response(self, formatter):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.read = AsyncMock(return_value=b'testText')
        mock_response.headers = {
            'Content-Disposition': 'attachment; filename=test.png',
            'Content-Type': 'image/png',
        }

        return formatter.format(mock_response)


class TestContentResponseFormatter(AbstractTestContentResponse):

    async def test(self):
        formatted_mock_response = await self.get_formatted_mock_response(formatters.ContentResponseFormatter())

        self.assertEqual(formatted_mock_response, b'testText')


class TestFileResponseFormatter(AbstractTestContentResponse):

    async def test(self):
        formatted_mock_response = await self.get_formatted_mock_response(formatters.FileResponseFormatter())

        self.assertIsInstance(formatted_mock_response, ResponseFile)

        self.assertEqual(getattr(formatted_mock_response, 'content', None), b'testText')
        self.assertEqual(getattr(formatted_mock_response, 'filename', None), 'test.png')
        self.assertEqual(getattr(formatted_mock_response, 'mimetype', None), 'image/png')
        self.assertEqual(getattr(formatted_mock_response, 'size_in_bytes', None), len(b'testText'))

        formatted_mock_response.save('./test_file_response_formatter.txt')

        with open('./test_file_response_formatter.txt', 'rb') as file:
            read_file = file.read()

        self.assertEqual(read_file, b'testText')

    def tearDown(self):
        os.remove('./test_file_response_formatter.txt')
