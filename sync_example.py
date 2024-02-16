from servic_request_helper.request_formatters import CamelizeRequestFormatter
from servic_request_helper.syncs.auth import AuthByServiceHeaderManager
from servic_request_helper.syncs.clients import RequestHelper
from servic_request_helper.syncs.response_formatters import JsonDecamelizeResponseFormatter, ContentResponseFormatter
from servic_request_helper.utils import MethodWrapper

HOST = 'https://api.startpoint.uz'
USERNAME = '***'
PASSWORD = '***'

auth_manager = AuthByServiceHeaderManager(
    host=HOST,
    auth_uri='/api/v1/account/public/login/password',
    credential={'login': USERNAME, 'password': PASSWORD},
    access_token_field='accessToken',
)


startpoint_api = MethodWrapper(RequestHelper(
    host=HOST,
    request_header_managers=[auth_manager],
    default_request_formatter=CamelizeRequestFormatter(),
    default_response_formatter=JsonDecamelizeResponseFormatter(),
))


my_profile = startpoint_api.get('/api/v1/account/user/me')

print('username:',  my_profile['username'])
print('first name:',  my_profile['first_name'])


photo = startpoint_api.get(
    '/api/v1/public-file/public/' + my_profile['profile_photo']['path'],
    response_formatter=ContentResponseFormatter(),
)

print(photo[:100])