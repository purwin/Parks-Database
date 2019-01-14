'use strict';

import 'jquery'

import {controller} from './controller';

$(document).ready(function() {

  (function importData() {

    let model = {

      columns: [],

      // Declare selected form type
      activeObject: null,

      artist: {
        li: $('#js-template_artist').html()
      }

    };


    let cont = {

      init: function() {
        view.init()
      },


      // Send import file data to server, work with response
      importFile: function(x) {
        // Call post data function, get response
        let postPromise = this.postFile($(x), $(x).attr('action'));

        postPromise.done(function(response) {
          console.log(response);
          // If form POST doesn't validate with wtforms, add errors to page
          if (response.success == false) {
            console.log("Form Error(s)!");
            console.dir(response);

            // For each received error...
            for (var itemName in response.data) {
              console.log("ITEM: " + itemName);
              // Notify user of alert error with alert DIV
              controller.addErrors(itemName + ": " + response.data[itemName]);
            }

          }

          else {
            console.log("Form Sucess!");
            console.dir(response);

          }

        })

      },


      // Send import data to server, work with response
      importData: function(x) {

      },


      // set select field
      // show second form (view)


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

      }

    };


    let view = {

      init: function() {
        this.sendFile();
      },


      sendFile: function() {
        $('body').on('click', '#js-post_file', function(e) {
          e.preventDefault();
          console.log("CLICKED");
          cont.importFile($('#js-form_import'));
        });
      }

    };

    cont.init()

  })();

});