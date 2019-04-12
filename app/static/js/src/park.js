import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for park and exhibition
model.park = new model.Obj("park");
model.exhibition = new model.Obj("exhibition");

// Set child datalist classnames
model.park.children = {
  artwork: {
    count: $('.js-datalist_artwork').length + 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  },
  exhibition: {
    count: $('.js-datalist_exhibition').length + 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  }
};

// Init controller object
controller.init();

// Call MDBootstrap function to set table as sortable
$('#js-table_exhibition').DataTable({
  // Sort table based on initial column (Artworks)
  "order": [[ 0, "asc" ]],
  "searching": false,
  "paging": false,
  "info" : false
});
