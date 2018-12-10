import {controller} from './controller';
import {model} from './model';
import {view} from './view';

import 'jquery';
import 'bootstrap';

// Create exhibition object class
model.exhibition = new model.Obj("exhibition");

// Set child datalist classnames
model.exhibition.children = {
  artwork: {
    count: 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  },
  park: {
    count: 1,
    class: ".js-datalist_park",
    id: "#js-datalist_park"
  },
  org: {
    count: 1,
    class: ".js-datalist_org",
    id: "#js-datalist_org"
  }
};



// Create artwork object class
model.artwork = new model.Obj("artwork");

// Set child datalist classnames
model.artwork.children = {
  artist: {
    count: 1,
    class: ".js-datalist_artist",
    id: "#js-datalist_artist"
  },
  exhibition: {
    count: 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  },
  park: {
    count: 1,
    class: ".js-datalist_park",
    id: "#js-datalist_park"
  }
};



// Create artist object class
model.artist = new model.Obj("artist");

// Set child datalist classnames
model.artist.children = {
  artwork: {
    count: 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  }
};



// Create park object class
model.park = new model.Obj("park");

// Set child datalist classnames
model.park.children = {
  artwork: {
    count: 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  },
  exhibition: {
    count: 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  }
};



// Create org object class
model.org = new model.Obj("org");

// Set child datalist classnames
model.org.children = {
  exhibition: {
    count: 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  }
};


// Create org object class
model.create = new model.Obj("create");

// Set child datalist classnames
model.create.children = {
  artist: {
    count: 1,
    class: ".js-datalist_artist",
    id: "#js-datalist_artist"
  },
  exhibition: {
    count: 1,
    class: ".js-datalist_exhibition",
    id: "#js-datalist_exhibition"
  },
  park: {
    count: 1,
    class: ".js-datalist_park",
    id: "#js-datalist_park"
  },
  artwork: {
    count: 1,
    class: ".js-datalist_artwork",
    id: "#js-datalist_artwork"
  },
  org: {
    count: 1,
    class: ".js-datalist_org",
    id: "#js-datalist_org"
  }
};


// Init controller object
controller.init();
