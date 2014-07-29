from wsgiref.simple_server import make_server
from enum import Enum
import wsgiref as serv
import API2 as JAPI
import random

def request(environ, start_response):
    global mcServer
    
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
    start_response(status, headers)


    #print("Request URL {0}".format(serv.util.request_uri(environ)))
    requestURL = serv.util.request_uri(environ)
    
    # Should have a string such as x=y
    rURLComponents = requestURL.rpartition("/")[2].partition("=")
    
    # We should have ['x', '=', 'y']
    var = rURLComponents[0]
    val = rURLComponents[2]

    mcServer.resolveRequest(var, val)    

    return [b"If this text displays, server was accessed successfully"]

class Weather(Enum):
    Sunny = 1,
    Rainy = 2,

class serverInterface():
    def __init__(self):
        self.temp = 30
        self.weather = Weather.Sunny
        
        mc_conn = JAPI.Connection()    
        self.api = JAPI.JSONAPI(mc_conn)

    def resolveRequest(self, var, val):
        # Switch var
        if var == "temp":
            self.setTemperature(val)
        elif var == "weather":
            self.setWeather(val)
        
    def setTemperature(self, temp):
        print("[World Status Update] Temperature is: " + temp)
        

    def setWeather(self, weather):
        print("[World Status Update] Weather is: " + weather)
        if "rain" in weather:
            self.weather = Weather.Rainy
            self.api.server.run_command("weather rain")
        else:
            self.weather = Weather.Sunny
            self.api.server.run_command("weather sun")

    def worldUpdate(currTemp, currWeather):
        pass

    # Abstractions
    def openWindows(self):
        print("[House Change] Opening Windows")
        self.setWindows("air")
        
    def closeWindows(self):
        print("[House Change] Closing Windows")
        self.setWindows("glass")


    def lightFire(self):
        print("[House Change] Lighting fire")
        self.enableRedstone("119 71 97")
        self.disableRedstone("119 71 97")


    # Backend for abstractions
    def enableRedstone(self, position):
        print("[House Change] Enabling redstone at " + position)
        self.setBlocks("redstone_torch", [position])

    def disableRedstone(self, position):
        print("[House Change] Disabling redstone at " + position)
        self.setBlocks("air", [position])


    def setWindows(self, windowType):
        windows = ["119 72 99", "119 72 100", "118 72 100", "117 72 100", "116 72 100", "115 72 100"]
        self.setBlocks(windowType, windows)

    def setBlocks(self, blockType, blockList):
        for block in blockList:
            self.api.server.run_command("setblock " + block + " minecraft:" + blockType)

mcServer = serverInterface()
httpd = make_server('', 8000, request)
print("[Online] Awaiting requests on port 8000")

# Serve until process is killed
httpd.serve_forever()
