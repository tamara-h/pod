from wsgiref.simple_server import make_server
import wsgiref as serv
import API2 as JAPI

def hello_world_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
    start_response(status, headers)
    '''
    mc_conn = JAPI.Connection()    
    api = JAPI.JSONAPI(mc_conn)
    api.players.name.ban("exterminationguy", "Test")
    '''
    print("Request URL {0}".format(serv.util.request_uri(environ)))    
    return [b"Hello World"]

httpd = make_server('', 8000, hello_world_app)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
