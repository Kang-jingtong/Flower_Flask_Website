$(document).ready(function timer(){
		
		var progressIn = $('#progress_in');
		var deltaMinute = $('#deltaMinute').html();
		console.log(deltaMinute);
		
		var width = 0;
		let time = deltaMinute.replace("<p>","");
		time = time.replace("</p>","");
		
		if(time != ""){
			difference = parseInt(time);
			console.log("time: " + time);
			let isTimeOut = false;
			
			// 1. get the time now
			var date = new Date();
			var start = date.getTime()/(1000*60);
			console.log(start);
			//$('#progress_in').css("width", '10%');
			// 2. get the difference
			while(!isTimeOut){
				date = new Date();
				if(date.getTime()/(1000*60) - start >= difference){
					isTimeOut = true;
				}
				
				width = (date.getTime()/(1000*60) - start)/difference;
				
				$('#progress_in').css("width", "1-width");
				
				
				console.log(width);
				}
		}
		else{
		console.log("the time is empty")
		}
	});
	 