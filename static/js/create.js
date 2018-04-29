$( document ).ready(function() {

// var model = {
// 	topCat: null,
// 	allCats: [
// 		{
// 			name: 'Doug',
// 			clickCount: 0,
// 			img: 'https://visualhunt.com/photos/s/7/eye-cat-pet.jpg',
// 			admin: false
// 		},
// 		{
// 			name: 'Tanya',
// 			clickCount: 0,
// 			img: 'https://cdn.images.express.co.uk/img/dynamic/128/590x/secondary/cats-480738.jpg',
// 			admin: false
// 		},
// 		{
// 			name: 'Pappa Louis',
// 			clickCount: 0,
// 			img: 'http://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg',
// 			admin: false
// 		}

// 	]
// };


var model = {

	art: {
		li: "",
		modal: "",
		post: "createArt"
	},

	artist: {
		li: "",
		modal: "",
		post: "createArtist"
	},

	org: {
		li: "",
		modal: "",
		post: "createOrg"
	},

	// exh: {
	// 	li: "",
	// 	modal: "",
	// 	post: ""
	// },

	// event: {
	// 	li: "",
	// 	modal: "",
	// 	post: ""
	// },

	// contact: {
	// 	li: "",
	// 	modal: "",
	// 	post: ""
	// },

	createButton: [null],

	init: function() {
		this['artist'].li = $('#section--create--art ul.ul_artist').html();
		this['org'].li = $('#section--create--exhibition ul.ul_org').html();
		this['art'].li = $('#section--create--exhibition ul.ul_art').html();

		this['art'].modal = "<form id='form_art'>\
				<div class='row justify-content-center'>\
				<div class='col-10 py-4'>\
				<ul>\
				<li class='row mb-3'>\
				<div class='col text-md-right'>\
				<label for='art_name'>Name</label>\
				</div>\
				<div class='col'>\
				<input type='text' name='art_name' placeholder='Artwork Name' class='form-control'>\
				</div>\
				</li>\
				</ul>\
				</div>\
				<div class='col-md-10'>\
				<h3 class='section__head section__head--modal pb-1 mb-3'>Artists</h3>\
				<p class='d-inline'>Related Artists</p>\
				<button type='button' id='createModal2_artist' class='artist_create btn__parks mb-3' data-toggle='modal' data-target='#modal_artistCreate'>Create</button>\
				<button type='button' id='addModal_artist' class='artist_add btn__parks btn__parks--edit'>+</button>\
				<ul class='ul_artist'>"
				+ this['artist'].li +
				"</ul>\
				</div>\
				</form>";

		this['artist'].modal = "<form id='form_artist'>\
				<ul>\
				<li><label for='artist_pName'>Name</label> <input type='text' name='artist_pName' placeholder='primary/last name'> <input type='text' name='artist_fName' placeholder='first name'></li>\
				<li><label for='artist_email'>Email</label> <input type='text' name='artist_email'></li>\
				<li><label for='artist_phone'>Phone</label> <input type='text' name='artist_phone'></li>\
				<li><label for='artist_website'>Website</label> <input type='text' name='artist_website'></li>\
				</ul>\
				</form>";

		this['org'].modal = "<form id='form_org'>\
				<ul class='pt-3'>\
				<li class='row mb-3'>\
				<div class='col-md-4 text-md-right'>\
				<label for='org_name'>Name</label>\
				</div>\
				<div class='col-md-6'>\
				<input type='text' name='org_name' placeholder='Organization Name' class='form-control'>\
				</div>\
				</li>\
				<li class='row mb-3'>\
				<div class='col-md-4 text-md-right'>\
				<label for='org_website'>Website</label>\
				</div>\
				<div class='col-md-6'>\
				<input type='text' name='org_website' placeholder='www.pizza.org' class='form-control'>\
				</div>\
				</li>\
				<li class='row mb-3'>\
				<div class='col-md-4 text-md-right'>\
				<label for='org_phone'>Phone</label>\
				</div>\
				<div class='col-md-6'>\
				<input type='text' name='org_phone' placeholder='###-###-####' class='form-control'>\
				</div>\
				</li>\
				</ul>\
				</form>";
	}

};

var controller = {
	init: function(){
		model.init();
		view.init();
	},

	// add new li
	appendUL: function(x){
		y = x.id.split("_")[1];
		$(x).nextAll('ul').append(model[y].li);
	},

	// add new modal form
	showModal: function(x){
		model.createButton.push(x);
		console.log("M.c: " + model.createButton);
		y = x.id.split("_")[1];

		$('#modal_' + y).modal('show').find('div.modal-body').html(model[y].modal);
	},

	// switch datalist values with data-values
	valSwitch: function(x){
		let y = x.id.split("_")[1];
		var tempVal, idVal;

		try {
			$('#form_' + y + ' [id^="datalist_"]').each(function(index){
				tempVal = $(this).val();
				console.log("Temp val: " + tempVal)
				idVal = $('#form_' + y + ' option').filter(function() {
					return this.value == tempVal;
				}).data('value');
				console.log("ID val: " + idVal);
				$(this).val(idVal);
			});
		}
		catch (e) {
			console.log("Catch: " + e);
		}
	},

	popModalList: function(){
		let x = model.createButton.pop();
		console.log("Current modalList: " + model.createButton);
		return x;
	},

	cancelPost: function(x){
		this.popModalList();
	},

	// post modal forms
	postData: function(x){
		console.log("WHAT: " + x.id);
		let y = x.id.split("_")[1];

		// store values
		var tempName = $("#form_" + y + " [id^='datalist_'] input[name$='_name']").val(); // store name of input, pass to new li

		// change values
		controller.valSwitch(x);

		// post data
		$.ajax({
			url: '/' + model[y].post,
			data: $('#form_' + y).serialize(),
			type: 'POST',
			success: function(response) {
				console.log("RESPONSE: " + response.data);
				console.log(".li_" + y)
				model[y].li = response.data;
				// $(".li_" + y).html(model[y].li);
		    },
		    error: function(error) {
				console.log(error);
			}
		});

		// // hide post modal
		$('#modal_' + y).modal('hide');

		// // add new li, pop most recent modal from modal array
		this.appendUL(this.popModalList());
		
		// // add stored values
		// $(model.createButton).nextAll('ul').find('.datalist_' + y).last().val(tempName);

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
};

var view = {
	init: function(){
		this.addSelection();
		this.modal();
		this.post();
		this.form_create();
		this.cancelPost();
	},

	// + button used to add new artwork / artist / org
	addSelection: function(){
		$('body').on('click', '.art_add, .artist_add, .org_add', function(event) { // update this to '.add_li'
			event.preventDefault();
			controller.appendUL(this);
		});
	},

	// show artist modal
	modal: function(){
		$('body').on('click', '.art_create, .artist_create, .org_create', function(event) { // update this to '.create_modal'
			event.preventDefault();
			controller.showModal(this);
		});
	},

	cancelPost: function(){
		$('body').on('click', '.post_cancel', function(event) {
			event.preventDefault();
			controller.cancelPost(this);
		});
	},

	// send data via modal
	post: function(){
		$('body').on('click', '.post_data', function(event) {
			event.preventDefault();
			controller.postData(this);
		});
	},

	form_create: function(){
		$('#form_create').submit(function(event) {
			event.preventDefault();
			y = $(this).attr('id').split("_")[1];
			controller.valSwitch(this);
		});
	}

};

controller.init();
});