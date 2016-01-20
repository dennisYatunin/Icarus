$('#yes').on('click', function() {
	if (this.checked) {
		$('#delEnt').collapse('show');
		$('#no').attr('disabled', true);
		$('#delEnt').on('shown.bs.collapse', function() {
			$('#no').attr('disabled', false);
		});
	}
});