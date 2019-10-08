import {model} from './model';
import {view} from './view';

export let controller = {

  init: function() {
    view.init();
  },


  // Get class input type (exhibition, artwork, artist, org)
  determineObject: function(x) {
    var y = x.id.split("_")[1];

    return y;
  },


  // Set model.activeObject to selected object
  selectActiveObject: function(x) {
    model.activeObject = model[x];
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

    // Update newest input ID and name attributes
    this.iterateFieldlists(model.activeObject.form.id);
  },


  // Add new LI based on selected button
  appendUL: function(x) {
    // Get object type from argument's ID
    var obj = this.determineObject(x);

    // Define nearest parent UL item to append li to
    let nearestParentUL = $(x).closest('.row').nextAll('ul');

    // Append next UL with LI HTML
    nearestParentUL.append(model[obj].li.html);

    // Update newest input ID and name attributes
    this.iterateFieldlists('#' + $(x).closest('form').attr('id'));
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

    // Get object type from argument's ID
    var obj = this.determineObject(x);

    // Set active object
    this.selectActiveObject(obj);

    // Show object modal and add object.modal HTML to modal body
    $(model[obj].modal.id).modal('show')
      .find('div.modal-body')
      .html(model[obj].modal.html);

    // Update newest input ID and name attributes
    this.iterateFieldlists(model.activeObject.form.modalID);
  },


  // Switch datalist values with data-values, passing in form ID
  valSwitch: function(formID) {
    var tempVal, idVal;

    try {
      $(formID + ' [id^="js-datalist_"]').each(function(index) {
        tempVal = $(this).val();

        idVal = $(formID + ' option').filter(function() {
          return this.value == tempVal;
        }).data('value');
        if (idVal === undefined) {
          throw tempVal + " is not a recognized value.";
        }

        $(this).val(idVal);
      });
    }
    catch (e) {
      controller.addErrors(e);
      return false;
    }
  },


  // Update input ID and name value for each object child element
  iterateFieldlists: function(obj) {
    for (const child in model.activeObject.children) {
      // Define child object in children
      let item = model.activeObject.children[child];

      // Loop through matching IDs and append count number
      $.each($(obj + ' ' + item.id), function() {

        // Update ID attribute
        $(this).attr('id', $(this).attr('id') + '-' + item.count);

        // Update name attribute
        $(this).attr('name', $(this).attr('name') + '-' + item.count);

        // Update count
        item.count++
      });
    }

  },


  // Pop most recent addition to modal list
  popModalList: function() {
    let x = model.createButton.pop();
    return x;
  },


  // Remove modal ref from list when a modal is cancelled
  removeModal: function(x) {
    this.popModalList();

    // Set active object
    this.selectActiveObject(view.getVal());
  },


  // Post modal form
  submitModal: function(x) {
    // Get object type from argument's ID
    var obj = this.determineObject(x);

    // Call post data function, get response
    var postPromise = this.postData(
        model[obj], model[obj].form.modalID, model[obj].post.create
    );

    postPromise.done(function(response) {
      // If form POST doesn't validate with wtforms, add errors to page
      if (response.success == false) {
        // For each received error...
        for (var itemName in response.data) {
          // Notify user of alert error with alert DIV
          controller.addErrors(itemName + ": " + response.data[itemName]);
        }

      }
      // ...Otherwise, return object sent from POST route
      else {
        // Notify user of item successfully added with alert DIV
        controller.addSuccess("Success! Created " + response.data.name + "!");

        // Update model object datalist
        model[obj].li.html = controller.updateTemplate(
            model[obj].li.html, response.data
        );

        // Set all [obj] datalists to updated model object datalist
        try {
          $('#' + model[obj].name + 's').each(function(index) {
            $(this).append('<option data-value="' + response.data.id +
                           '" value="' + response.data.name + '"></option>');
          });
        }
        catch (e) {
          console.log("Catch: " + e);
        }

        // FUTURE: Add empty LI

        // FUTURE: Select LI input value to created object

        // Hide modal
        view.closeModal();

        // Set active object to current value of create.html select value
        controller.selectActiveObject(view.getVal());
      }

    }).fail(function(error) {
      console.dir(error);
    })

    // FUTURE: get response from postData function
  },


  // Post main form
  submitForm: function(x) {
    // Call post data function, get response
    var postPromise = this.postData(
        model.activeObject, model.activeObject.form.id,
        model.activeObject.post.create
    );

    postPromise.done(function(response) {
      // If form POST doesn't validate with wtforms, add errors to page
      if (response.success == false) {
        console.dir(response);

        // For each received error...
        for (var item in response.data) {
          // Notify user of alert error with alert DIV
          controller.addErrors(item + ": " + response.data[item]);
        }

      }
      // ...Otherwise, reload page
      else {
        controller.addSuccess("Success! Created " + response.data.name + "!");

        // Update model object datalist
        model.activeObject.li.html = 
        controller.updateTemplate(model.activeObject.li.html, response.data);

        // Set all [obj] datalists to updated model object datalist
        try {
          $('#' + model.activeObject.name + 's').each(function(index) {
            $(this).append('<option data-value="' + response.data.id +
                           '" value="' + response.data.name + '"></option>');
          });
        }
        catch (e) {
          console.log("Catch: " + e);
        }

        // Refresh form
        $(model.activeObject.form.id).trigger('reset');

      }
    });
  },

  submitUpdate: function(x) {
    // If no object has been selected as active, get obj name from selected ID
    // Used for single pages where the object doesn't change (org.html,
    // artist.html, etc.)
    if (model.activeObject === null) {
      var obj = this.determineObject(x);
      this.selectActiveObject(obj);
    }

    // Call post data function, get response
    var postPromise = this.postData(
        model.activeObject, model.activeObject.form.id,
        model.activeObject.post.edit
    );

    postPromise.done(function(response) {
      if (response.success == undefined) {
        location.assign("/login")
      }
      // If form POST doesn't validate with wtforms, add errors to page
      else if (response.success == false) {
        console.dir(response);

        // For each received error...
        for (var item in response.data) {
          // Notify user of alert error with alert DIV
          controller.addErrors(item + ": " + response.data[item]);
        }
      }
      // ...Otherwise, reload page
      else if (response.success == true) {
        // Reload page
        window.location.reload(true);
      }

    });
  },


  // Post form
  postData: function(obj, formID, postRoute) {
    // Post data
    return $.ajax({
      url: postRoute,
      data: $(formID).serialize(),
      type: 'POST'
    });

  },


  retrieveResponse: function(response) {

  },


  // Add form/AJAX error to page
  addErrors: function(error) {
    // Create temporary DIV
    var div = $('<div/>');

    // Add error template HTML to DIV, add error message to inner DIV SPAN
    $(div).html($('#js-template_error').html())
                                       .find('.js-error-notice')
                                       .append(error);

    // Add new DIV to body
    $('.js-alert').append($(div).html());
  },


  // Add success message to page
  addSuccess: function(message) {
    // Create temporary DIV
    var div = $('<div/>');

    // Add success template HTML to DIV, add success message to inner DIV
    $(div).html($('#js-template_success').html())
                                         .find('.js-success-message')
                                         .append(message);

    // Add new DIV to body
    $('.js-alert').append($(div).html());
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
    $(div).find('datalist').append('\t<option data-value="' + update.id + 
                                   '" value="' + update.name + '"></option>')

    // Return template
    return $(div).html();
  },


  toggleInputs: function(x) {
    // Get object type from argument's ID
    var obj = this.determineObject(x);

    // Set active object
    this.selectActiveObject(obj);

    // Make inputs editable
    $(model[obj].form.id).find(":input").not(":button").each(function() {
      // Remove input readonly attributes
      $(this).attr("readonly", false);

      // Remove input disabled attributes
      $(this).attr("disabled", false);

      // Update input classes
      $(this).toggleClass('form-control-plaintext').toggleClass('form-control');
    });

    // Display hidden elements
    $(model[obj].form.id).find(".d-none").each(function() {
      $(this).toggleClass("d-none");
    });

    // Hide designated non-editable elements
    $(model[obj].form.id).find(".is-active").each(function() {
      $(this).toggleClass("is-active").toggleClass("d-none");
    });

    // Hide edit button
    $(x).addClass('invisible');

    // Update fieldlist item ID and name values for wtforms validation
    this.iterateFieldlists(model.activeObject.form.id);
  },


  // Show login modal
  showLogin: function(html) {
    // Show object modal and add object.modal HTML to modal body
    $('body').append(html);
    $('#js-modal_login').modal('show');
  },


  // Log out user
  getLogout: function() {
    $.get('/logout', function(data) {
      controller.addSuccess(data);
    });
  }


}