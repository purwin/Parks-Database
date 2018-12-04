import {controller} from './controller';
import {model} from './model';
import {view} from './view';
// import 'jquery';

// Create object classes for park and exhibition
model.park = new model.Obj("park");
model.exhibition = new model.Obj("exhibition");

// Set form POST route based on HTML's action attribute
// model.park.post.edit = $('form').attr('action');

// Set child datalist classnames
model.park.children = {
  "exhibition": ".js-datalist_exhibition",
  "artwork": ".js-datalist_artwork",
  "org": ".js-datalist_org"
};

// Init controller object
controller.init();