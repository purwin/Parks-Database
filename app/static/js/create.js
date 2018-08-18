$( document ).ready(function() {

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

	// Declare list of active createButtons
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

		this['artist'].modal = "<form id='form_artist' class='pt-3'>" + $('#section--create--artist ul').parent().html() + "</form>";

		this['org'].modal = "<form id='form_org' class='pt-3'>" + $('#section--create--org ul').parent().html() + "</form>";
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

	// Pop most recent addition to modal list
	popModalList: function(){
		let x = model.createButton.pop();
		console.log("Current modalList: " + model.createButton);
		return x;
	},

	// Remove modal ref from list when a modal is cancelled
	cancelPost: function(x){
		this.popModalList();
	},

	// Post modal forms
	postData: function(x){
		console.log("WHAT: " + x.id);
		let y = x.id.split("_")[1];

		// store values
		var tempName = $("#form_" + y + " [id^='datalist_'] input[name$='_name']").val(); // store name of input, pass to new li

		// change values to IDs
		controller.valSwitch(x);

		console.log("Post data: " + $('#form_' + y).serialize());

		// post data
		$.ajax({
			url: '/' + model[y].post,
			data: $('#form_' + y).serialize(),
			type: 'POST',
			success: function(response) {
				console.log("RESPONSE: " + response.data);
				console.log(".li_" + y)
				model[y].li = response.data;
				$(".li_" + y).html(model[y].li);
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
			$('body').on('click', '#post_create', function(event) {
			event.preventDefault();
			y = $(this).attr('id').split("_")[1];
			controller.valSwitch(this);
			$('#form_create').submit();
		});
	}

};

controller.init();
});