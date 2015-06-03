;(function ($, window, document, undefined) {
	var  $rows = $(".PSLEVEL1GRIDWBO .PSLEVEL1GRID").find('tr')
		,$projectColumns = $rows.find('td:nth-child(7)')
		,projectRows = [];

	$projectColumns.each(function () {
		this.setAttribute('data-projectID', this.textContent.replace(/^\s\s*/, '').replace(/\s\s*$/, '')); //the project numbers have random white-space around them
	});

	function findProjects (data) {
		data.jobs.forEach(function (jobNumber) {
			var $thisProject = $projectColumns.filter(function () {
				return this.getAttribute('data-projectID') == jobNumber;
			});
			var $input = $thisProject.parent('tr').find(':checkbox');
			$input.prop('checked', !$input.prop('checked'));
		});
		$('#EWW_DERIVED_OK_PB').click();
	}

	var END_DATE = '2015-05-31';
	var API_KEY = '3c0de9ddaf96d8562f6288df46d75525';

	$.getJSON("https://vees.net/apps/toggl/"+API_KEY+"/"+END_DATE+"/", findProjects);
})(jQuery, window, document);