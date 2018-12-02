import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for artwork, artist, and exhibition
model.artwork = new model.Obj("artwork");
model.artist = new model.Obj("artist");
model.exhibition = new model.Obj("exhibition");

// Set form POST route based on HTML's action attribute
model.artwork.post.edit = $('form').attr('action');

// Init controller object
controller.init();