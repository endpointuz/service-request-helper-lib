Introduction
=======
Service Request Helper is a Python library designed to abstract http requests with shared properties.
It contains minimal amount of external dependencies, and supports both sync and async modes of operation.


Installation
=========
Install locally via pip:
```commandline
pip install service-request-helper[sync]
```
or
```
pip install service-request-helper[async]
```


Basic usage
==========
Depending on the execution context (sync or async), some import statements will differ. For async requests,
the response must also be awaited:

Sync
------
```python
from servic_request_helper.syncs.clients import RequestHelper
from servic_request_helper.utils import MethodWrapper

api = MethodWrapper(RequestHelper(
    host='https://example.com'
))

response = api.get('/example')
```

Async
------
```python
from servic_request_helper.asyncs.clients import RequestHelper
from servic_request_helper.utils import MethodWrapper

api = MethodWrapper(RequestHelper(
    host='https://example.com'
))


async def main():
    response = await api.get('/example')
```

Classes such as RequestHelper are doubled in _.syncs_ and _.asyncs_ subpackages. Such classes will be marked with
(sync/async) note in this documentation. They have the same name, same constructor
arguments and serve the same purpose. The only difference is in the execution context (sync or async).

All HTTP methods are exposed via the MethodWrapper instance methods:
- GET - .get
- POST - .post
- PUT - .put
- PATCH - .patch
- DELETE - .delete
- HEAD - .head

MethodWrapper constructor accepts RequestHelper (see the "RequestHelper class" section) instance as its one and
only argument, which contains shared properties for all http requests that will be made with the 
given MethodWrapper instance.


RequestHelper class (sync/async)
=====
RequestHelper class contains settings that will be applied to each http request that will be made 
with the corresponding MethodWrapper instance. Depending on the context (sync or async), RequestHelper can be imported
from _.asyncs_ subpackage for async requests or _.syncs_ subpackage for sync requests.

RequestHelper class constructor accepts the following required arguments:
- **host** - A host part of the url where each individual request will be sent

and the following optional arguments:
- **default_request_formatter** - A formatter applied to request query parameters and body, if any are provided,
before the request is sent. Can be overriden on per-request basis via _request_formatter_ kwarg 
(see "Making HTTP requests" section). If not provided, the DefaultRequestFormatter instance is used (see "Request formatters" section).
- **default_response_formatter** - A formatter applied to response body, after the request is successfully completed. 
Can be overriden on per-request basis via _response_formatter_ kwarg (see "Making HTTP requests" section). 
If not provided, the FullResponseFormatter instance is used (see "Request formatters" section).
- **request_header_managers** - A list or tuple of header manager instances (see "Request header managers" section) for generating headers during request execution. 
Each header manager corresponds to single header key:value pair sent with each individual request. An empty tuple is used by default.
- **default_response_error_builder** - A class, which maps unsuccessful response to error class by response status code
  (see "Response error builder" section). 


Request header managers
======
Request header managers provide additional request headers to the request before it is sent.

Each header manager must be an inheritor of the AbstractRequestHeaderManager class and implement .get_header_name() 
and .get_header_value() methods. Method .get_header_name() provides header key and method .get_header_value()
provides header value. 

During the request execution, any existing request headers will be supplemented by 
headers retrieved from header managers passed to corresponding RequestHelper instance. 
**Each header manager is responsible for one header only**.


Passing Authorization to http request
==========
Authorization is set via AuthByServiceHeaderManager (sync/async) request header manager instance, which is passed to 
RequestHelper constructor as a member of the _request_header_managers_ list or tuple.

```python
from servic_request_helper.syncs.auth import AuthByServiceHeaderManager
from servic_request_helper.syncs.clients import RequestHelper
from servic_request_helper.utils import MethodWrapper

auth_manager = AuthByServiceHeaderManager(
    host='https://example.com',
    auth_uri='/auth/example',
    credential={'login': '***', 'password': '***'},
    access_token_field='accessToken',
)

api = MethodWrapper(RequestHelper(
    host='https://example.com',
    request_header_managers=[auth_manager],
))
```

