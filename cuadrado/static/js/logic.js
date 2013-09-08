function showAccFinanForm(){

	
}
function loadSearchGroupNames(){
	var colors = ["red", "blue", "green", "yellow", "brown", "black"];
	  $('#serchGroupField').typeahead({
		    source: function (query, process) {
		        return $.get('/typeaheadGroup/', { query: query }, function (data) {
		            return process(data.options);
		        });
		    }
		});
}

$(document).ready(function() {
	$(function () {
	    $('#showAccFinForm').popover({ 
	    	html : true, 
	    	content: function() {
	    	      return $('#popover_content_wrapper').html();
	    	    }



	    	});
	});
	
	
	hideFinancialConfig();
	loadSearchGroupNames();
	});

function hideFinancialConfig(){
//	if(component.checked == "checked"){
		$("#creditContainer").hide();
//	}
}
function showFinancialConfig(){
//	if(component.checked == "checked"){
		$("#creditContainer").show();
//	}
}

function closePopover(){
	
	$('#showAccFinForm').popover('hide');
}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}

function isSpending(){
	$('#transType').val("isSpending");
}
function isDeposit(){
	$('#transType').val("isDeposit");
}
