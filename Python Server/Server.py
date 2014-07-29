from wsgiref.simple_server import make_server
import wsgiref as serv
import API2 as JAPI
import random



def request(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
    start_response(status, headers)
    
    mc_conn = JAPI.Connection()    
    api = JAPI.JSONAPI(mc_conn)

    #print("Request URL {0}".format(serv.util.request_uri(environ)))
    requestURL = serv.util.request_uri(environ)
    
    # Should have a string such as x=y
    rURLComponents = requestURL.rpartition("/")[2].partition("=")
    
    # We should have ['x', '=', 'y']
    var = rURLComponents[0]
    val = rURLComponents[2]

    # Now we switch var
    if var == "temp":
        setTemperature(api, val)
    elif var == "weather":
        setWeather(api, val)

    lightFire(api)

    return [b"If this text displays, server was accessed successfully"]


def setTemperature(api, temp):
    print("[World Status Update] Temperature is: " + temp)
    

def setWeather(api, weather):
    print("[World Status Update] Weather is: " + weather)
    if "rain" in weather:
        print("Rainy")
        api.server.run_command("weather rain")
    else:
        print("Sunny")
        api.server.run_command("weather sun")

# Abstractions
def openWindows(api):
    print("[House Change] Opening Windows")
    setWindows(api, "air")
    
def closeWindows(api):
    print("[House Change] Closing Windows")
    setWindows(api, "glass")


def lightFire(api):
    print("[House Change] Lighting fire")
    enableRedstone(api, "119 71 97")
    disableRedstone(api, "119 71 97")


# Backend for abstractions
def enableRedstone(api, position):
    print("[House Change] Enabling redstone at " + position)
    setBlocks(api, "redstone_torch", [position])

def disableRedstone(api, position):
    print("[House Change] Disabling redstone at " + position)
    setBlocks(api, "air", [position])


def setWindows(api, windowType):
    windows = ["119 72 99", "119 72 100", "118 72 100", "117 72 100", "116 72 100", "115 72 100"]
    setBlocks(api, windowType, windows)

def setBlocks(api, blockType, blockList):
    for block in blockList:
        api.server.run_command("setblock " + block + " minecraft:" + blockType)
    
httpd = make_server('', 8000, request)
print("[Online] Awaiting requests on port 8000")

# Serve until process is killed
httpd.serve_forever()
