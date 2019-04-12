$(window).on('load', () => {
  // Add animation classes to container and loading divs
  const internalLinkLoad = e => {
    $('.js-spinner').addClass('is-spinning');

    // Fade out container div
    $('.container-fluid').toggleClass('fade-out');
    // $('#js-container').hide('slow');

    // Fade in loading div
    $('#js-loading').toggleClass('fade-in').toggleClass('is-inactive');

    // $('#js-loading').show('slow');
    $('.js-spinner-div').toggleClass('fade-in').toggleClass('is-hidden');
  };


  // Add loading transition to all a class="js-internal"
  $('.js-internal').on('click', e => {
    // Add temporary preventDefault to observe transition
    // e.preventDefault();
    internalLinkLoad(e);
  });


  // Toggle indexed names based on selected index value
  $('.js-index').on('click', e => {
    console.log('.js-index clicked!');
    // Get value of selected item
    const classTarget = $(this).attr('id');

    // Hide elements that don't have the target value as a class
    $('.js-index-item').not(document.getElementsByClassName(classTarget)).hide('fast');

    // Show targeted elements
    $(document.getElementsByClassName(classTarget)).show('slow');
  })

});


// FUTURE: if hide/show work for both things, make one single function called separately