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
	
	
	$.get('/typeaheadGroup/', {}, function (data) {
		available = data.split(',');
		$('#serchGroupField').autocomplete({
			  source:available
			});
    });
}
function loadBudgetTranx(){
	$.get('/typeaheadBudget/', {}, function (data) {
		available = data.split(',');
		$('#conceptoTransaccion').autocomplete({
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
	loadBudgetTranx();
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
function disableBudgetTrx(pid){
	$.get('/disableBudgetTrx/', {keyBudget:pid}, function (data) {
		if (data =="NOK"){
			alert("Accion interrumpida");
		}
		if(data == "OK" ){
//			e.preventDefault();
			$('#trx-tr-'+pid).remove();
		}
	});
}