$(document).on('click', '[data-toggle="lightbox"]', function(event) {
	event.preventDefault();
	console.log('IMG')
	$(this).ekkoLightbox();
});