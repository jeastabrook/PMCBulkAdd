

class Url():

    # check to ensure that the https:// precedes the url
    def __init__(self, url):
        if url.startswith("http://"):
            self.url = url.replace('http://', 'https://')
        if not url.startswith('https://'):
            self.url = 'https://' + url
        else:
            self.url =  url

    # Allow URL to be represented as a string
    def __repr__(self):
        return self.url


    # Allow string concatenation
    def __add__(self, other):
        return str(self) + other

    # Allow string concatenation
    def __radd__(self, other):
        return other + str(self)


    # Method to iterate through the url based on the offset
    # To-Do: add the ability to manipulate the limit
    def next(self, path, offset):
        components = path.split('?')
        if len(components) == 2:
            return self.url + components[0] + f'?limit=200&offset={offset}' + f'&{components[1]}'
        else:
            return self.url + path + f'?limit=200&offset={offset}'
