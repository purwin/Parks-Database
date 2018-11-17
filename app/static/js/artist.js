// Click event to make form editable
$("#form_edit").on('click', function(event) {

  // Disable a anchor links when in edit mode
  // $("#formArtist").find("a").each(function(e) {
  //  $(this).attr("onclick", "return false");
  // });

  // Make inputs editable
  $("#formArtist").find(":input").not(":button").each(function() {
    // Remove input readonly attributes
    $(this).attr("readonly", false);
    // Update input classes
    $(this).toggleClass('form-control-plaintext').toggleClass('form-control');
  });

  // Display hidden elements
  $("#formArtist").find(".d-none").each(function() {
    $(this).toggleClass("d-none");
  });

  // Hide non-edit block elements
  $("#formArtist").find(".d-block").each(function() {
    $(this).toggleClass("d-block").toggleClass("d-none");
  });

  // Hide non-edit inline elements
  $("#formArtist").find(".d-inline").each(function() {
    $(this).toggleClass("d-inline").toggleClass("d-none");
  });

  // Hide edit button
  $(this).addClass('invisible');
});


// Click event to cancel form editing
$("#form_cancel").on('click', function(event) {
  // Reload page
  window.location.reload(true);
});


// Switch datalist values with data-values (pulled from create.js)
function valSwitch() {
  try {
    $('#formArtist #datalist_art').each(function(index){
      // Hide item
      $(this).hide();
      // Store name value
      tempVal = $(this).val();
      console.log("Temp val: " + tempVal)
      // Get data-value (ID) of matching value item
      idVal = $('#formArtist option').filter(function() {
        return this.value == tempVal;
      }).data('value');
      console.log("ID val: " + idVal);
      // Assign ID as value 
      $(this).val(idVal);
    });
  }
  catch (e) {
    console.log("Catch: " + e);
  }
}


function postArtist() {
  var csrftoken = $('meta[name=csrf-token]').attr('content');

  // Add CSRF Token to AJAX Header
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken)
          }
      }
  });

  // send AJAX request to artist_edit function
  $.ajax({
    url: $('#formArtist').attr('action'),
    type: 'POST',
    // contentType: 'application/json; charset=utf-8',
    // dataType: 'json',
    data: $('#formArtist').serialize(),
    error: function(xhr, textStatus, error) {
        console.log("XHR: " + xhr.statusText);
        console.log("Text: " + textStatus);
        console.log("Error: " + error);
    }
  })
  .done(function(data) {
    // If the form has errors...
    if (data.success == false) {
      console.log("Form errors!");
      console.dir(data)
      // Add errors to page
    } else {
      // If no form errors, reload page
      // window.location.reload(true);
      console.log("Form success!");
      console.dir(data)
    }
  });
}


// Click event to submit form updates
$("#form_update").on('click', function(event) {

  // Do the data-value / value switch
  valSwitch();

  // POST AJAX data
  postArtist();
  });

// Click event to add an artist list item
$(".form_add").on('click', function(event) {
  // add template html to relevant ul
  $(".ul_artworks").append($("#template_artwork").html());
  var x = $( "input[name='artworks']" ).attr("name", "artworks-" + $(".ul_artworks li").length);
  console.log(x);
});


// Click event to remove current artwork from artist
$(".form_remove").on('click', function(event) {
  $(this).closest(".artist__li--artworks").remove();
})
