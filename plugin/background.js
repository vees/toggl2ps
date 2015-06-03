// based from this https://carl-topham.com/theblog/post/creating-chrome-extension-uses-jquery-manipulate-dom-page/

$(".PAPAGETITLE").append('&nbsp; <a href="#" id="validateJobs">Validate Toggl Jobs</a> <div id="validationResults"></div>');
console.log('hello');

function onValidateButtonPush() {
	// http://stackoverflow.com/a/14395641/682915
	var  $rows = $("#EX_TIME_DTL\\$scrolli\\$0").find('tr')
		,$projectColumns = $rows.find('td:nth-child(4)')
		,projectRows = [];

	$projectColumns.each(function () {
		//the project numbers have random white-space around them
		this.setAttribute('data-projectID', 
			this.textContent.replace(/^\s\s*/, '').replace(/\s\s*$/, '')); 
	});

	function findProjects (data) {
		data.jobs.forEach(function (jobNumber) {
			var $thisProject = $projectColumns.filter(function () {
				return this.getAttribute('data-projectID') == jobNumber;
			});
			var $input = $thisProject.parent('tr').find(':checkbox');
			$input.prop('checked', !$input.prop('checked'));
			console.log(jobNumber);
		});
		$('#EWW_DERIVED_OK_PB').click();
	}

	function validateProjects(data) {
		var errorList = "";
		data.jobs.forEach(function (jobNumber) {
			var hasProject = false;
			$projectColumns.each(function(){
				hasProject = hasProject || this.getAttribute('data-projectID') == jobNumber;
			});
			if (hasProject == false){
				errorList += "<li>Job "+jobNumber+" required.</li>";
			}
		});
		if (errorList == "") {
			errorList = "<li>All projects present</li>";
		}
		$("#validationResults").append(errorList)
		console.log("<ul>"+errorList+"</ul>");
	}

	var END_DATE = '2015-05-31';
	var API_KEY = '3c0de9ddaf96d8562f6288df46d75525';

	console.log(localStorage["togglApiKey"])

	$.getJSON("https://vees.net/apps/toggl/"+API_KEY+"/"+END_DATE+"/", validateProjects);
}

document.getElementById("validateJobs").addEventListener("click", onValidateButtonPush);
console.log('goodbye');

