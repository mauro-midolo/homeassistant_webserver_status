from datetime import datetime, timezone


class ConnectionStatus():
    def __init__(self, hostname, state, durantion, response_status, error=None):
        self._hostname = hostname
        self._data = {
            "state": state,
            "response_time": durantion,
            "response_status": response_status,
            "error": error,
            "last_check": datetime.now(timezone.utc),
        }
