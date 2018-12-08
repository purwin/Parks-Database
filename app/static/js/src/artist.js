import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for artwork, artist, and exhibition
model.artist = new model.Obj("artist");
model.artwork = new model.Obj("artwork");

// Set child datalist classnames
model.artist.children = {
  artwork: {
    count: $('.js-datalist_artwork').length + 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  }
};

// Init controller object
controller.init();