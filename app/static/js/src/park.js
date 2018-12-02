import {controller} from './controller';
import {model} from './model';
import {view} from './view';
// import 'jquery';

// Create object classes for park and exhibition
model.park = new model.Obj("park");
model.exhibition = new model.Obj("exhibition");

// Set form POST route based on HTML's action attribute
model.park.post.edit = $('form').attr('action');

// Init controller object
controller.init();