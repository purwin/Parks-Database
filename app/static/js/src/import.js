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
        li: $('#js-template_exhibition').html()
      },

      artwork: {
        name: "artwork",
        li: $('#js-template_artwork').html()
      },

      park: {
        name: "park",
        li: $('#js-template_park').html()
      },

      artist: {
        name: "artist",
        li: $('#js-template_artist').html()
      },

      org: {
        name: "org",
        li: $('#js-template_org').html()
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
            console.log(model.key);
            console.log(typeof model.key);

            // Build mapping UL
            // control.buildUL();

            // Show Data DIV
            // view.toggleVisible($('#js-data'));

            // set import_data file input to match import_file input
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
      },


      buildUL: function() {
        console.log("RUNNING BUILDUL");
        model.columns.forEach(function(column) {
          $('#js-data_ul').append('<li class="[ row mb-3 align-items-baseline ]">\
                <div class="js-key [ col-md-5 ]">' +
                  $(model.key) +
                '</div>\
                <div class="[ col-md-2 ]">\
                  <i class="fas fa-arrow-right"></i>\
                </div>\
                <div class="js-value [ col-md-5 ]">\
                </div>\
              </li>');
        })
      },


      // Build key/value list
      changeObject: function(x) {

        // Set new model.activeObject
        model.activeObject = model[x];

        // Format LI for each item in columns
        $('.js-value').each(function(item) {
          $(item).append(model.activeObject.li);
        });

      },


      // Post file form
      postFile: function(formID, postRoute) {

        // console.log("Form ID: " + formID);
        console.log("Post route: " + postRoute);

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


      // Post data form
      postData: function(formID, postRoute) {

      },


      iterateErrors: function(response) {
        // For each received error...
        for (const item in response.data) {
          console.log("ERROR ITEM: " + item);
          // Notify user of alert error with alert DIV
          controller.addErrors(item + ": " + response.data[item]);
        }
      },


      // Notify user if data import has errors
      notifyErrors: function(response) {

      },


      // Notify user if data import is 100% successful
      notifySuccess: function(response) {
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


      sendFile: function() {
        $('body').on('click', '#js-post_file', function(e) {
          e.preventDefault();
          control.sendFile($('#js-form_import_file'));
        });
      },


      sendData: function() {
        $('body').on('click', '#js-post_data', function(e) {
          e.preventDefault();
          control.sendData($('#js-form_import_data'));
        });
      },


      changeObject: function() {
        $('#class_object').change(function(e) {
          // Hide UL
          $('#js-data_ul').addClass('d-none');

          // Call controller function to show object section based on user input
          control.changeObject(view.getVal());

          // Show UL
          $('#js-data_ul').removeClass('d-none');

          // FUTURE: (create as Promise?)
        });
      },


      getVal: function() {
        return $('#class_object').val();
      },


      toggleVisible: function(element) {
        $(element).toggleClass("d-none");
      }

    };

    control.init()

  })();

});