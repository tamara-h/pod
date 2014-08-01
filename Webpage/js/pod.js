if(!console) {console={}; console.log = function(){};}

function XHRequest(variable, value){
	var returnV;
	$.ajax({
		url: ("http://141.163.72.31:42070/" + variable + "=" + value),
		async: false,
		success: function(result) {
			returnV = result;
		}
	});
	return returnV;
}

function getWeatherFromAPI() {
    var url = "http://api.openweathermap.org/data/2.5/weather?q=" + localStorage.getItem("location") + "&amp;units=metric";
    var request = new XMLHttpRequest();
    request.open("GET", url, false);
    request.send(null);
    var reply = JSON.parse(request.responseText);
    return reply;
}

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

function PowerOn(ifOn) {
  XHRequest("PowerOn", ifOn);
}
  
function LightsOn(ifLOn) { 
	XHRequest("LightsOn", ifLOn);
	lightsStatus(); 
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
		PowerOn(false);
		LightsOn(false);
		break;
	case day:
		PowerOn(true);
		LightsOn(false);
		break;
	case night:
		PowerOn(false);
		LightsOn(true);
		break;
	case away:
		PowerOn(false);
		LightsOn(false);
		break;

	}
}

function doorChange(state){
				XHRequest("doorsOpen", state);
				doorsStatus();
		  }

function doorsStatus() {
				var responseText = XHRequest("ignore", "x");
				var data = JSON.parse(responseText);
				
				var doorOpen = data.houseStatus.doorsOpen;
				
				$('#doorStatus').html( doorOpen ? "Open" : "Locked" );
				
				if (doorOpen)
					$('#Alert').show();
				else
					$('#Alert').hide();
}

function lightsStatus(){
	var responseText = XHRequest("ignore", "x");
	var data = JSON.parse(responseText);
	var lightsOn = data.houseStatus.lightsOn;
	$('#lightsStatus').html( lightsOn ? "On" : "Off" );
	//alert (lightsOn);
}

function windowChange(state){
				XHRequest("windowsOpen", state);
				windowStatus();
}
		  
function windowStatus() {
	var responseText = XHRequest("ignore", "x");
	var data = JSON.parse(responseText);
	var windowStatus = data.houseStatus.windowsOpen;
		$('#windowStatus').html( windowStatus ? "Open" : "Closed" );
}



if (localStorage.getItem("location") === null)
{
	localStorage.setItem("location", "plymouth,uk");
}
