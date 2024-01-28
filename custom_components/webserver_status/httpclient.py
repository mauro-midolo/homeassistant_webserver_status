

from .Ping import ConnectionStatus

import time
import requests

class HttpClient():
    
    def get_request(self, url) -> ConnectionStatus:
        try:
            start_time = time.time()
            response = response = requests.get( self._hostname, timeout=5)
            end_time = time.time()
            state_result="offline"
            if response.status_code == 200:
                state_result = "online"
            duration_time = round(end_time - start_time, 2)
            return ConnectionStatus(self._hostname, state_result, duration_time, response.status_code)
        except requests.RequestException:
            return ConnectionStatus(self._hostname, "offline", None, None)