AuthByServiceHeaderManager accepts the following required arguments:
- **host** - A host part of the url for authorization request
- **auth_uri** - A uri path component of the authorization endpoint url
- **credential** - A dict of authorization credentials, which is passed as request body to the authorization endpoint

and the following optional arguments:
- **access_token_field** - A name of the field in the response body of the authorization endpoint, 
which contains the bearer token to be used for authorization for requests to the API. Default value is 'access_token'.
- **access_expire_at_field** - A name of the field in the response body of the authorization endpoint, 
which contains the string representation of token expiry date and time. Default value is None.
- **datetime_converter** - A function to convert the string representation of token expiry date and time, retrieved 
from the response body, to the python datetime object. Default value is datetime.fromisoformat.


Making HTTP requests
=======
All HTTP requests are made through the corresponding methods of the MethodWrapper instance. Each method has
the same set of required and optional arguments as its input:

Required arguments:
- **uri** - A uri path component of the endpoint url where the request will be sent

Optional arguments:
- **request_formatter** - An instance of the inheritor of AbstractRequestFormatter class. Used to format request query params
and body before the request is sent. Overrides _default_request_formatter_ of the RequestHelper.
- **response_formatter** - An instance of the inheritor of AbstractResponseFormatter class. Used to format response body
after successful response to the request. Overrides _default_response_formatter_ of the RequestHelper.
- **response_error_builder** - An instance of the inheritor of AbstractResponseErrorBuilder class. Used to map 
unsuccessful response to error class by response status code. Overrides _default_response_error_builder_ of the
RequestHelper class.
- **params** - A dict of the query params to be sent with the request
- **data** - A dict to be added to request body. Either _data_ or _json_ argument can be set, not both.
- **json** - A dict to be added to request body in json format. Either _data_ or _json_ argument can be set, not both.
- **files** - A dict of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
        ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
        or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
        defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
        to add for the file.
- **headers** - A dict of additional headers to add to headers generated by _request_header_managers_ of the 
RequestHelper class.
- **\*\*kwargs** - Any additional keyword arguments to be passed to underlying request method.

All optional arguments are None by default.


Request formatters
======
Request formatters are used to modify request query params or body before the request is sent. Each request formatter 
must inherit from AbstractRequestFormatter and implement _.format_ method, which accepts dict and must return dict.

Library provides the following request formatters:
- **DefaultRequestFormatter()** - Does not perform formatting on the data
- **CamelizeRequestFormatter()** - Transforms dict keys of the data to be formatted to camelCase


Response formatters (sync/async)
=======
Response formatters are used to modify response body after the successful execution of the request and before 
it is returned to client. Each response formatter must inherit from AbstractResponseFormatter 
and implement _.format_ method, which accepts response object and must return processed response body.

Async response object's methods must be awaited before they are returned to client.

Library provides the following response formatters for sync and async:
- **FullResponseFormatter()** - Does not perform formatting on the response, response object will be passed to client
- **JsonResponseFormatter()** - Retrieves json body of the response without modifying it
- **JsonDecamelizeResponseFormatter()** - Retrieves json body of the response with keys formatted to snake_notation
- **ContentResponseFormatter()** - Retrieves the file content of the response


Response error builder (sync/async)
=======
Response error builder is used to map unsuccessful response to relevant exception class by response status code and 
raise its exception. Each response error builder must inherit from AbstractResponseErrorBuilder class and implement its
_build_error_ method, which accepts url, request method and response object, and raises suitable exception from .errors
module. 

Async response object's methods must be awaited before they are returned to client.

Library provides the following response error builders for sync and async:
- **ResponseStatusErrorBuilder()** - Handles most common response status codes for unsuccessful requests
