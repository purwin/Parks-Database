import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for exhibition, artwork, park
model.exhibition = new model.Obj("exhibition");
model.artwork = new model.Obj("artwork");
model.park = new model.Obj("park");
model.org = new model.Obj("org");


// Set form POST route based on HTML's action attribute
// model.exhibition.post.edit = $('form').attr('action');

// Set child datalist classnames
model.exhibition.children = {
  artwork: {
    count: $('.js-datalist_artwork').length + 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  },
  park: {
    count: $('.js-datalist_park').length + 1,
    class: ".js-datalist_park",
    id: "#js-datalist_park"
  },
  org: {
    count: $('.js-datalist_org').length + 1,
    class: ".js-datalist_org",
    id: "#js-datalist_org"
  }
};

// Init controller object
controller.init();