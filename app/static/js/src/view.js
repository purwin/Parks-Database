import {controller} from './controller';

export let view = {

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

    this.editForm();

    this.cancelForm();

    this.updateForm();

    this.logoutUser();
  },


  hideDivs: function() {
    // Hide all object DIVs
    $(".js-create-div").hide();

    // Hide submit buttons
    $(".js-submit-div").hide();
  },


  getVal: function() {
    return $('#js-create_object').val();
  },


  // Determine active form based on input type
  selectForm: function() {
    $('#js-create_object').change(function(e) {

      // Call controller function to show object section based on user input
      controller.showSection(view.getVal());
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
  },

  // Click event to make read-only forms editable
  editForm: function() {
    $(".js-form-edit").on('click', function(e) {

      // Call controller function to make view-only form editable
      controller.toggleInputs(this);
    });
  },


  // Click event to submit [obj]_edit.html forms to database
  updateForm: function() {
    $('body').on('click', '.js-update-form', function(e) {
      e.preventDefault();

      // Call controller function to POST data via AJAX
      controller.submitUpdate(this);
    });
  },


  // Click event to cancel form editing and reload page
  cancelForm: function() {
    $(".js-cancel-form").on('click', function(e) {
      // Reload page
      window.location.reload(true);
    });
  },


  // Click event for user logging out
  logoutUser: function() {
    $('#js-logout').on('click', function(e) {
      controller.getLogout();
    });
  }

}