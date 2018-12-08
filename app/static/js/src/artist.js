import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for artwork, artist, and exhibition
model.artist = new model.Obj("artist");
model.artwork = new model.Obj("artwork");

// Set child datalist classnames
model.artist.children = {
  artist: {
    count: $('.js-datalist_artist').length + 1,
    class: ".js-datalist_artist",
    id: "#js-datalist_artist"
  }
};

// Init controller object
controller.init();