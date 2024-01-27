class ConnectionStatus():
    def __init__(self, hostname, state, durantion):
        self._hostname = hostname
        self._data = {"state": state, "response_time": durantion}