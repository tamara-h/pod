function XHRequest(variable, value)
{
    var request = new XMLHttpRequest();
    var url = "http://10.150.85.50:8000/" + variable + "=" + value;
    request.open("GET", url, false);
    request.send(null);
    
    return request.responseText;
}

function getWeatherFromAPI() {
    var url = "http://api.openweathermap.org/data/2.5/weather" +
    "?q=Swansea,uk&amp;units=metric";
    var request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send(null);
    var reply = JSON.parse(request.responseText);
    return reply;
}

/* Tamara's code from /project.html */

/* okay this is the start of my JavaScript code the example of a call to it (this is a button but you can mess with whatever else idk is
 to get temperature		<input type="submit" value="Temperature" onclick="gettemp()">  --> 
 to get description   <input type="submit" value="Weather" onclick="getweather()">
 to get icon     <input type="submit" value="Weather" onclick="geticon()">
    					<img id="icon" src="" alt="weather"> */

function geticon() {
    var reply = getWeatherFromAPI();
    var icon = "http://openweathermap.org/img/w/" +
      reply.weather[0].icon + ".png";
    var img = document.getElementById("iconx");
	alert(icon);
	img.src = icon;
}

function getweather() {
    var reply = getWeatherFromAPI();
    var description = reply.weather[0].description;
    var weatherDescription = document.getElementById("weatherDescription");
	if (weatherDescription != undefined)
    {
        weatherDescription.innerHTML = description;
    }
    XHRequest("weather", description);

    // alert(description);
}

function gettemp() {
    var reply = getWeatherFromAPI();
    var temperature = Math.round(reply.main.temp - 273.15);

    XHRequest("temp", temperature);
    //alert("Temp = " + temperature);

    // Update "OutdoorTemp" id object if it exists
    var outdoorTemp = document.getElementById("OutdoorTemp");
    if (outdoorTemp != undefined)
    {
        outdoorTemp.innerHTML = temperature;
    }
}