$(document).ready(function(){

	// ===========================================================
	// ---------- Navbar moves as we scroll down ------------start
	// ===========================================================
 	$(window).on('scroll', fixHeader);
		var header = $('nav');
		var headerOffset = header.offset().top;
		function fixHeader(evt){
			var currentScroll = $(window).scrollTop()
			// console.log(headerOffset, currentScroll);
			if(headerOffset <= currentScroll){
				header.addClass('navbar-fixed-top').css({"right":"10px","left":"10px"});
			}
			else {
			 header.removeClass('navbar-fixed-top')
			}
		}	
	// ===========================================================
	// ---------- Navbar moves as we scroll down ------------ends
	// ===========================================================


	// ===================================================================================
	// Div slide in and visible when scroll with arguments, Left, Right & Speed -----start
	// Reuseable Function
	// ===================================================================================
	
	// Define variables globally so variable scope will be beyond any particular function

	var windowHeight = $(window).height();
	var windowScrollPositionTop = $(window).scrollTop();
	var windowScrollPositionBottom = windowHeight + windowScrollPositionTop;

	$.fn.revealOnScroll = function(direction, speed){
		return this.each(function(){

			var objectOffset = $(this).offset();
			var objectOffsetTop = objectOffset.top;

			// we need to run this code only once we scroll
			// Do NOT use hidden class if your are using Bootstrap, name something else like "closed"
			if (!$(this).hasClass("closed")){

				// Run the code by checking it's direction
				if (direction == "right"){
					$(this).css({
						"opacity" : 0,
						"right"	  : "700px",
						"position": "relative"
					});
				} else if (direction == "left"){
					$(this).css({
						"opacity" : 0,
						"right"	  : "-700px",
						"position": "relative"
					});
				} else {
					$(this).css({
						"opacity" : 0						
					});
				}

				$(this).addClass("closed");
			} //------checking direction ends
			
			// we don't want the code to be keep running after animation is completed
			if(!$(this).hasClass("animation-complete")){
				if(windowScrollPositionBottom > objectOffsetTop){
					$(this).animate({"opacity":1, "right":0}, speed).addClass("animation-complete");
				}
			}
		});

	} //function ends

	// #step 1: hide the content
	//$(".main-container").css({"opacity":0})
	$(window).scroll(function(){

		windowHeight = $(window).height();
		windowScrollPositionTop = $(window).scrollTop();
		windowScrollPositionBottom = windowHeight + windowScrollPositionTop;
	
		// #step 2: Calling revealOnScroll()
		// close if for later $(".main-container").revealOnScroll("right",5000);

		// Calling revealOnScroll() with arguments, Left, Right & Speed
		// $(".about").revealOnScroll("left", 2000);
		// $(".about2").revealOnScroll("right",2000);
		// $(".about3").revealOnScroll("left",2000);

	});

	// ===============================================
	// Div slide in and visible when scroll ------ends
	// ===============================================


	// ===============================================
	// Heading animation-------------------------start
	// ===============================================

	setInterval(function(){
		$(".main-heading").fadeOut(1000).fadeIn(1000);
	},1000);
	
	// ===============================================
	// Heading animation--------------------------ends
	// ===============================================

	// ===============================================
	// Dashboard Status $Ajax calls--------------start
	// ===============================================

	var status = $("#status");
	var statusContainer = $(".status-container");
	statusContainer.hide();
	$("#draft-post,#future-post,#create-post").click(function(e){
		$(".create-container").hide()
		var url = $(this).attr("data-href");

		$.get(url,function(data){
			$("#content-display").html(data);

			if((e.target.id) == "draft-post"){
				status.text("Draft Posts");
				statusContainer.show();
			} else if((e.target.id) == "future-post"){
				status.text("Future Posts");
				statusContainer.show();
			
			} 
			
		});
	});

	// ===============================================
	// Dashboard Status $Ajax calls---------------Ends
	// ===============================================

	// ================================================================
	// Post Create Form $Ajax & Disable Blank submit--------------Start
	// ================================================================


	var createContainer = $(".create-container");
	var createPostForm = $("form#create-post-form");
	var submitBtn = $("#submit-btn");

	createContainer.hide()
	$("#create-post").click(function(){
		$("#status").text("Create New Post")
		createContainer.show();

		// Disable submit button if form is blank ------------>Start

		submitBtn.attr("disabled",true); 
		$("#id_title,#id_content,#id_publish").keyup(function(){
			$("#id_title,#id_content,#id_publish").each(function(){
				if($(this).val().length !=0){
					submitBtn.attr("disabled",false);
				}
				else{
					submitBtn.attr("disabled",true);
				}
			});
		});
		// Disable submit button if form is blank ------------>End
		
		createPostForm.submit(function(e){
			// redirect_path = $(this).attr("redirect"); ------> if need to redirect some other page
			// e.preventDefault();
			var data = new FormData(createPostForm.get(0));

			$.ajax({
				url:$(this).attr("action"),
				method:"POST",
				data:data,
				processData:false,
				contentType:false,
				success:function(response){
					// console.log(response[0]['fields']['user']);
					$("#content-display").html(response);
					$("#status").text("New Post Seccessfully Created.");
					createPostForm.trigger("reset");
					submitBtn.attr("disabled",true);
					// redirect path
					// window.location.assign(redirect_path);------> if need to redirect some other page	
				},
				error:function(response){
					alert(response);
				}				
			});
			return false;			
		});		
	});

	// ================================================================
	// Post Create Form $Ajax & Disable Blank submit---------------ends
	// ================================================================

	// ====================================
	// Back to the top function ------start
	// ====================================
	
	$(window).scroll(function(){

		var $backtotop = $('#backtotop')
		
		if ($(this).scrollTop()){
			$backtotop.fadeIn();
			$backtotop.click(function(){
				$(window).scrollTop(0);
			});
		} else {
			$backtotop.fadeOut();
		}
	});

	// ====================================
	// Back to the top function ------ends
	// ====================================

	// ========================================
	// Ajax call for update comments -----start
	// ========================================
	$("#comment-form").submit(function(e){
		e.preventDefault();
		var url=$(this).attr("action");
		console.log(url);
		$.ajax({
			url:url,
			method:"POST",
			dataType:"json",
			data:$(this).serialize(),
			success:function(response){
				var newComment =('<div><blockquote><p>'+response[0].fields.content+'</p><footer>via '
					+ response[0].fields.user+' | '+ response[0].fields.timestamp +' ago</footer></blockquote><hr></div>')

				// use prepend instead of append as it will show last entry at first row
				$("#new_comment").prepend(newComment);
				
			},
			error:function(response){
					alert("Error: Please try again...!!!");
			}

		});
	});

	// ========================================
	// Ajax call for update comments ------ends
	// ========================================


});
// ----------document. ready() ends here -----------



























