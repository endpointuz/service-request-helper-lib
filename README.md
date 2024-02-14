Introduction
=======
Service Request Helper is a Python library designed to abstract http requests with shared properties.
It contains minimal amount of external dependencies, and supports both sync and async modes of operation.


Installation
=========
Install locally via pip:
```commandline
pip install "service-request-helper @ git+https://github.com/endpointuz/service-request-helper-lib.git"
```
In requirements.txt:
```text
service-request-helper @ git+https://github.com/endpointuz/service-request-helper-lib.git
```


Basic usage
==========
All HTTP methods are exposed via the MethodWrapper instance methods:
- GET - .get()
- POST - .post()
- PUT - .put()
- PATCH - .patch()
- DELETE - .delete()
- HEAD - .head()

MethodWrapper constructor accepts RequestHelper (see the "RequestHelper class" section) instance as its one and only argument,
which contains shared properties for all http requests that will be made with the given MethodWrapper instance.
Depending on the execution context (sync or async), some import statements will differ:

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


RequestHelper class
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
Authorization is set via AuthByServiceHeaderManager request header manager instance, which is passed to 
RequestHelper constructor as a member of the _request_header_managers_ list or tuple. Same as the RequestHelper, 
AuthByServiceHeaderManager can be imported from .syncs or .asyncs subpackage depending on the execution context.

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
the same set of positional and keyword arguments as its input:


Positional arguments
-----
- uri - Bb


Keyword arguments
-----
- request_formatter - Bb
- response_formatter - Bb


Request formatters
======
Aa


Response formatters
=======
Aa


Response error builder
=======
Aa
