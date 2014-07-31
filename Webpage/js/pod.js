function XHRequest(variable, value)
{
    var request = new XMLHttpRequest();
    var url = "http://10.150.85.50:8000/" + variable + "=" + value;
    request.open("GET", url, false);
    request.send(null);
    
    return request.responseText;
}

function getWeatherFromAPI() {
    var url = "http://api.openweathermap.org/data/2.5/weather?q=" + updateLocation() + "&amp;units=metric";
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
	//TEMPORARY COMMENTING OUT FOR TESTING PURPOSES NOW
    XHRequest("weather", description);
}

function gettemp() {
    var reply = getWeatherFromAPI();
    var temperature = Math.round(reply.main.temp - 273.15);
    var outdoorTemp = document.getElementById("OutdoorTemp");
    if (outdoorTemp != undefined)
    {
        outdoorTemp.innerHTML = temperature;
    }
	//TEMPORARY COMMENTING OUT FOR TESTING PURPOSES NOW
    XHRequest("temp", temperature);
}

function getPressure() {
	var reply = getWeatherFromAPI();
	var pressure = reply.main.pressure;
	var currentPressure = document.getElementById("currentPressure");
	if (currentPressure != undefined) {
		currentPressure.innerHTML = pressure;
	}
}

function getHumidity() {
	var reply = getWeatherFromAPI();
	var humidity = reply.main.humidity;
	var currentHumidity = document.getElementById("currentHumidity");
	if (currentHumidity != undefined) {
		currentHumidity.innerHTML = humidity;
	}
}

function getWindSpeed() {
	var reply = getWeatherFromAPI();
	var speed = reply.wind.speed;
	var currentSpeed = document.getElementById("windSpeed");
	if (currentSpeed != undefined) {
		currentSpeed.innerHTML = speed;
	}
}

//This function may not be necessary if we implement a way of letting the user set a location- at the moment all it does is display what location it is calling the API for 
function getLocationFromAPI() {
	var reply = getWeatherFromAPI();
	var location = reply.name;
	var APILocation = document.getElementById("APILocation");
	if (APILocation != undefined) {
		APILocation.innerHTML = location;
	}
}


function changeMode(type) {
switch (type) {
	case holiday: 
		holidaymode();
		break;
	case day:
		daymode();
		break;
	case night:
		nightmode();
		break;
	case away:
		awaymode();
		break;

}


}
// Auto set location if unset
if (localStorage.getItem("location") === null)
{
	localStorage.setItem("location", "plymouth,uk");
}