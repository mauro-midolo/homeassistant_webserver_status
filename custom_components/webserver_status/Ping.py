class ConnectionStatus():
    def __init__(self, hostname, state, durantion, response_status):
        self._hostname = hostname
        self._data = {"state": state, "response_time": durantion, "response_status": response_status}