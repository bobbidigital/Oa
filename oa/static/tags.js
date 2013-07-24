
$(document).ready(function () {
	$(".tags").each(function () 
		{
		    $(this).tagsInput();
		});
	$(".tags").typeahead(
		{ source: function(query, process) {
			return $.get('/api/get_metadata',{ query: query }, function(data) {
				return process(data.options);
			});
		     }
		});
});
