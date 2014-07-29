function XHRequest(variable, value)
{
    var request = new XMLHttpRequest();
    var url = "http://localhost:8000/" + variable + "=" + value
    request.open("GET", url, false);
    request.send(null);
    
    return request.responseText;
}