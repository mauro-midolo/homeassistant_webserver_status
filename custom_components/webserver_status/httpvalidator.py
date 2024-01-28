from urllib.parse import urlparse

class HttpValidator():

    def is_valid(self, url) ->bool:
        try:
            parsed_url = urlparse(url)
            return parsed_url.scheme.lower() in ['http', 'https'] and parsed_url.netloc != ''
        except ValueError:
            return False