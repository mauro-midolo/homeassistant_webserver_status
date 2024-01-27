class ConnectionStatus():
    def __init__(self, hostname_alis, hostname, state, durantion):
        self._hostname_alis = hostname_alis
        self._hostname = hostname
        self._data = {"state": state, "duration": durantion}