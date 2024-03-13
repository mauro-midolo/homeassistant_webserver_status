

from .connectionresult import ConnectionStatus

import time
import requests

class HttpClient():
    
    def get_request(self, url, ssl_check=True) -> ConnectionStatus:
        try:
            start_time = time.time()
            response = requests.get(url=url, allow_redirects=False, timeout=5, verify=ssl_check)
            end_time = time.time()
            state_result = "online"
            duration_time = round(end_time - start_time, 2)
            return ConnectionStatus(url, state_result, duration_time, response.status_code)
        except requests.RequestException:
            return ConnectionStatus(url, "offline", None, None)