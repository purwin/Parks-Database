$( document ).ready(function() {


  var model = {

    // Object prototype for table objects (exhibition, artwork, artist, org)
    Obj: function(arg) {

      // Declare object name
      this.name = arg;

      // Declare object DIV ID
      this.div = {
        id: "#js-div_" + arg
      },

      // Declare object LI class and HTML
      this.li = {
        class: ".js-li_" + arg,
        html:  $('#js-template_' + arg).html()
      },

      // Declare class names for object children (exhibition.artworks, etc.)
      this.children = {
      },

      this.datalist = 'js-datalist_' + arg,

      // Declare object modal ID and body HTML
      this.modal = {
        id: "#js-modal_" + arg, // modal ID ref
        html: $('#js-form_' + arg).html(),
      },

      // Declare IDs for object form and object modal form
      this.form = {
        id: "#js-form_" + arg,
        modalID: "#js-form-modal_" + arg
      },

      // Declare action route for AJAX POST functions
      this.post = "/" + arg + "s/create"
    },


    // Currently showing IDs, but remove ULs and update IDs to empty strings
    // that get actual html refs in the model.init function
    exhibition: {
      name: "exhibition",
      div: {
        id: "#js-div_exhibition"
      },
      ul: {
        class: ".js-ul_exhibition",
        html: ""
      },
      li: {
        class: ".js-li_exhibition",
        html:  $('#js-template_exhibition').html()
      },
      children: {
        "org": ".js-datalist_org",
        "artwork": ".js-datalist_artwork",
        "park": ".js-datalist_park"
      },
      datalist: "js-datalist_exhibition",
      modal: {
        id: "#js-modal_exhibition", // modal ID ref
        html: null, // no exhibition modal at this time
      },
      form: {
        id: "#js-form_exhibition",
        modalID: "#js-form-modal_exhibition"
      },
      postID: "js-post_exhibition",
      post: "/exhibitions/create"
    },


    artwork: {
      name: "artwork",
      div: {
        id: "#js-div_artwork"
      },
      ul: "js-ul_artwork",
      li: {
        class: "#js-li_artwork",
        html: $('#js-template_artwork').html(),
      },
      children: {
        "artist": ".js-datalist_artist"
      },
      datalist: "js-datalist_artwork",
      modal: {
        id: "#js-modal_artwork", // modal ID ref
        html: '<form id="js-form-modal_artwork" action="" method="POST">\n' + $('#js-form_artwork').html() + '</form>\n' // modal body HTML
      },
      modalUL: "js-modal-ul_artwork",
      modalLI: "js-modal-li_artwork",
      form: {
        id: "#js-form_artwork",
        modalID: "#js-form-modal_artwork"
      },
      postID: "js-post_artwork",
      post: "/artworks/create"
    },


    artist: {
      name: "artist",
      div: {
        id: "#js-div_artist"
      },
      ul: "js-ul_artist",
      li: {
        class: ".js-li_artist",
        html: $('#js-template_artist').html(),
      },
      children: {
        "artwork": ".js-datalist_artwork"
      },
      datalist: "js-datalist_artist",
      modal: {
        id: "#js-modal_artist", // modal ID ref
        html: '<form id="js-form-modal_artist" action="" method="POST">\n' + $('#js-form_artist').html() + '</form>\n' // modal body HTML
      },
      modalUL: "js-modal-ul_artist",
      modalLI: "js-modal-li_artist",
      form: {
        id: "#js-form_artist",
        modalID: "#js-form-modal_artist"
      },
      postID: "js-post_artist",
      post: "/artists/create"
    },

    park: {
      name: "park",
      div: {
        id: "#js-div_park"
      },
      ul: "js-ul_park",
      li: {
        count: 0,
        class: ".js-li_park",
        html: $('#js-template_park').html(),
      },
      datalist: "js-datalist_park",
      modal: {
        id: "#js-modal_park", // modal ID ref
        html: '<form id="js-form-modal_park" action="" method="POST">\n' + $('#js-form_park').html() + '</form>\n' // modal body HTML
      },
      modalUL: "js-modal-ul_park",
      modalLI: "js-modal-li_park",
      form: {
        id: "#js-form_park",
        modalID: "#js-form-modal_park"
      },
      postID: "js-post_park",
      post: "/parks/create"
    },


    org: {
      name: "org",
      div: {
        id: "#js-div_org"
      },
      ul: "js-ul_org",
      li: {
        count: 0,
        class: ".js-li_org",
        html: $('#js-template_org').html(),
      },
      datalist: "js-datalist_org",
      modal: {
        id: "#js-modal_org", // modal ID ref
        html: '<form id="js-form-modal_org" action="" method="POST">\n' + $('#js-form_org').html() + '</form>\n' // modal body HTML
      },
      modalUL: "js-modal-ul_org",
      modalLI: "js-modal-li_org",
      form: {
        id: "#js-form_org",
        modalID: "#js-form-modal_org"
      },
      postID: "js-post_org",
      post: "/orgs/create"
    },


    // Declare selected form type
    activeObject: null,

    // Declare list of active createButtons
    createButton: [null],

    init: function() {
      model.exhibition = new model.Obj("exhibition");
      model.artwork = new model.Obj("artwork");
      model.artist = new model.Obj("artist");
      model.park = new model.Obj("park");
      model.org = new model.Obj("org");
    }

  };


  var controller = {

    init: function() {
      // model.init();
      view.init();
    },


    // Get class input type (exhibition, artwork, artist, org)
    determineObject: function(x) {
      var y = x.id.split("_")[1];

      console.log("Selected object type: " + y);

      return y;
    },


    // Set model.activeObject to selected object
    selectActiveObject: function(x) {
      model.activeObject = model[x];

      console.log("New active object:");
      console.dir(model.activeObject);
    },


    // Show section based on user input
    showSection: function(x) {
      // Set active object
      this.selectActiveObject(x);

      // Hide all object DIVs
      $(".js-create-div").hide();

      // Show selected DIV
      $(model[x].div.id).show();

      // Show submit buttons
      $(".js-submit-div").show();
    },


    // Add new LI based on selected button
    appendUL: function(x) {
      // Get object type from argument's ID
      var obj = this.determineObject(x);

      // Append next UL with LI HTML
      $(x).nextAll('ul').append(model[obj].li.html);

    },


    removeLI: function(x) {
      // Get object type from argument's ID
      var obj = this.determineObject(x);

      // Remove parent LI of selected
      $(x).closest("li").remove();
    },


    // Add new modal form
    showModal: function(x) {
      // Add modal ID to array of active modals
      model.createButton.push(x);

      console.log("createbutton: ");
      console.dir(model.createButton);

      // Get object type from argument's ID
      var obj = this.determineObject(x);

      // Show object modal and add object.modal HTML to modal body
      $(model[obj].modal.id).modal('show')
        .find('div.modal-body')
        .html(model[obj].modal.html);
    },


    // Switch datalist values with data-values, passing in form ID
    valSwitch: function(formID) {
      var tempVal, idVal;

      try {
        $(formID + ' [id^="js-datalist_"]').each(function(index) {
          tempVal = $(this).val();
          console.log("Temp val: " + tempVal)
          idVal = $(formID + ' option').filter(function() {
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


    // Update input name value before posting forms for wtforms Fieldlist keys
    iterateFieldlists: function(formID, childClass) {
      // console.log("ITERATE: " + formID + " " + childClass);
      $.each($(formID + " " + childClass), function(index, value) {
          value.name = value.name + '-' + (index + 1);
      });
    },


    // Pop most recent addition to modal list
    popModalList: function() {
      let x = model.createButton.pop();
      console.log("createbutton: ");
      console.dir(model.createButton);
      return x;
    },


    // Remove modal ref from list when a modal is cancelled
    removeModal: function(x) {
      this.popModalList();
    },


    // Post modal form
    submitModal: function(x) {
      // Get object type from argument's ID
      var obj = this.determineObject(x);

      // Call post data function, get response
      var postPromise = this.postData(model[obj], model[obj].form.modalID);

      postPromise.done(function(response) {
        // If form POST doesn't validate with wtforms, add errors to page
        if (response.success == false) {
          console.log("Form Error(s)!");
          console.dir(response);

          // FUTURE: Call addErrors() for each error
        }
        // ...Otherwise, return object sent from POST route
        else {
          console.log("Form Sucess!");
          console.dir(response);
          controller.addSuccess("Success! Created " + response.data.name + "!");

          // Update model object datalist
          model[obj].li.html = controller.updateTemplate(model[obj].li.html, response.data);

          // Set all [obj] datalists to updated model object datalist
          try {
            $('#' + model[obj].name + 's').each(function(index) {
              $(this).append('<option data-value="' + response.data.id + '" value="' + response.data.name + '"></option>');
            });
          }
          catch (e) {
            console.log("Catch: " + e);
          }

          // FUTURE: Add empty LI

          // FUTURE: Select LI input value to created object

          // Hide modal
          view.closeModal();

        }

      }).fail(function(error) {
        console.log("AJAX error!");
        console.dir(error);
      })

      // FUTURE: get response from postData function
    },


    // Post main form
    submitForm: function(x) {

      console.log("submitForm form ID: " + model.activeObject.form.id);
      console.log("submitForm form post route: " + model.activeObject.post);

      // Call post data function, get response
      var postPromise = this.postData(model.activeObject, model.activeObject.form.id);

      postPromise.done(function(response) {
        // If form POST doesn't validate with wtforms, add errors to page
        if (response.success == false) {
          console.log("Form Error(s)!");
          console.dir(response);

          // FUTURE: Call addErrors() for each error
        }
        // ...Otherwise, reload page
        else {
          console.log("Form Sucess!");
          console.dir(response);
          controller.addSuccess("Success! Created " + response.data.name + "!");

          // Update model object datalist
          model[obj].li.html = controller.updateTemplate(model[obj].li.html, response.data);

          // Set all [obj] datalists to updated model object datalist
          try {
            $('#' + model[obj].name + 's').each(function(index) {
              $(this).append('<option data-value="' + response.data.id + '" value="' + response.data.name + '"></option>');
            });
          }
          catch (e) {
            console.log("Catch: " + e);
          }

        }
      });
    },


    // Post form
    postData: function(obj, formID) {

      console.log("Form ID: " + formID);

      // Change selected datalist values to IDs for adding via SQLAlchemy
      this.valSwitch(formID);

      // For each object child class (artwork.artists, exhibition.orgs, etc.),
      // add number suffix for wtforms Datalist
      for (child in obj.children) {
        this.iterateFieldlists(formID, obj.children[child]);
      }

      console.log("Post data: " + $(formID).serialize());

      console.log("Post route: " + obj.post);

      // Post data
      return $.ajax({
        url: obj.post,
        data: $(formID).serialize(),
        type: 'POST'
      });

    },


    retrieveResponse: function(response) {

    },


    // Add form/AJAX errors to page
    addErrors: function(errors) {
      // FUTURE
    },


    // Add success message to page
    addSuccess: function(message) {
      // Create temporary DIV
      var div = $('<div/>');

      // Add success template HTML to DIV, add success message to inner DIV
      $(div).html($('#js-template_success').html()).find('.js-success-message').append(message);

      // Add new DIV to body
      $('body').append($(div).html());
    },


    // Add created object (artwork, artist, org) to LI options
    addCreatedItem: function(item) {
      // FUTURE

      // FUTURE: Call selectCreatedItem() to add item to page
    },


    // Add value of created object to newest LI
    selectCreatedItem: function(x) {
      // FUTURE
    },


    // Update template with created object data from server
    updateTemplate: function(template, update) {
      // Create temp div
      var div = document.createElement("div");

      // Set inner HTML to received LI template
      $(div).html(template);

      // Append template datalist with new object data
      $(div).find('datalist').append('\t<option data-value="' + update.id + '" value="' + update.name + '"></option>')

      // Return template
      return $(div).html();
    }


  };


  var view = {

    // Call all view functions
    init: function() {
      this.hideDivs();

      this.selectForm();

      this.addLI();

      this.deleteLI();

      this.createModal();

      this.cancelModal();

      this.postForm();

      this.postModal();
    },


    hideDivs: function() {
      // Hide all object DIVs
      $(".js-create-div").hide();

      // Hide submit buttons
      $(".js-submit-div").hide();
    },


    // Determine active form based on input type
    selectForm: function() {
      $('#js-create_object').change(function(e) {

        // Call controller function to show object section based on user input
        controller.showSection($(this).val());
      });
    },


    // Add click listener to .js-add-li buttons to add LI to parent UL
    // TARGET CLASS: .js-add-li
    // GET ID EXAMPLE: .js-add_artist
    addLI: function() {
      $('body').on('click', '.js-add-li', function(e) {
        e.preventDefault();

        // Call controller function to add LI to parent UL of selected button
        controller.appendUL(this);
      });
    },


    // Add click listener to .js-delete-li buttons to remove parent LI
    // TARGET CLASS: .js-delete-li
    // GET ID EXAMPLE: .js-delete_artist
    deleteLI: function() {
      $('body').on('click', '.js-delete-li', function(e) {
        e.preventDefault();

        // Remove parent LI of selected button
        $(this).closest("li").remove();

      });
    },


    // Add click listener to .js-create-modal buttons to create and show modal
    // TARGET CLASS: .js-create-modal
    // GET ID EXAMPLE: .js-create_artist
    createModal: function() {
      $('body').on('click', '.js-create-modal', function(e) {
        e.preventDefault();

        // Call controller function to show modal
        controller.showModal(this);
      });
    },


    // Close modal, using Bootstrap's hide.bs.modal call
    // Accounts for all variations of closing a modal
    cancelModal: function() {
      $('.modal').on('hide.bs.modal', function (e) {

        console.log("Removing modal!");

        // Call controller function to cancel modal POST and remove modal
        controller.removeModal(this);
      });
    },


    closeModal: function() {
      // Close modal
      $('.modal').modal('hide');

      // Call controller function to cancel modal POST and remove modal
      controller.removeModal(this);
    },


    // Add click listener to .js-post-modal buttons to post modal forms via AJAX
    // TARGET CLASS: .js-post-modal
    // GET ID EXAMPLE: .js-post_artist
    postModal: function() {
      $('body').on('click', '.js-post-modal', function(e) {
        e.preventDefault();

        // Call controller function to POST data via AJAX
        controller.submitModal(this);
      });
    },


    // Add click listener to .js-post-form buttons to post forms via AJAX
    // TARGET CLASS: .js-post-form
    // GET ID EXAMPLE: .js-post_artist
    postForm: function() {
      $('body').on('click', '.js-post-form', function(e) {
        e.preventDefault();

        // Call controller function to POST data via AJAX
        controller.submitForm(this);
      });
    }


  };

  controller.init();

});
