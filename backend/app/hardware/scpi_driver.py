import pyvisa

class SCPIInstrument:
    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(address)

    def run_test(self, params):
        idn = self.inst.query("*IDN?")
        # Send SCPI test sequence...
        return {"status": "OK", "die_data": [{"x":0,"y":0,"test":"IV","value":0.0012}]}
