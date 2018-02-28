class Packet():
    def __init__(self, header, payload):
        self._header = header
        self._payload = payload

    @staticmethod
    def pack(header, line):
        n = 500
        lines = [line[i:i+n] for i in range(0, len(line), n)]
        packets = [Packet(header, payload) for payload in lines]
        return packets