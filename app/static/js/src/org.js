import {controller} from './controller';
import {model} from './model';
import {view} from './view';

// Create object classes for org and exhibition
model.org = new model.Obj("org");
model.exhibition = new model.Obj("exhibition");

// Set child datalist classnames
model.org.children = {
  exhibition: {
    count: $('.js-datalist_exhibition').length + 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  }
};

// Init controller object
controller.init();

console.dir(model.org);