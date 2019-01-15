/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"import": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push(["./app/static/js/src/import.js","commons"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./app/static/js/src/import.js":
/*!*************************************!*\
  !*** ./app/static/js/src/import.js ***!
  \*************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _controller__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./controller */ "./app/static/js/src/controller.js");




$(document).ready(function () {
  (function importData() {
    // MODEL
    let model = {
      // Store list of CSV column heads
      columns: [],
      // Declare selected form type
      activeObject: null,
      key: $('#js-template_keys').html(),
      exhibition: {
        name: "exhibition",
        li: $('#js-template_exhibition').html()
      },
      artwork: {
        name: "artwork",
        li: $('#js-template_artwork').html()
      },
      park: {
        name: "park",
        li: $('#js-template_park').html()
      },
      artist: {
        name: "artist",
        li: $('#js-template_artist').html()
      },
      org: {
        name: "org",
        li: $('#js-template_org').html()
      }
    }; // CONTROLLER

    let control = {
      init: function () {
        view.init();
      },
      // Send import file data to server, get response
      sendFile: function (x) {
        // Call post data function, get response
        let postPromise = this.postFile($(x), $(x).attr('action'));
        postPromise.done(function (response) {
          console.log(response); // If form POST doesn't validate with wtforms, add errors to page

          if (response.success == false) {
            console.log("Form Error(s)!");
            console.dir(response);
            control.iterateErrors(response);
          } else if (response.success == true) {
            // Store response list in model.columns
            model.columns = response.data; // Loop through response, add as option to model.key

            for (const item in response.data) {
              console.log("COLUMN: " + item); // Add item to column list
              // model.columns.push(item);
              // Add item as option to key SelectField

              model.key = $(model.key).append($("<option></option>").attr("value", item).text(item));
            } // Build mapping UL


            control.buildUL(); // Show Data DIV

            view.toggleVisible($('#js-data')); // set import_data file input to match import_file input
          } else {
            console.log("Don't know what to do!");
            console.dir(response);
          }
        });
      },
      // Send import data to server, get response
      sendData: function (x) {
        // Call post data function, get response
        let postPromise = this.postFile($(x), $(x).attr('action'));
      },
      buildUL: function () {
        model.columns.forEach(function (column) {
          $('#js-ul_data').append('<li class="[ row mb-3 align-items-baseline ]">\
                <div class="js-key [ col-md-5 ]">' + $(model.key).html() + '</div>\
                <div class="[ col-md-2 ]">\
                  <i class="fas fa-arrow-right"></i>\
                </div>\
                <div class="js-value [ col-md-5 ]">\
                </div>\
              </li>');
        });
      },
      // Build key/value list
      changeObject: function (x) {
        // Set new model.activeObject
        model.activeObject = model[x]; // Format LI for each item in columns

        $('.js-value').each(function (item) {
          $(item).append(model.activeObject.li);
        });
      },
      // Post file form
      postFile: function (formID, postRoute) {
        // console.log("Form ID: " + formID);
        console.log("Post route: " + postRoute);
        let formData = new FormData($(formID)[0]); // Post data

        return $.ajax({
          type: 'POST',
          url: postRoute,
          processData: false,
          contentType: false,
          data: formData
        });
      },
      // Post data form
      postData: function (formID, postRoute) {},
      iterateErrors: function (response) {
        // For each received error...
        for (const item in response.data) {
          console.log("ERROR ITEM: " + item); // Notify user of alert error with alert DIV

          _controller__WEBPACK_IMPORTED_MODULE_1__["controller"].addErrors(item + ": " + response.data[item]);
        }
      },
      // Notify user if data import has errors
      notifyErrors: function (response) {},
      // Notify user if data import is 100% successful
      notifySuccess: function (response) {
        _controller__WEBPACK_IMPORTED_MODULE_1__["controller"].addSuccess(response);
      }
    }; // VIEW

    let view = {
      init: function () {
        this.sendFile();
        this.sendData();
        this.changeObject();
      },
      sendFile: function () {
        $('body').on('click', '#js-post_file', function (e) {
          e.preventDefault();
          control.sendFile($('#js-form_import_file'));
        });
      },
      sendData: function () {
        $('body').on('click', '#js-post_data', function (e) {
          e.preventDefault();
          control.sendData($('#js-form_import_data'));
        });
      },
      changeObject: function () {
        $('#class_object').change(function (e) {
          // Hide UL
          $('#js-data_ul').addClass('d-none'); // Call controller function to show object section based on user input

          control.changeObject(view.getVal()); // Show UL

          $('#js-data_ul').removeClass('d-none'); // FUTURE: (create as Promise?)
        });
      },
      getVal: function () {
        return $('#class_object').val();
      },
      toggleVisible: function (element) {
        $(element).toggleClass("d-none");
      }
    };
    control.init();
  })();
});
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ })

/******/ });
//# sourceMappingURL=import.bundle.js.map