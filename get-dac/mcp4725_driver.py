import smbus
class MCP4725:
    def __init__(self, dynamuc_range, address = 0x61, verbose = True):
        