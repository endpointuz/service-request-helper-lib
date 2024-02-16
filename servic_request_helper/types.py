class ResponseFile:
    content = None
    filename = None
    type = None
    subtype = None

    def __init__(self, content, filename=None, type=None, subtype=None):
        self.content = content
        self.filename = filename
        self.type = type
        self.subtype = subtype

    @property
    def size_in_bytes(self):
        return len(self.content)


    def save(self, path):
        with open(path, 'wb') as file:
            result = file.write(self.content)
        return result