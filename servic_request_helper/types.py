from servic_request_helper.utils import get_filename_from_content_disposition_header


class ResponseFile:
    content = None
    filename = None
    type = None
    extension = None

    def __init__(self, content, headers):
        self.content = content

        content_disposition = headers.get('Content-Disposition', '')
        self.filename = get_filename_from_content_disposition_header(content_disposition)

        content_type_list = headers.get('Content-Type', '').split('/')
        if len(content_type_list) == 2:
            self.type = content_type_list[0] or None
            self.extension = content_type_list[1] or None

    @property
    def size_in_bytes(self):
        return len(self.content)


    def save(self, path):
        with open(path, 'wb') as file:
            result = file.write(self.content)
        return result