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
function valSwitch(){
  try {
    $('#formArtist #datalist_art').each(function(index){
      tempVal = $(this).val();
      console.log("Temp val: " + tempVal)
      idVal = $('#formArtist option').filter(function() {
        return this.value == tempVal;
      }).data('value');
      console.log("ID val: " + idVal);
      $(this).val(idVal);
    });
  }
  catch (e) {
    console.log("Catch: " + e);
  }
}


// Click event to submit form updates
$("#form_update").on('click', function(event) {
  // Do the data-value / value switch
  valSwitch();
  // Post data to /artists/<int:artist_id>/edit url
  $("#formArtist").submit();
});


// Click event to add an artist list item
$(".form_add").on('click', function(event) {
  // add template html to relevant ul
  $(".ul_artworks").append($("#template_artwork").html());
});


// Click event to remove current artwork from artist
$(".form_remove").on('click', function(event) {
  $(this).closest(".artist__li--artworks").remove();
})
