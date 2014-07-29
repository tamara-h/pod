from wsgiref.simple_server import make_server
from enum import Enum
import wsgiref as serv
import API2 as JAPI
import random

pLog = []

def print(*args, **kwargs):
    __builtins__.print(*args, **kwargs)
    for arg in args:
        server.pLog.append(arg)

class server():
    pLog = []
    mcServer = None

    @staticmethod
    def request(environ, start_response):
        server.pLog = []
        
        status = '200 OK' # HTTP Status
        headers = [('Content-type', 'text/plain; charset=utf-8'), ('Access-Control-Allow-Origin', '*')] # HTTP Headers
        start_response(status, headers)


        #print("Request URL {0}".format(serv.util.request_uri(environ)))
        requestURL = serv.util.request_uri(environ)
        
        # Should have a string such as x=y
        rURLComponents = requestURL.rpartition("/")[2].partition("=")
        
        # We should have ['x', '=', 'y']
        var = rURLComponents[0]
        val = rURLComponents[2]
        print("Variable: " + var + " has been set to value: " + val)
        server.mcServer.resolveRequest(var.lower(), val.lower())

        #return [b"String"]
        return server.formReply(var, val)

    @staticmethod
    def formReply(var, val):
        json = True

        if json:
            returnStr = bytes(
                    '{' + "\n" +
                    '\t"temperature": ' + str(server.mcServer.temperature) + ',\n' +
                    '\t"idealTemperature": ' + str(server.mcServer.idealTemperature) + ',\n' +
                    '\t"indoorTemperature": ' + str(server.mcServer.indoorTemperature) +  ',\n' +
                    '\t"weather": "' + ('sun' if (server.mcServer.indoorTemperature == Weather.Sunny) else 'rainy') + '",\n' +
                    '\t"houseStatus": {' + '\n' +
                    ''.join(['\t\t"{}": {},\n'.format(key, 'true' if value else 'false') for key, value in server.mcServer.house.items()])
                    + '\t}'
                    + '\n'
                    '}'
                , 'utf-8')
        else:
            returnStr = bytes("Server accessed successfully.\nYour request was: " + var + " = " + val + "."
                + "\n\nCurrent Variables Held in Server:"
                + "\n   Target Ideal Temperature:\t" + str(server.mcServer.idealTemperature) + "*C"
                + "\n   Temperature:\t\t\t" + str(server.mcServer.temperature) + "*C"
                + "\n   Indoor Temp:\t\t\t" + str(server.mcServer.indoorTemperature) + "*C"
                + "\n   Weather: " + str(server.mcServer.weather)
                + "\n   House Information:\n    " + "\n    ".join(["{0:15.15}: \t\t{1}".format(key, "Yes" if value else "No") for key, value in server.mcServer.house.items()])
                + "\n\n\nServer Log for Request: \n    " + "\n    ".join(server.pLog), 'utf-8')
        return [returnStr]

class Weather(Enum):
    Sunny = 1,
    Rainy = 2,

class serverInterface():
    def __init__(self):
        self.idealTemperature       = 23
        self.temperature            = 30
        self.indoorTemperature      = 30
        self.weather                = Weather.Sunny
        self.house                  = {}
        self.house["windowsOpen"]   = False
        self.house["doorsOpen"]     = False
        self.house["fireOn"]        = False
        
        mc_conn = JAPI.Connection()    
        self.api = JAPI.JSONAPI(mc_conn)

        # Initialise everything
        self.worldUpdate()

    def resolveRequest(self, var, val):
        # Switch var
        if var == "temp":
            self.setTemperature(val)
        elif var == "weather":
            self.setWeather(val)
        elif var == "indoortemp":
            self.setIndoorTemp(val)
        
    def setTemperature(self, temp):
        print("[World Status Update] Temperature is: " + temp)
        self.temperature = int(temp)
        self.worldUpdate()

    def setIndoorTemp(self, temp):
        print("[World Status Update] Indoor Temperature is " + temp)
        self.indoorTemperature = int(temp)
        self.worldUpdate()
        

    def setWeather(self, weather):
        print("[World Status Update] Weather is: " + weather)
        if "rain" in weather:
            self.weather = Weather.Rainy
            self.api.server.run_command("weather rain")
        else:
            self.weather = Weather.Sunny
            self.api.server.run_command("weather clear")
        self.worldUpdate()

    def worldUpdate(self):
        print("[Info] Re-initialising entire environment...")
        if self.weather == Weather.Rainy:
            if self.house["windowsOpen"] == True:
                self.closeWindows()
            else:
                print("[House Info] Windows Already Closed")
            if self.house["doorsOpen"] == True:
                self.closeDoors()
            else:
                print("[House Info] Doors Already Closed")

        if (self.idealTemperature - self.indoorTemperature) > 3:
            print("[House Info] Temperature is more than 3*C below ideal temperature. Engaging fire.")
            fireOn = True
            self.lightFire()
        elif (self.idealTemperature > self.indoorTemperature):
            print("[House Info] Temperature is hotter than the ideal temperature, fire put out.")

    # Abstractions
    def openWindows(self):
        print("[House Change] Opening Windows")
        self.setWindows("air")
        
    def closeWindows(self):
        print("[House Change] Closing Windows")
        self.setWindows("glass")


    def lightFire(self):
        print("[House Change] Lighting fire")
        self.enableRedstone("123 71 97")
        self.disableRedstone("123 71 97")


    def openDoors(self):
        print("[House Change] Opening Doors")
        self.enableRedstone("116 69 92")
        self.enableRedstone("115 69 92")

    def closeDoors(self):
        print("[House Change] Closing Doors")
        self.disableRedstone("116 69 92")
        self.disableRedstone("115 69 92")

    # Backend for abstractions
    def enableRedstone(self, position):
        print("[R-Change] Enabling redstone at " + position)
        self.setBlocks("redstone_torch", [position])

    def disableRedstone(self, position):
        print("[R-Change] Disabling redstone at " + position)
        self.setBlocks("air", [position])


    def setWindows(self, windowType):
        windows = ["119 72 99", "119 72 100", "118 72 100", "117 72 100", "116 72 100", "115 72 100"]
        self.setBlocks(windowType, windows)

    def setBlocks(self, blockType, blockList):
        for block in blockList:
            self.api.server.run_command("setblock " + block + " minecraft:" + blockType)

server.mcServer = serverInterface()
httpd = make_server('', 8000, server.request)
print("[Online] Awaiting requests on port 8000")

# Serve until process is killed
httpd.serve_forever()
