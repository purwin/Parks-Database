$( document ).ready(function() {
var model = {

	// add artwork/park combo to exhibition
	artAdd: "<li><select id='' name='exh_art' class=''>\
		<option value='' disabled selected>Artwork</option>\
		{% for artwork in artworks %}<option value='{{ artwork.id }}'>{{ artwork.name }}</option>{% endfor %}</select>\
		 @ <select id='' name='exh_park' class=''><option value='' disabled selected>Park</option>\
		 {% for park in parks %}<option value='{{ park.id }}'>{{ park.name }}</option>{% endfor %}</select></li>",

	// add artist to an artwork
	artistAdd: "<li>Artist <input type='text' id='' name='art_artist' class='' list='artists'><datalist id='artists'>\
		{% for artist in artists %}\
		<option data-value='{{ artist.id }}' value='{% if artist.fName %}{{ artist.fName }} {% endif %}{{ artist.pName }}'></option>\
		{% endfor %}\
		</datalist></li>",

	artistAddModal: "",

	// add org to exhibition
	orgAdd: "<li><select id='' name='exh_org' class=''><option value='' disabled selected>Organization</option>\
		{% for org in orgs %}<option value='{{ org.id }}'>{{ org.name }}</option>{% endfor %}\
		</select></li>",

	// create artwork modal form
	artCreate: "<form id='form_art'>\
		<ul class='ul_art'>\
		<li><label for='artwork_name'>Name</label> <input type='text' name='artwork_name'></li>\
		<li><label for='art_artist'>Artist</label> <input type='text' id='' name='art_artist' class='' list='artists'>\
		<datalist id='artists'>\
		</datalist>\
		<button type='button' class='artistCreate btn-add' data-toggle='modal' data-target='#modal_artistCreate'>Create</button>\
		<button type='button' id='artistAddModal' class='artist_add btn-edit'>+</button>\
		</li>\
		</ul>\
		</form>",

	// create artist modal form
	artistCreate: "<form id='form_artist'>\
		<ul class='ul_artist'>\
		<li><label for='artist_pName'>Name</label> <input type='text' name='artist_pName' placeholder='primary/last name'> <input type='text' name='artist_fName' placeholder='first name'></li>\
		<li><label for='artist_email'>Email</label> <input type='text' name='artist_email'></li>\
		<li><label for='artist_phone'>Phone</label> <input type='text' name='artist_phone'></li>\
		<li><label for='artist_website'>Website</label> <input type='text' name='artist_website'></li>\
		</ul>\
		</form>",

	// create org modal form
	orgCreate: "<form id='form_org'>\
		<ul class='ul_org'>\
		<li><label for='org_name'>Name</label> <input type='text' name='org_name'></li>\
		<li><label for='org_website'>Website</label> <input type='text' name='org_website'></li>\
		<li><label for='org_phone'>Phone</label> <input type='text' name='org_phone'></li>\
		</ul>\
		</form>"

};

var controller = {
	init: function(){
		view.init();
		model.artistAddModal = $('.art_artists ul.ul_artist').html();
	},

	// add new [artAdd|artistAdd|orgAdd] li
	appendUL: function(x){
		$(x).parents('ul').append(model[x.id]);
		console.log(x.id);
		var data = {}; 
		$("#try_it option").each(function(i,el) {  
		   data[$(el).data("value")] = $(el).val();
		});
		// `data` : object of `data-value` : `value`
		console.log("DATA: " + data, $("#try_it option").val());
		console.log("Value: " + $('#try_it').val());
		console.log("Data Value: " + $('#artists [value="' + $('#try_it').val() + '"]').data('value'));
	},

	// add new [artCreate|artistCreate|orgCreate] modal form
	showModal: function(x){
		$('#modal_' + x).modal('show').find('div.modal-body').html(model[x]);
		console.log("Last-child: " + $('ul.ul_art li:last-child option:selected').val());
	},

	postArtist: function(){
		console.log($('#form_artist').serialize());
		$.ajax({
			url: '/createArtist',
			data: $('#form_artist').serialize(),
			type: 'POST',
			success: function(response) {
				console.log("Response: " + response);
				console.log("ID: " + response.id);
				console.log("Primary Name: " + response.pName);
				console.log("First Name: " + response.fName);
				if ($('#modal_artCreate').hasClass('show')) {
					// add artist row in modal with response info so it's added to exhibition
					// controller.appendUL('#artistAddModal');
					model.artistAddModal = model.artistAddModal + "<li>Added!!</li>";
					$('#artistAddModal').parents('ul').append(model.artistAddModal);
					// $('#artistAddModal').parents('ul li:last-child select').val("Tanya Harding");
					console.log($('ul.ul_art li:last-child').html());
					console.log($('#artistAddModal').parents('ul li').last().val());
				} else {
					// add artist row with response info so it's added to artwork
					console.log('NO CLASS!');
					controller.appendUL('#artistAdd');
					$('#artistAdd').parents('ul li:last-child select').val(response.pName + " " + response.fName);
				//	$('.art_artists').children('ul').append("<li>Artist <input type='text' id='' name='art_artist' class='' list='artists'><datalist id='artists'>{% for artist in artists %}<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>{% endfor %}</datalist></li>");
				}

		    },
		    error: function(error) {
				console.log(error);
			}
		});
		$('#modal_artistCreate').modal('hide');
		// $('#modal_artist .modal-body').html(artistForm);
	},

	postArtwork: function(){
		$.ajax({
			url: '/createArtwork',
			data: $('#form_art').serialize(),
			type: 'POST',
			success: function(response) {
				console.log("Response: " + response);
				console.log("ID: " + response.id);
				console.log("Art Name: " + response.name);
				model.artAdd = response;
				$('#artistAddModal').parents('ul').append(model.artAdd);

				if ($('#modal_artCreate').hasClass('show')) {
					// add artist row in modal with response info so it's added to exhibition
					// controller.appendUL('#artistAddModal');
					model.artistAddModal = model.artistAddModal + "<li>Added!!</li>";
					$('#artistAddModal').parents('ul').append(model.artistAddModal);
					// $('#artistAddModal').parents('ul li:last-child select').val("Tanya Harding");
					console.log($('ul.ul_art li:last-child').html());
					console.log($('#artistAddModal').parents('ul li').last().val());
				} else {
					// add artist row with response info so it's added to artwork
					console.log('NO CLASS!');
					controller.appendUL('#artistAdd');
					$('#artistAdd').parents('ul li:last-child select').val(response.pName + " " + response.fName);
				//	$('.art_artists').children('ul').append("<li>Artist <input type='text' id='' name='art_artist' class='' list='artists'><datalist id='artists'>{% for artist in artists %}<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>{% endfor %}</datalist></li>");
				}

		    },
		    error: function(error) {
				console.log(error);
			}
		});
		$('#modal_artistCreate').modal('hide');
		// $('#modal_artist .modal-body').html(artistForm);
	}
	//plus button
	//create button
	//send button
	//reset modal
};

var view = {
	init: function(){
		this.addSelection();
		this.modal();
		this.postCreate();

	},
	//render new ul
	//render new modal

	// + button used to add new artwork / artist / org
	addSelection: function(){
		$('body').on('click', '.art_add, .artist_add, .org_add', function(event) {
			event.preventDefault();
			controller.appendUL(this);
			console.log("THIS: " + this.classList);
		});
	},

	//show artist modal
	modal: function(){
		$('body').on('click', '.artCreate, .artistCreate, .orgCreate', function(event) {
			event.preventDefault();
			var createType = (this.className.split(' ')).filter(function(index){
				return index.includes('Create');
			});
			console.log("X: " + String(createType));
			//'[class~=Create]');
			controller.showModal(createType[0]);
		});
	},

	//new artwork modal create button
	postCreate: function(){
		$('body').on('click', '#modal_add_artist', function(event) {
			console.log("Run the thing! " + $('#modal_add_artist').attr('id'));
			event.preventDefault();
			controller.postArtist();
			$('#modal_artistCreate').modal('hide');
		});
	},

	// testo: function(){
	// 	$('body').on('click', '.btn-add', function(event) {
	// 		console.log("Body clicked!");
	// 		console.log($('#modal_add_artist').attr('class'));
	// 	});
	// },

	oldWay: function(){
		$('#modal_add_artist').on('click', function(event) {
			event.preventDefault();
			$.ajax({
				url: '/createArtist',
				data: $('#form_artist').serialize(),
				type: 'POST',
				success: function(response) {
					console.log("Response: " + response);
					console.log("ID: " + response.id);
					if ($('#modal_art').hasClass('show')) {
						// add artist row in modal with response info so it's added to exhibition
					} else {
						// add artist row with response info so it's added to artwork
						
					//	$('.art_artists').children('ul').append("<li>Artist <input type='text' id='' name='art_artist' class='' list='artists'><datalist id='artists'>{% for artist in artists %}<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>{% endfor %}</datalist></li>");
					}

			    },
			    error: function(error) {
					console.log(error);
				}
			});
			$('#modal_artist').modal('hide');
			$('#modal_artist .modal-body').html(artistForm);
		});
	}

};

controller.init();
});

