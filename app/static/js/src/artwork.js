import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for artwork, artist, and exhibition
model.artwork = new model.Obj("artwork");
model.artist = new model.Obj("artist");
model.exhibition = new model.Obj("exhibition");

// Set child datalist classnames
model.artwork.children = {
  artist: {
    count: $('.js-datalist_artist').length + 1,
    class: ".js-datalist_artist",
    id: "#js-datalist_artist"
  },
  exhibition: {
    count: $('.js-datalist_exhibition').length + 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  },
  park: {
    count: $('.js-datalist_park').length + 1,
    class: ".js-datalist_park",
    id: "#js-datalist_park"
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
