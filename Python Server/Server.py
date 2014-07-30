from wsgiref.simple_server  import make_server
from STwilio                import TwilioMessages, TwilioClient
from enum                   import Enum
import wsgiref  as serv
import API2     as JAPI
import math
import copy
import json

def print(*args, **kwargs):
    __builtins__.print(*args, **kwargs)
    for arg in args:
        server.pLog.append(arg)

class server():
    pLog        = []
    mcServer    = None
    twilio      = None

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
        if not var == "ignore":
            server.mcServer.resolveRequest(var.lower(), val.lower())
        else:
            print("Ignored request, responding with data.")
        
        #return [b"String"]
        return server.formReply(var, val)

    @staticmethod
    def formReply(var, val):
        returnStr = bytes(json.dumps(dict(temperature = server.mcServer.temperature, idealTemperature = server.mcServer.idealTemperature,
                        indoorTemperature = server.mcServer.indoorTemperature,
                        weather = "sun" if server.mcServer.weather == Weather.Sunny else "rain",
                        houseStatus = server.mcServer.house,
                        printedData = server.pLog)), 'utf-8')
        return [returnStr]

class Weather(Enum):
    Sunny = 1,
    Rainy = 2,

class ServerInterface():
    def __init__(self):
        self.idealTemperature       = 23
        self.temperature            = 30
        self.indoorTemperature      = 30
        self.weather                = Weather.Sunny
        self.house                  = {}
        self.house["windowsOpen"]   = False
        self.house["doorsOpen"]     = False
        self.house["fireOn"]        = False
        self.house["powerOn"]       = False
        self.house["flooded"]       = False
        
        mc_conn = JAPI.Connection()    
        self.api = JAPI.JSONAPI(mc_conn)

        # Initialise everything
        self.worldUpdate()

    def resolveRequest(self, var, val):
        # Switch var
        # Sensory information updates
        if var == "temp":
            self.setTemperature(val)
        elif var == "weather":
            self.setWeather(val)
        elif var == "indoortemp":
            self.setIndoorTemp(val)
        # Forced house updates
        elif var == "doorsopen":
            self.openDoors()    if val == "true" else self.closeDoors()
        elif var == "windowsopen":
            self.openWindows()  if val == "true" else self.closeWindows()
        elif var == "fireon":
            self.lightFire()    if val == "true" else self.extinguishFire()
        elif var == "poweron":
            self.enablePower()  if val == "true" else self.disablePower()
        elif var == "flooded":
            self.floodHouse()   if val == "true" else self.drainHouse()
        
        
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
        else:
            self.weather = Weather.Sunny
        self.worldUpdate()

    def worldUpdate(self):
        print("[Info] Re-initialising entire environment...")

        buffer = self.house.copy()
        
        # OPEN WINDOWS IF OUTSIDE TEMPERATURE IS MORE DESIRABLE THAN INSIDE TEMPERATURE >3S*
        if abs(self.indoorTemperature - self.idealTemperature) - abs(self.temperature - self.idealTemperature) > 3:
            buffer["windowsOpen"]   = True
            buffer["fireOn"]        = False

        if self.indoorTemperature >= 3000:
            server.twilio.sendMessage(TwilioMessages.extremeHeat)

        # CLOSE DOORS & WINDOWS FOR RAIN
        if self.weather == Weather.Rainy:
            buffer["windowsOpen"]   = False
            buffer["doorsOpen"]     = False

        # TEMPERATURE SENSITIVE FIRE
        if self.idealTemperature - self.indoorTemperature > 3:
            buffer["fireOn"]        = True
        elif self.indoorTemperature > self.idealTemperature:
            buffer["fireOn"]        = False

        # UPDATE WEATHER
        if self.weather == Weather.Sunny:
            self.api.server.run_command("weather clear")
        else:
            self.api.server.run_command("weather rain")

        # Min temp 15; Max temp 25
        if self.indoorTemperature <= 16 or self.indoorTemperature >= 24:
            server.twilio.sendMessage(TwilioMessages.tempWarn)
        
        # Reflect buffer changes in-game
        self.actionIf(self.bufferDiffers(buffer, "windowsOpen"  ), self.openWindows if buffer["windowsOpen"]    else self.closeWindows  )
        self.actionIf(self.bufferDiffers(buffer, "fireOn"       ), self.lightFire   if buffer["fireOn"]         else self.extinguishFire)
        self.actionIf(self.bufferDiffers(buffer, "doorsOpen"    ), self.openDoors   if buffer["doorsOpen"]      else self.closeDoors    )

        # Now merge buffer into house
        self.house = buffer
        
    def bufferDiffers(self, buffer, val):
        if self.house[val] != buffer[val]:
            return True
        else:
            return False
        
    def actionIf(self, condition, action):
        if condition:
            action()

    # Abstractions
    def openWindows(self):
        print("[House Change] Opening Windows")
        self.house["windowsOpen"] = True
        self.setWindows("air")
        
    def closeWindows(self):
        print("[House Change] Closing Windows")
        self.house["windowsOpen"] = False
        self.setWindows("glass")


    def lightFire(self):
        print("[House Change] Lighting Fire")
        self.enableRedstone("123 71 97")
        self.disableRedstone("123 71 97")
        self.house["fireOn"] = True

    def extinguishFire(self):
        print("[House Change] Extinguish Fire")
        self.setBlocks("air", ["119 71 97"])
        self.house["fireOn"] = False

    def openDoors(self):
        print("[House Change] Opening Doors")
        self.house["doorsOpen"] = True
        self.enableRedstone("116 69 92")
        self.enableRedstone("115 69 92")

    def closeDoors(self):
        print("[House Change] Closing Doors")
        self.house["doorsOpen"] = False
        self.disableRedstone("116 69 92")
        self.disableRedstone("115 69 92")

    def enablePower(self):
        self.enableRedstone("113 70 94")
        self.house["powerOn"] = True

    def disablePower(self):
        self.disableRedstone("113 70 94")
        self.house["powerOn"] = True

    def floodHouse(self, unflood = False):
        innerHouseRect = [(114, 74, 94), (118, 74, 99)]
        for x in range(innerHouseRect[0][0], innerHouseRect[1][0] + 1):
            for z in range(innerHouseRect[0][2], innerHouseRect[1][2] + 1):
                self.setBlocks("water" if not unflood else "air", [str(x) + " " + str(innerHouseRect[0][1]) + " " + str(z)])#

        if not unflood:
            server.twilio.sendMessage(TwilioMessages.flood)
        self.house["flooded"] = True

    def drainHouse(self):
        self.floodHouse(True)
        self.house["flooded"] = False

    # Backend for abstractions
    def enableRedstone(self, position):
        print("[R-Change] Enabling redstone at " + position)
        self.setBlocks("redstone_torch", [position])

    def disableRedstone(self, position):
        print("[R-Change] Disabling redstone at " + position)
        self.setBlocks("air", [position])


    def setWindows(self, windowType):
        windows = ["119 72 99", "119 72 100", "118 72 100", "117 72 100", "116 72 100", "115 72 100", "118 73 93", "118 72 93", "109 74 98"]
        self.setBlocks(windowType, windows)

    def setBlocks(self, blockType, blockList):
        for block in blockList:
            self.api.server.run_command("setblock " + block + " minecraft:" + blockType)

server.twilio   = TwilioClient()
server.mcServer = ServerInterface()
httpd           = make_server('', 8000, server.request)
print("[Online] Awaiting requests on port 8000")

# Serve until process is killed
httpd.serve_forever()
