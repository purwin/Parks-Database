(function() {

  let model = {

  };


  let controller = {

    postFile: function(x) {
      // Call post data function, get response
      let postPromise = this.postImport($(x).attr('id'), $(x).attr('action'));

      postPromise.done(function(response) {
        console.log(response);
      })

    },


    // Post form
    postImport: function(formID, postRoute) {

      console.log("Form ID: " + formID);
      console.log("Post route: " + postRoute);

      let formData = new FormData($(formID));

      // Post data
      return $.ajax({
        url: postRoute,
        contentType: false,
        data: formData,
        type: 'POST'
      });

    }

  };


  let view = {

    init: function() {
      this.sendFile()
    },

    sendFile: function() {
      $('#js-post_file').on('click', function(e) {
        e.preventDefault();
        controller.postFile($('#js-form_import'));
      });
    }

  };

})();