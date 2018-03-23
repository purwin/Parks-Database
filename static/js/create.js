$( document ).ready(function() {
var model = {

	// add artwork/park combo to exhibition: $('.exh_artworks ul#exh_art_list').html();
	artAdd: "",

	// add artist to an artwork: 
	artistAdd: "",

	// add artist to artwork modal: 
	artistAddModal: "",

	// add org to exhibition
	orgAdd: "",

	// create artwork modal form
	artCreate: "",

	// create artist modal form
	artistCreate: "<form id='form_artist'>\
		<ul>\
		<li><label for='artist_pName'>Name</label> <input type='text' name='artist_pName' placeholder='primary/last name'> <input type='text' name='artist_fName' placeholder='first name'></li>\
		<li><label for='artist_email'>Email</label> <input type='text' name='artist_email'></li>\
		<li><label for='artist_phone'>Phone</label> <input type='text' name='artist_phone'></li>\
		<li><label for='artist_website'>Website</label> <input type='text' name='artist_website'></li>\
		</ul>\
		</form>",

	// create org modal form
	orgCreate: "<form id='form_org'>\
		<ul>\
		<li><label for='org_name'>Name</label> <input type='text' name='org_name'></li>\
		<li><label for='org_website'>Website</label> <input type='text' name='org_website'></li>\
		<li><label for='org_phone'>Phone</label> <input type='text' name='org_phone'></li>\
		</ul>\
		</form>",

	init: function() {
		this.artAdd = $('.exh_artworks ul#exh_art_list').html();
		this.artistAdd = $('.art_artists ul.ul_artist').html();
		this.artistAddModal = this.artistAdd;
		this.orgAdd = $('#create_exhibition ul.ul_org').html();
		this.artCreate = "<form id='form_art'>\
			<ul>\
			<li><label for='artwork_name'>Name</label> <input type='text' name='artwork_name'></li>\
			</ul>\
			<h4>Artists</h4>\
			<button type='button' class='artistCreate btn-add' data-toggle='modal' data-target='#modal_artistCreate'>Create</button>\
			<button type='button' id='artistAddModal' class='artist_add btn-edit'>+</button>\
			<ul class='ul_artist'>" + this.artistAdd + "</ul>\
			</form>";
	}

};

var controller = {
	init: function(){
		model.init();
		view.init();
	},

	// add new [artAdd|artistAdd|orgAdd] li
	appendUL: function(x){
		$(x).next('ul').append(model[x.id]);

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
		this.artworkCreate();

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

	artworkCreate: function(){
		$('body').on('click', '#modal_add_artwork', function(event) {
			event.preventDefault();

			$('#form_art #try_it').each(function(index){
				console.log(index + ": " + $( this ).val());
				var val = $(this).val();
				var xyz = $('#form_art #artists option').filter(function() {
					return this.value == val;
				}).data('value');
				console.log("XYZ: " + xyz);
				$(this).val(xyz);
			});

			$.ajax({
				url: '/createArtwork',
				data: $('#form_art').serialize(),
				type: 'POST',
				success: function(response) {
					console.log("Response: " + response);
					console.log("ID: " + response.id);
					console.log("Name: " + response.name);
				},
				error: function(error){
					console.log(error);
				}
			});
			$('#modal_artCreate').modal('hide');
		});
	}

};

controller.init();
});