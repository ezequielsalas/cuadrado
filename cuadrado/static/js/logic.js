function showAccFinanForm(){

	
}
/*
function (query, process) {
    return $.get('/typeaheadGroup/', { query: query }, function (data) {
        return process(data.options);
    });
}
*/
function loadSearchGroupNames(){
	var colors = ["red", "blue", "green", "yellow", "brown", "black"];
	
	$.get('/typeaheadGroup/', {}, function (data) {
       
		available = data.split(',');
		
		$('#serchGroupField').typeahead({
			  source:available
			});
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
    if (charCode > 31 && (charCode < 48 || charCode > 57)){
    	//add two exceptions
    	if(charCode == 44 || charCode == 46){
    		return true;
    	}
    	return false;
    }
    return true;
}

function isSpending(){
	$('#transType').val("isSpending");
}
function isDeposit(){
	$('#transType').val("isDeposit");
}
function showFieldIfFill(trigger,target){
	if($(trigger).val()!=""){
		
		$("#"+target).show();
		
	}else{
	
		$("#"+target).hide();
	}
}