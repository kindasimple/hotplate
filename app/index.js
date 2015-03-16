var photos = [],
	results = {},
	likes = 0,
	dislikes = 0;

$(document).ready(function(){

	//grab the container element
	$content = $("#container")

	//query for a list of photos
	$.ajax({ url: 'http://localhost:8080/venues/photos.json' })
	.done(function (response) {
		photos = response
		loadPhotos(photos)
	})

	//Take a set of photos and populate a tinder-like interface
	function loadPhotos(photos) {

		//now we have a bunch of metadata related to the images, and we need to generate an interface
		photos.forEach(function (photo, index) {
			//Add an image container, with an image inside
			var $container = $('<div>').addClass('buddy')
			if(index == 0) {
				$container.css('display', 'block') //show the first image
			}
			var $image = $('<div>')
				.addClass('avatar')
				.data('id', photo.photoID)
				.css('background-image', 'url(' + photo.thumbnail + ')')
			$container.append($image)
			//detect a right swipe, and fade out when it happens, adding a like indicator to the card as it fades and show the next card

			$content.append($container)
		})

		//when someone swipes left, fade the image out and show the dislike indicator, and show the next card
		$(".buddy").on("swipeleft", swipeLeft);

		$(".buddy").on("swiperight", swipeRight);  
	}

	function swipeLeft () {
		$(this).addClass('rotate-right').delay(700).fadeOut(1);
		$('.buddy').find('.status').remove();
		$(this).append('<div class="status dislike">Dislike!</div>');

		if ( $(this).is(':last-child') ) {
			$('.buddy:nth-child(1)').removeClass ('rotate-left rotate-right').fadeIn(300);
			alert('Na-na!');
		} else {
			$(this).next().removeClass('rotate-left rotate-right').fadeIn(400);
		}

		addDislike($(this).data("id"))
	}

	function swipeRight () {
		$(this).addClass('rotate-left').delay(700).fadeOut(1);
		$('.buddy').find('.status').remove();

		$(this).append('<div class="status like">Like!</div>');      
		if ( $(this).is(':last-child') ) {
			$('.buddy:nth-child(1)').removeClass ('rotate-left rotate-right').fadeIn(300);
		} else {
			$(this).next().removeClass('rotate-left rotate-right').fadeIn(400);
		}
		addLike($(this).data("id"))  	
	}

	function addLike(id) {
		$('.likes').text(++likes)
		results[id] = true;
		$.ajax('http://localhost:8080/vote/like')
	}
	
	function addDislike(id) {
		$('.dislikes').text(++dislikes)
		results[id] = false
		$.ajax('http://localhost:8080/vote/dislike')
	}
});
