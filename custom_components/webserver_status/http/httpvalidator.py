from urllib.parse import urlparse

class HttpValidator:
    def is_valid(self, url) -> bool:
        try:
            p = urlparse(url)
            if p.scheme.lower() not in ("http", "https") or not p.netloc:
                return False
            if "://" in url and "[" not in p.netloc and "]" not in p.netloc and p.netloc.count(":") >= 2:
                return False
            return True
        except ValueError:
            return False
