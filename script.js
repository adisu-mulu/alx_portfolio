$(document).ready(function() {
    // Select elements with jQuery
    const $titleRadio = $('input[name="searchBy"][value="title"]');
    const $abstractRadio = $('input[name="searchBy"][value="abstract"]');
    const $inputContainer = $('#inputContainer');
    const $query_button = $('#search_submit_Button');
    

    
    // Event handler for titleRadio
    $titleRadio.on('change', function() {
	if ($titleRadio.is(':checked')) {
	    $inputContainer.html('<input type="text" class="searchTitle" id="query" placeholder="Enter title">');
	    }
    });

    // Event handler for abstractRadio
    $abstractRadio.on('change', function() {
	if ($abstractRadio.is(':checked')) {
	    $inputContainer.html('<textarea id="query" class="searchAbstract" placeholder="Paste abstract here"></textarea>');
	    //$search_query = $('#query');
	}
    });

    // Event handler for search_submit_Button
    $query_button.on('click', function(){
	$search_query = $('#query').val();
	var $search_by = $('input[name="searchBy"]:checked').val();
	// construct an object that will carry the data information
	var data = {
	    search_query: $search_query
	}
	// construct the correct url that will point to the correct endpoint based on the search_by
	if ($search_by == 'title'){
	    url = '/search_by_title';
	}
	if ($search_by == 'abstract'){
	    url = '/search_by_abstract';
	}
	// make an ajax post request that sends the data to the endpoint
	$.ajax({
	    url: url,
	    type: 'POST',
	    data: data,
	    success: function(response){
		// Redirect to a new page with sessionStorage
		
		sessionStorage.setItem('responseMessage', response);
		// Redirect to a new page
		window.location.href = '/results';
	    },
	    error: function(xhr, status, error){
		console.log(error)}
	    
	});
    });



    
});
