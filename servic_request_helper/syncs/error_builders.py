from servic_request_helper import errors


class ResponseStatusErrorBuilder:
    _ERROR_BY_STATUS_MAP = {
        400: errors.ApiBadRequestError,
        401: errors.ApiUnauthorizedError,
        403: errors.ApiForbiddenError,
        404: errors.ApiNotFoundError,
        502: errors.ApiBadGatewayError,
        504: errors.ApiGatewayTimeoutError,
    }

    def build_error(self, url, method, response):
        if response.status_code // 100 == 2:
            return None
        # todo: add service api error handel
        error_class = self._ERROR_BY_STATUS_MAP.get(response.status_code)

        if not error_class:
            if response.status_code // 100 == 4:
                error_class = errors.ApiClientError
            elif response.status_code // 100 == 5:
                error_class = errors.ApiServerError
            else:
                error_class = errors.ApiResponseWithError

        return error_class(url, method, response.status_code, response.text)


