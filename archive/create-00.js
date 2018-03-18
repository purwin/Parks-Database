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
		<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>\
		{% endfor %}\
		</datalist></li>",

	// add org to exhibition
	orgAdd: "<li><select id='' name='exh_org' class=''><option value='' disabled selected>Organization</option>\
		{% for org in orgs %}<option value='{{ org.id }}'>{{ org.name }}</option>{% endfor %}\
		</select></li>",

	// create artwork modal form
	artCreate: "<form>\
		<ul>\
		<li><label for='artwork_name'>Name</label> <input type='text' name='artwork_name'></li>\
		<li><label for='art_artist'>Artist</label> <input type='text' id='' name='art_artist' class='' list='artists'>\
		<datalist id='artists'>\
		{% for artist in artists %}\
		<option data-value='{{ artist.id }}' value='{{ artist.name }}'></option>\
		{% endfor %}\
		</datalist>\
		<button type='button' class='artistCreate btn-add' data-toggle='modal' data-target='#modal_artistCreate'>Create</button>\
		<button type='button' id='artistAdd' class='artist_add btn-edit'>+</button>\
		</li>\
		</ul>\
		</form>",

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
		</form>"

};

var controller = {
	init: function(){
		view.init();
	},

	// add new [artAdd|artistAdd|orgAdd] li
	appendUL: function(x){
		$(x).parents('ul').append(model[x.id]);
	},

	// add new [artCreate|artistCreate|orgCreate] modal form
	showModal: function(x){
		$('#modal_' + x).modal('show').find('div.modal-body').html(model[x]);
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

	},
	//render new ul
	//render new modal

	// + button used to add new artwork / artist / org
	addSelection: function(){
		$('.art_add, .artist_add, .org_add').on('click', function(event) {
			event.preventDefault();
			controller.appendUL(this);
		});
	},

	//show artist modal
	modal: function(){
		$('.artCreate, .artistCreate, .orgCreate').on('click', function(event) {
			event.preventDefault();
			var createType = (this.className.split(' ')).filter(function(index){
				return index.includes('Create');
			});
			console.log("X: " + String(createType));
			//'[class~=Create]');
			controller.showModal(createType[0]);
		});
	}

};

controller.init();
});