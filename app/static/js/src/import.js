'use strict';

import 'jquery';
import {controller} from './controller';


$(document).ready(function() {

  (function importData() {

    // MODEL
    let model = {

      // Store list of CSV column heads
      columns: [],

      // Declare selected form type
      activeObject: null,

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
          console.log(response);
          // If form POST doesn't validate with wtforms, add errors to page
          if (response.success == false) {
            console.log("Form Error(s)!");
            console.dir(response);

            control.iterateErrors(response);
          }

          else if (response.success == true) {
            // Store response list in model.columns
            model.columns = response.data;

            // Loop through response, add as option to model.key
            for (const item of response.data) {
              console.log("COLUMN: " + item);
              // Add item to column list

              // Add item as option to key SelectField
              model.key = $(model.key).append($("<option></option>")
                                      .attr("value", item)
                                      .text(item));
            }

            console.log(model.columns);

            // Build mapping UL
            control.buildUL();

            // Show Data DIV
            view.toggleVisible($('#js-import_data'));

            // set import_data file input to match import_file input
            // console.log($('#file_file')[0].files[0]);
            $('#file_file').clone().attr('id', 'data_file').appendTo('#js-import_data_ul');
          }

          else {
            console.log("Don't know what to do!");
            console.dir(response);
          }

        })

      },


      // Send import data to server, get response
      sendData: function(x) {

        // Call post data function, get response
        let postPromise = this.postFile($(x), $(x).attr('action'));

        postPromise.done(function(response) {
          console.log(response);
          // If form POST doesn't validate with wtforms, add errors to page
          if (response.success == false) {
            console.log("Form Error(s)!");
            console.dir(response);

            control.iterateErrors(response);
          }

          else if (response.success == true) {
            // Store response list in model.columns
            model.columns = response.data;
          }

          else {
            console.log("Don't know what to do!");
            console.dir(response);
          }

        })

      },


      buildUL: function() {

        model.columns.forEach(function(column) {
          $('#js-data_ul').append(
              '<li class="[ row mb-3 align-items-baseline justify-content-center ]">\
                <div class="js-key">' +
                  $(model.key)[0].outerHTML +
                '</div>\
                <div class="[ px-3 ]">\
                  <i class="fas fa-arrow-right c-blue--l"></i>\
                </div>\
                <div class="js-value"></div>\
              </li>');
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

        console.log(model.activeObject);

        // Set values LI based on selected Object name
        $('.js-value').each(function() {
          $(this).html(model.activeObject.li);
        });

        // Update name attribute to match WTForms FieldList formatting
        control.appendNameList(model.activeObject.class);

      },


      // Post file form
      postFile: function(formID, postRoute) {

        // console.log("Form ID: " + formID);
        console.log("Post route: " + postRoute);

        let formData = new FormData($(formID)[0]);

        console.log(formData);

        // Post data
        return $.ajax({
          type: 'POST',
          url: postRoute,
          processData: false,
          contentType: false,
          data: formData,
        });

      },


      // Post data form
      postData: function(formID, postRoute) {

      },


      // Add each error to HTML page
      iterateErrors: function(response) {

        // For each received error...
        for (const item in response.data) {
          console.log("ERROR ITEM: " + item);
          // Notify user of alert error with alert DIV
          controller.addErrors(item + ": " + response.data[item]);
        }

      },


      // Notify user if data import has errors
      notifyDataErrors: function(response) {

      },


      // Notify user if data import is 100% successful
      notifyDataSuccess: function(response) {

        controller.addSuccess(response);

      }

    };


    // VIEW
    let view = {

      init: function() {

        this.sendFile();
        this.sendData();
        this.changeObject();

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
        });

      },

      // Function called when Class_object option is changed
      changeObject: function() {

        $('#class_object').change(function(e) {

          let obj = view.getVal();

          if (obj) {
            // Hide UL
            // FUTURE: Move to View
            $('#js-data_ul').addClass('d-none');

            // Call controller function to show object section based on user input
            control.changeObject(obj);

            // Show UL
            // FUTURE: Move to View
            $('#js-data_ul').removeClass('d-none');

            // FUTURE: (create as Promise?)
          }
        });

      },

      // Function called to retrieve current Class_object value
      getVal: function() {

        return $('#class_object').val();

      },


      // Function called to change display value of element
      toggleVisible: function(element) {

        $(element).toggleClass("d-none");

      }

    };


    control.init()

  })();

});