/*
$( document ).ready(function() {
	// controller.init();

	// on New [...] change
	$('#create_type').change(function() {
//				$('.create_div').hide();
//			    $('#create_' + $('#create_type').val()).show();
	    $('.form_submit').show();
	});

	//show artwork modal
	$('.art_create').on('click', function(event) {
		event.preventDefault();
		$('#modal_art').modal('show');
	});

	//new artwork modal create button
	$('#modal_add_artwork').on('click', function(event) {
		event.preventDefault();
		console.log('clicked');
		$('#modal_art').modal('hide');
	});

	//artist modal form
	var artistForm = "<form id='form_artist'>\
	<ul>\
	<li>Name <input type='text' name='artist_pName' placeholder='primary/last name'> <input type='text' name='artist_fName' placeholder='first name'></li>\
	<li>Email <input type='text' name='artist_email'></li>\
	<li>Phone <input type='text' name='artist_phone'></li>\
	<li>Website  <input type='text' name='artist_website'></li>\
	</ul>\
	</form>"

	//show artist modal
	$('.artist_create').on('click', function(event) {
		event.preventDefault();
		$('#modal_artist').modal('show');
	});

	//new artwork modal create button
	$('#modal_add_artist').on('click', function(event) {
		event.preventDefault();
		$.ajax({
			url: '/createArtist',
			data: $('#form_artist').serialize(),
			type: 'POST',
			success: function(response) {
				console.log("Response: " + response);
				console.log("ID: " + response.id);
				if ($('#modal_art').hasClass('show')) {
					// add artist row in modal with response info so it's added to exhibition
				} else {
					// add artist row with response info so it's added to artwork
					
				//	$('.art_artists').children('ul').append("<li>Artist <input type='text' id='' name='art_artist' class='' list='artists'><datalist id='artists'>{% for artist in artists %}<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>{% endfor %}</datalist></li>");
				}

		    },
		    error: function(error) {
				console.log(error);
			}
		});
		$('#modal_artist').modal('hide');
		$('#modal_artist .modal-body').html(artistForm);
	});
	

	// on artist modal 'add' click, reset modal html

	// add artwork selection
	$('.art_add').on('click', function(event) {
		event.preventDefault();
		$(this).parents('ul').append("<li><select id='' name='exh_art' class=''>\
			<option value='' disabled selected>Artwork</option>\
			{% for artwork in artworks %}<option value='{{ artwork.id }}'>{{ artwork.name }}</option>{% endfor %}</select>\
			 @ <select id='' name='exh_park' class=''><option value='' disabled selected>Park</option>\
			 {% for park in parks %}<option value='{{ park.id }}'>{{ park.name }}</option>{% endfor %}</select></li>");
	});

	// add artist selection
	$('.artist_add').on('click', function(event) {
		event.preventDefault();
		console.log($(this).parents('ul').get(0).className);
		$(this).parents('ul').append("<li>Artist <input type='text' id='' name='art_artist' class='' list='artists'><datalist id='artists'>\
			{% for artist in artists %}\
			<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>\
			{% endfor %}\
			</datalist></li>");
	});

	// add org selection
	$('.org_add').on('click', function(event) {
		event.preventDefault();
		$(this).parents('ul').append("<li><select id='' name='exh_org' class=''><option value='' disabled selected>Organization</option>\
			{% for org in orgs %}<option value='{{ org.id }}'>{{ org.name }}</option>{% endfor %}\
			</select></li>");
	});

});
*/