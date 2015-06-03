window.addEventListener("load", loadOptions);

function init()
{
	document.getElementById("optionsSaveButton").addEventListener("click", saveOptions);
}

function loadOptions() {
	var togglApiKey = localStorage["togglApiKey"];
	document.getElementById('togglApiKey').value = togglApiKey;
	console.log('Tried to load');
}

function saveOptions() {
	var togglApiKey = document.getElementById('togglApiKey').value
	localStorage["togglApiKey"] = document.getElementById('togglApiKey').value;
	console.log('Saved value %s', togglApiKey);
}

function eraseOptions() {
	localStorage.removeItem("togglApiKey");
	location.reload();
}

window.onload = init
