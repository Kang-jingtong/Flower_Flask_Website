$(document).ready(function(){
	console.log('adding event handlers');
	$('#email1').on('change',check_username);
	console.log('function registered');
});

function check_username(){
	console.log('check_username called');
	var chosen_user = document.getElementById("email1").value;
	console.log('user chose: ' + chosen_user);
	
	$('#checkuser').removeClass();
	var re = /^1[345678]\d{9}$/;
	
	if(re.test(chosen_user)){
		$('#checkuser').html("<progress></progress>");
	
		// ajax
		$.post('registerCheckPhoneNumber',{
			'email': chosen_user
		}).done(function(response){
			console.log("line 19")
			var server_response = response['text'];
			var server_code = response['returnvalue'];
			
			if(server_code == 0){
				$('#password1').focus();
				$('#checkuser').html(server_response);
				$('#checkuser').addClass('success');
			}
			else{
				$('#email1').focus();
				$('#checkuser').html(server_response);
				$('#checkuser').addClass('failure');
				
			}
		}).fail(function(){
			$('#checkuser').html("Error");
			$('#checkuser').addClass("failure");
		});
	}
	else{
		$('#checkuser').html("Check your phone number format");
		$('#checkuser').addClass("failure");
	}
	
	
	
}