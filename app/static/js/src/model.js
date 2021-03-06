export const model = {

  // Object prototype for table objects (exhibition, artwork, artist, org)
  Obj: function(arg) {

    // Declare object name
    this.name = arg;

    // Declare object DIV ID
    this.div = {
      id: "#js-div_" + arg
    },

    this.ul = {
      class: ".js-ul_" + arg,
      html: ""
    },

    // Declare object LI class and HTML
    this.li = {
      class: ".js-li_" + arg,
      html:  $('#js-template_' + arg).html()
    },

    // Declare class names for object children (exhibition.artworks, etc.)
    this.children = {
    },

    this.datalist = '.js-datalist_' + arg,

    // Declare object modal ID and body HTML
    this.modal = {
      id: "#js-modal_" + arg, // modal ID ref
      html: '<form id="js-form-modal_' + arg + '" action="" method="POST">' + $('#js-form_' + arg).html() + '</form>' // modal body HTML
    },

    // Declare IDs for object form and object modal form
    this.form = {
      id: "#js-form_" + arg,
      modalID: "#js-form-modal_" + arg
    },

    // Declare action route for AJAX POST functions
    this.post = {
      create: "/" + arg + "s/create",
      edit: $('form').attr('action'),
    }
  },


  // Declare selected form type
  activeObject: null,


  // Declare list of active createButtons
  createButton: [null]

};