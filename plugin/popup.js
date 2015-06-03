window.addEventListener("load", loadOptions);

function loadOptions() {
	var togglApiKey = localStorage["togglApiKey"];
	document.getElementById('togglApiKey').innerHTML = togglApiKey;
	console.log('Tried to load');
}

