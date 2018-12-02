import {controller} from './controller';
import {model} from './model';
import {view} from './view';
// import 'jquery';

// Create object classes for exhibition, artwork, park
model.exhibition = new model.Obj("exhibition");
model.artwork = new model.Obj("artwork");
model.park = new model.Obj("park");


// Set form POST route based on HTML's action attribute
model.exhibition.post.edit = $('form').attr('action');

// Init controller object
controller.init();