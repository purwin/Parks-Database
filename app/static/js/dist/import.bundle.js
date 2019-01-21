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
        li: $('#js-template_exhibition').html(),
        class: '.js-column_exhibition'
      },
      artwork: {
        name: "artwork",
        li: $('#js-template_artwork').html(),
        class: '.js-column_artwork'
      },
      park: {
        name: "park",
        li: $('#js-template_park').html(),
        class: '.js-column_park'
      },
      artist: {
        name: "artist",
        li: $('#js-template_artist').html(),
        class: '.js-column_artist'
      },
      org: {
        name: "org",
        li: $('#js-template_org').html(),
        class: '.js-column_org'
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

            for (const item of response.data) {
              console.log("COLUMN: " + item); // Add item to column list
              // Add item as option to key SelectField

              model.key = $(model.key).append($("<option></option>").attr("value", item).text(item));
            }

            console.log(model.columns); // Build mapping UL

            control.buildUL(); // Show Data DIV

            view.toggleVisible($('#js-import_data')); // set import_data file input to match import_file input
            // console.log($('#file_file')[0].files[0]);

            $('#file_file').clone().attr('id', 'data_file').addClass('d-none').appendTo('#js-import_data_ul');
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
        postPromise.done(function (response) {
          console.log(response); // If form POST doesn't validate with wtforms, add errors to page

          if (response.success == false) {
            console.log("Form Error(s)!");
            console.dir(response);
            control.iterateErrors(response);
          } else if (response.success == true) {
            // Store response list in model.columns
            model.columns = response.data;
          } else {
            console.log("Don't know what to do!");
            console.dir(response);
          }
        });
      },
      buildUL: function () {
        model.columns.forEach(function (column) {
          $('#js-data_ul').append('<li class="[ row mb-3 align-items-baseline justify-content-center ]">\
                <div class="js-key">' + $(model.key)[0].outerHTML + '</div>\
                <div class="[ px-3 ]">\
                  <i class="fas fa-arrow-right c-blue--l"></i>\
                </div>\
                <div class="js-value"></div>\
              </li>');
        }); // Update name attribute to match WTForms FieldList formatting

        control.appendNameList('.js-column_key');
      },
      // Loop through arguments to update name attribute for WTForms Fieldlist
      appendNameList: function (items) {
        $(items).each(function (index) {
          $(this).attr('name', $(this).attr('name') + '-' + (index + 1));
        });
      },
      // Build key/value list
      changeObject: function (x) {
        // Set new model.activeObject
        model.activeObject = model[x];
        console.log(model.activeObject); // Set values LI based on selected Object name

        $('.js-value').each(function () {
          $(this).html(model.activeObject.li);
        }); // Update name attribute to match WTForms FieldList formatting

        control.appendNameList(model.activeObject.class);
      },
      // Post file form
      postFile: function (formID, postRoute) {
        // console.log("Form ID: " + formID);
        console.log("Post route: " + postRoute);
        let formData = new FormData($(formID)[0]);
        console.log(formData); // Post data

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
      // Add each error to HTML page
      iterateErrors: function (response) {
        // For each received error...
        for (const item in response.data) {
          console.log("ERROR ITEM: " + item); // Notify user of alert error with alert DIV

          _controller__WEBPACK_IMPORTED_MODULE_1__["controller"].addErrors(item + ": " + response.data[item]);
        }
      },
      // Notify user if data import has errors
      notifyDataErrors: function (response) {},
      // Notify user if data import is 100% successful
      notifyDataSuccess: function (response) {
        _controller__WEBPACK_IMPORTED_MODULE_1__["controller"].addSuccess(response);
      }
    }; // VIEW

    let view = {
      init: function () {
        this.sendFile();
        this.sendData();
        this.changeObject();
      },
      // Function called when Submit File submit form button clicked
      sendFile: function () {
        $('#js-post_file').on('click', function (e) {
          e.preventDefault();
          control.sendFile($('#js-form_import_file'));
        });
      },
      // Function called when Submit Data submit form button clicked
      sendData: function () {
        $('#js-post_data').on('click', function (e) {
          e.preventDefault();
          control.sendData($('#js-form_import_data'));
        });
      },
      // Function called when Class_object option is changed
      changeObject: function () {
        $('#class_object').change(function (e) {
          let obj = view.getVal();

          if (obj) {
            // Hide UL
            // FUTURE: Move to View
            $('#js-data_ul').addClass('d-none'); // Call controller function to show object section based on user input

            control.changeObject(obj); // Show UL
            // FUTURE: Move to View

            $('#js-data_ul').removeClass('d-none'); // FUTURE: (create as Promise?)
          }
        });
      },
      // Function called to retrieve current Class_object value
      getVal: function () {
        return $('#class_object').val();
      },
      // Function called to change display value of element
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