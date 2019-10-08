$(window).on('load', () => {
  // Add animation classes to container and loading divs
  const internalLinkLoad = () => {
    $('.js-spinner').toggleClass('is-spinning');

    // Fade out container div
    $('.container-fluid').toggleClass('is-hidden');

    // Fade in loading div
    $('#js-loading').toggleClass('is-hidden');

    $('.js-spinner-div').toggleClass('is-hidden');
  };


  // Add loading transition to all a class="js-internal"
  $('.js-internal').on('click', e => {
    // Add temporary preventDefault to observe transition
    // e.preventDefault();
    internalLinkLoad();
  });


  // Toggle indexed names based on selected index value
  $('.js-index').on('click', e => {

    // If selected doesn't have selected class, toggle displayed index items
    if (!$(e.target).hasClass('index--selected')) {
      $('.index--selected').removeClass('index--selected');

      // Get value of selected item
      const classTarget = e.target.id;

      // Add selected class
      $(e.target).addClass('index--selected');

      // Hide elements that don't have the target value as a class
      $('.js-index-item').not(
        document.getElementsByClassName(classTarget)
        ).addClass('d-none');

      // Show targeted elements
      $(document.getElementsByClassName(classTarget)).removeClass('d-none');
    }
  })

});
