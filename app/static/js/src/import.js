'use strict';

import {controller} from './controller';


$(document).ready(function() {

  (function importData() {

    // MODEL
    let model = {

      // Store list of CSV column heads
      columns: [],

      // Declare selected form type
      activeObject: null,

      // Store result array from imported data
      result: [],

      // Route to post AJAX request to receive CSV download
      routeExport: '/export',

      key: $('#js-template_keys').html(),

      exhibition: {
        name: "exhibition",
        li: $('#js-template_exhibition').html(),
        class: '.js-column_exhibition'
      },

      artwork: {
        name: "artwork",
        li: $('#js-template_artwork').html(),
        class: '.js-column_artwork'
      },

      park: {
        name: "park",
        li: $('#js-template_park').html(),
        class: '.js-column_park'
      },

      artist: {
        name: "artist",
        li: $('#js-template_artist').html(),
        class: '.js-column_artist'
      },

      org: {
        name: "org",
        li: $('#js-template_org').html(),
        class: '.js-column_org'
      }

    };


    // CONTROLLER
    let control = {

      init: function() {
        view.init()
      },


      // Send import file data to server, get response
      sendFile: function(x) {

        // Call post data function, get response
        let postPromise = this.postFile($(x), $(x).attr('action'));

        postPromise.done(function(response) {
          // If form POST doesn't validate with wtforms, add errors to page
          if (response.success == false) {
            control.iterateErrors(response);
          }

          // If POST is successful, add column values to import_data form
          else if (response.success == true) {
            // Store response list in model.columns
            model.columns = response.data;

            // Clear model.key of any old data
            model.key = $('#js-template_keys').html();

            // Call function to populate key option values
            control.iterateKeys(response.data);

            // Clear object/column values in map section
            view.refreshMap();

            // Build mapping UL
            control.buildUL();

            // Show Data DIV
            view.showItem($('#js-import_data'));

            // Delete current #data_file if it exists
            $('#data_file').remove();

            // Set import_data file input to match import_file input
            $('#file_file').clone()
                           .attr('id', 'data_file')
                           .addClass('d-none')
                           .appendTo('#js-import_data_ul');
          }

          else {
            console.dir(response);
          }

        })

      },


      // Send import data to server, get response
      sendData: function(x) {
        // Call post data function, get response
        let postPromise = this.postFile($(x), $(x).attr('action'));

        postPromise.done(function(response) {
          // If form POST doesn't validate with wtforms, add errors to page
          if (response.success == false) {
            control.iterateErrors(response.data);
          }

          // If POST is successful, notify user of import results via modal
          else if (response.success == true) {
            // Store response list in model.columns
            model.result = response;

            // Get count of import success/warning/error values
            const resultCount = control.iterateResults(model.result.data);

            // Add result info to modal
            view.showModal(
              `<h3 class="[ my-4 ]">
                ${model.activeObject.name.toUpperCase()} IMPORT RESULTS
              </h3>
              <ul>
                <li>Records imported: ${resultCount.success}</li>
                <li>Records with warnings: ${resultCount.warning}</li>
                <li>Records with errors: ${resultCount.error}</li>
              </ul>
              <h3 class="[ my-4 ]">EXPORT RESULTS?</h3>`
            );

            // Restore post buttons
            view.clearLoading();
          }

          else {
            console.dir(response);
          }

        })

      },


      // Send export data to server, get file to download
      sendExport: function(x) {
        // Add import results JSON to export form field
        $('#export_data').val(JSON.stringify(model.result.data));
        // Submit form
        $(x).closest('form').submit();
        // Reset page
        view.closeModal();
      },


      buildUL: function() {
        // Loop through model.columns, add to page
        model.columns.forEach(function(column) {
          $('#js-data_ul').append(
            `<li 
              class="[ row mb-4 align-items-baseline justify-content-center ]"
             >
              <div class="js-key [ col ]">
                ${$(model.key)[0].outerHTML}
              </div>
              <div class="[ px-3 col-12 col-md-1 text-center ]">
                <i class="fas fa-arrow-right c-blue--l arrow-import"></i>
              </div>
              <div class="js-value [ col ]"></div>
            </li>`
          );
        });

        // Update name attribute to match WTForms FieldList formatting
        control.appendNameList('.js-column_key');

      },


      // Loop through arguments to update name attribute for WTForms Fieldlist
      appendNameList: function(items) {
        $(items).each(function(index) {
          $(this).attr('name', $(this).attr('name') + '-' + (index + 1));
        });
      },


      // Build key/value list
      changeObject: function(x) {
        // Set new model.activeObject
        model.activeObject = model[x];

        // Set values LI based on selected Object name
        $('.js-value').each(function() {
          $(this).html(model.activeObject.li);
        });

        // Update name attribute to match WTForms FieldList formatting
        control.appendNameList(model.activeObject.class);

      },


      // Post file form
      postFile: function(formID, postRoute) {
        let formData = new FormData($(formID)[0]);

        // Post data
        return $.ajax({
          type: 'POST',
          url: postRoute,
          processData: false,
          contentType: false,
          data: formData,
        });

      },


      // Add each error to HTML page
      iterateErrors: function(response) {
        // For each received error...
        for (const item in response.data) {
          // Notify user of alert error with alert DIV
          controller.addErrors(item + ": " + response.data[item]);
        }

      },


      // Add received key values to key select option
      iterateKeys: function(data) {
        // Loop through response, add as option to model.key
        for (const item of data) {
          // Add item as option to key SelectField
          model.key = $(model.key).append($("<option></option>")
                                  .attr("value", item)
                                  .text(item));
        }

      },


      // Sift through passed object argument, return success/error/warning count
      iterateResults: function(obj_data) {
        // Count # of successes, warnings, errors
        return obj_data.reduce((item, obj) => {
          obj.success == true ? item.success++ : item.error++;
          obj.warning.length > 0 && item.warning++;
          return item;
        }, {success: 0, warning: 0, error: 0});
      },


      // Function called when import is complete, resetting page view and values
      resetImport: function() {
        // Reset model values
        model.columns = [];
        model.activeObject = null;
        model.result = [];
        model.key = $('#js-template_keys').html();

        // Clear import file text
        $('#file_text').html("");
      }

    };


    // VIEW
    let view = {

      init: function() {
        this.sendFile();
        this.sendData();
        this.changeObject();
        this.closeModal();
        this.sendExport();
        this.selectFile();
      },


      // Function called when Submit File submit form button clicked
      sendFile: function() {
        $('#js-post_file').on('click', function(e) {
          e.preventDefault();
          control.sendFile($('#js-form_import_file'));
        });

      },


      // Function called when Submit Data submit form button clicked
      sendData: function() {
        $('#js-post_data').on('click', function(e) {
          e.preventDefault();
          control.sendData($('#js-form_import_data'));
          view.addLoading();
        });

      },

      // Function called when Class_object option is changed
      changeObject: function() {
        $('#class_object').change(function(e) {
          let obj = view.getVal();

          if (obj) {
            // Call controller function to show object section based on user input
            control.changeObject(obj);

            // Show UL
            $('#js-data_ul').removeClass('d-none');
          }

        });

      },


      // Function called to retrieve current Class_object value
      getVal: function() {
        return $('#class_object').val();
      },


      selectFile: function() {
        // Referenced from https://stackoverflow.com/questions/11235206/
        // twitter-bootstrap-form-file-element-upload-button/25053973#25053973
        $(document).on('change', '#file_file', function(e) {
          $('#file_text').html(this.files[0].name);
        });
      },


      // Function called to display passed element
      showItem: function(element) {
        $(element).removeClass("d-none");
      },


      // Function called to hide passed element
      hideItem: function(element) {
        $(element).addClass("d-none");
      },


      // Function called to display export modal, add HTML from passed argument
      showModal: function(html) {
        // Show modal with results
        $('#js-modal_results').modal('show')
                              .find('div.modal-body')
                              .html(html);
      },


      // Function called when modal is closed
      closeModal: function() {
        $('#js-modal_results').modal('hide');

        $('#js-modal_results').on('hidden.bs.modal', function (e) {
          // Call function to hide modal, reset import page
          view.resetImport();
        });

      },


      // Function called when export data button in modal selected
      sendExport: function() {
        $('#js-modal-post_export').on('click', function(e) {
          e.preventDefault();
          // Call function to submit import results
          control.sendExport(this);
        })
      },


      // Function called when import is complete, resetting page view and values
      resetImport: function() {
        // Hide #js-import_data DIV
        view.hideItem('#js-import_data');

        // Clear #file_file
        $('#file_file').trigger('reset');

        // Clear forms
        $('#js-form_import_file').trigger('reset');
        $('#js-form_import_data').trigger('reset');
        $('#js-form_export').trigger('reset');
        view.refreshMap();
        view.clearLoading();
        // Call control function to reset model values
        control.resetImport();
      },


      refreshMap: function() {
        // Clear selected object value
        $('#class_object').val("");

        // Clear Data UL if attributes exist
        $('#js-data_ul').empty().addClass('d-none');
      },


      // Function called to disable post buttons when import in progress
      // Show user a loading spinner
      addLoading: function() {
        // Disable submit buttons
        $('.js-cancel-import, .js-post-import').prop('disabled', true);

        // Show/add spinner
        view.showItem('#js-post_loading');
        $('.js-spinner').addClass('is-spinning');
        view.hideItem('#js-post_label');
      },


      // Function called to re-enable post buttons after import completes
      // Hide spinner span
      clearLoading: function() {
        // Un-disable submit buttons
        $('.js-cancel-import, .js-post-import').prop('disabled', false);

        // Clear/hide spinner
        view.hideItem('#js-post_loading');
        view.showItem('#js-post_label');
      }

    };


    control.init()

  })();

});