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

    print("Request URL {0}".format(serv.util.request_uri(environ)))
    requestURL = serv.util.request_uri(environ)
    requestURL = requestURL[7:]
    print(requestURL)
    num = 1
    # Could use partition but may mess up in edge cases like "http://" being omitted from request string
    for char in requestURL:
        if char.isnumeric() or char == "." or char == ":":
            num += 1
            continue
        else:
            break

    requestURL = requestURL[num:].lower()
    print(requestURL)
    # Should have a string such as x=y
    rURLComponents = requestURL.partition("=")
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
    print("Temperature is: " + temp)

def setWeather(api, weather):
    print("Weather is: " + weather)
    if "rain" in weather:
        print("Rainy")
        api.server.run_command("weather rain")
    else:
        print("Sunny")
        api.server.run_comment("weather sun")

# Abstractions
def openWindows(api):
    print("Opening Windows")
    setWindows(api, "air")
def closeWindows(api):
    print("Closing Windows")
    setWindows(api, "glass")

def lightFire(api):
    print("Lighting fire")
    enableRedstone(api, "122 71 97")
    disableRedstone(api, "122 71 97")

# Backend for abstractions
def enableRedstone(api, position):
    print("Enabling redstone at " + position)
    setBlocks(api, "redstone_torch", [position])
def disableRedstone(api, position):
    print("Disabling redstone at " + position)
    setBlocks(api, "air", [position])

def setWindows(api, windowType):
    windows = ["119 72 99", "119 72 100", "118 72 100", "117 72 100", "116 72 100", "115 72 100"]
    setBlocks(api, windowType, windows)

def setBlocks(api, blockType, blockList):
    for block in blockList:
        print("setblock " + block + " minecraft:" + blockType)
        api.server.run_command("setblock " + block + " minecraft:" + blockType)
    
httpd = make_server('', 8000, request)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
