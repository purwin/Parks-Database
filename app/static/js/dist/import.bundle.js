!function(t){var e={};function o(i){if(e[i])return e[i].exports;var n=e[i]={i:i,l:!1,exports:{}};return t[i].call(n.exports,n,n.exports,o),n.l=!0,n.exports}o.m=t,o.c=e,o.d=function(t,e,i){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},o.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(o.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)o.d(i,n,function(e){return t[e]}.bind(null,n));return i},o.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="",o(o.s=10)}([function(t,e,o){"use strict";o.d(e,"a",function(){return i});const i={Obj:function(t){this.name=t,this.div={id:"#js-div_"+t},this.ul={class:".js-ul_"+t,html:""},this.li={class:".js-li_"+t,html:$("#js-template_"+t).html()},this.children={},this.datalist=".js-datalist_"+t,this.modal={id:"#js-modal_"+t,html:'<form id="js-form-modal_'+t+'" action="" method="POST">'+$("#js-form_"+t).html()+"</form>"},this.form={id:"#js-form_"+t,modalID:"#js-form-modal_"+t},this.post={create:"/"+t+"s/create",edit:$("form").attr("action")}},activeObject:null,createButton:[null]}},function(t,e,o){"use strict";o.d(e,"a",function(){return a});var i=o(0),n=o(2);let a={init:function(){n.a.init()},determineObject:function(t){return t.id.split("_")[1]},selectActiveObject:function(t){i.a.activeObject=i.a[t]},showSection:function(t){this.selectActiveObject(t),$(".js-create-div").hide(),$(i.a[t].div.id).show(),$(".js-submit-div").show(),this.iterateFieldlists(i.a.activeObject.form.id)},appendUL:function(t){var e=this.determineObject(t);$(t).closest(".row").nextAll("ul").append(i.a[e].li.html),this.iterateFieldlists("#"+$(t).closest("form").attr("id"))},removeLI:function(t){this.determineObject(t);$(t).closest("li").remove()},showModal:function(t){i.a.createButton.push(t);var e=this.determineObject(t);this.selectActiveObject(e),$(i.a[e].modal.id).modal("show").find("div.modal-body").html(i.a[e].modal.html),this.iterateFieldlists(i.a.activeObject.form.modalID)},valSwitch:function(t){var e,o;try{$(t+' [id^="js-datalist_"]').each(function(i){if(e=$(this).val(),void 0===(o=$(t+" option").filter(function(){return this.value==e}).data("value")))throw e+" is not a recognized value.";$(this).val(o)})}catch(t){return a.addErrors(t),!1}},iterateFieldlists:function(t){for(const e in i.a.activeObject.children){let o=i.a.activeObject.children[e];$.each($(t+" "+o.id),function(){$(this).attr("id",$(this).attr("id")+"-"+o.count),$(this).attr("name",$(this).attr("name")+"-"+o.count),o.count++})}},popModalList:function(){return i.a.createButton.pop()},removeModal:function(t){this.popModalList(),this.selectActiveObject(n.a.getVal())},submitModal:function(t){var e=this.determineObject(t);this.postData(i.a[e],i.a[e].form.modalID,i.a[e].post.create).done(function(t){if(0==t.success)for(var o in t.data)a.addErrors(o+": "+t.data[o]);else{a.addSuccess("Success! Created "+t.data.name+"!"),i.a[e].li.html=a.updateTemplate(i.a[e].li.html,t.data);try{$("#"+i.a[e].name+"s").each(function(e){$(this).append('<option data-value="'+t.data.id+'" value="'+t.data.name+'"></option>')})}catch(t){console.log("Catch: "+t)}n.a.closeModal(),a.selectActiveObject(n.a.getVal())}}).fail(function(t){console.dir(t)})},submitForm:function(t){this.postData(i.a.activeObject,i.a.activeObject.form.id,i.a.activeObject.post.create).done(function(t){if(0==t.success)for(var e in console.dir(t),t.data)a.addErrors(e+": "+t.data[e]);else{a.addSuccess("Success! Created "+t.data.name+"!"),i.a.activeObject.li.html=a.updateTemplate(i.a.activeObject.li.html,t.data);try{$("#"+i.a.activeObject.name+"s").each(function(e){$(this).append('<option data-value="'+t.data.id+'" value="'+t.data.name+'"></option>')})}catch(t){console.log("Catch: "+t)}$(i.a.activeObject.form.id).trigger("reset")}})},submitUpdate:function(t){if(null===i.a.activeObject){var e=this.determineObject(t);this.selectActiveObject(e)}this.postData(i.a.activeObject,i.a.activeObject.form.id,i.a.activeObject.post.edit).done(function(t){if(null==t.success)location.assign("/login");else if(0==t.success)for(var e in console.dir(t),t.data)a.addErrors(e+": "+t.data[e]);else 1==t.success&&window.location.reload(!0)})},postData:function(t,e,o){return $.ajax({url:o,data:$(e).serialize(),type:"POST"})},retrieveResponse:function(t){},addErrors:function(t){var e=$("<div/>");$(e).html($("#js-template_error").html()).find(".js-error-notice").append(t),$(".js-alert").append($(e).html())},addSuccess:function(t){var e=$("<div/>");$(e).html($("#js-template_success").html()).find(".js-success-message").append(t),$(".js-alert").append($(e).html())},addCreatedItem:function(t){},selectCreatedItem:function(t){},updateTemplate:function(t,e){var o=document.createElement("div");return $(o).html(t),$(o).find("datalist").append('\t<option data-value="'+e.id+'" value="'+e.name+'"></option>'),$(o).html()},toggleInputs:function(t){var e=this.determineObject(t);this.selectActiveObject(e),$(i.a[e].form.id).find(":input").not(":button").each(function(){$(this).attr("readonly",!1),$(this).attr("disabled",!1),$(this).toggleClass("form-control-plaintext").toggleClass("form-control")}),$(i.a[e].form.id).find(".d-none").each(function(){$(this).toggleClass("d-none")}),$(i.a[e].form.id).find(".is-active").each(function(){$(this).toggleClass("is-active").toggleClass("d-none")}),$(t).addClass("invisible"),this.iterateFieldlists(i.a.activeObject.form.id)},showLogin:function(t){$("body").append(t),$("#js-modal_login").modal("show")},getLogout:function(){$.get("/logout",function(t){a.addSuccess(t)})}}},function(t,e,o){"use strict";o.d(e,"a",function(){return n});var i=o(1);let n={init:function(){this.hideDivs(),this.selectForm(),this.addLI(),this.deleteLI(),this.createModal(),this.cancelModal(),this.postForm(),this.postModal(),this.editForm(),this.cancelForm(),this.updateForm(),this.logoutUser()},hideDivs:function(){$(".js-create-div").hide(),$(".js-submit-div").hide()},getVal:function(){return $("#js-create_object").val()},selectForm:function(){$("#js-create_object").change(function(t){i.a.showSection(n.getVal())})},addLI:function(){$("body").on("click",".js-add-li",function(t){t.preventDefault(),i.a.appendUL(this)})},deleteLI:function(){$("body").on("click",".js-delete-li",function(t){t.preventDefault(),$(this).closest("li").remove()})},createModal:function(){$("body").on("click",".js-create-modal",function(t){t.preventDefault(),i.a.showModal(this)})},cancelModal:function(){$(".modal").on("hide.bs.modal",function(t){i.a.removeModal(this)})},closeModal:function(){$(".modal").modal("hide"),i.a.removeModal(this)},postModal:function(){$("body").on("click",".js-post-modal",function(t){t.preventDefault(),i.a.submitModal(this)})},postForm:function(){$("body").on("click",".js-post-form",function(t){t.preventDefault(),i.a.submitForm(this)})},editForm:function(){$(".js-form-edit").on("click",function(t){i.a.toggleInputs(this)})},updateForm:function(){$("body").on("click",".js-update-form",function(t){t.preventDefault(),i.a.submitUpdate(this)})},cancelForm:function(){$(".js-cancel-form").on("click",function(t){window.location.reload(!0)})},logoutUser:function(){$("#js-logout").on("click",function(t){i.a.getLogout()})}}},,,,,,,,function(t,e,o){"use strict";o.r(e);var i=o(1);$(document).ready(function(){!function(){let t={columns:[],activeObject:null,result:[],routeExport:"/export",key:$("#js-template_keys").html(),exhibition:{name:"exhibition",li:$("#js-template_exhibition").html(),class:".js-column_exhibition"},artwork:{name:"artwork",li:$("#js-template_artwork").html(),class:".js-column_artwork"},park:{name:"park",li:$("#js-template_park").html(),class:".js-column_park"},artist:{name:"artist",li:$("#js-template_artist").html(),class:".js-column_artist"},org:{name:"org",li:$("#js-template_org").html(),class:".js-column_org"}},e={init:function(){o.init()},sendFile:function(i){this.postFile($(i),$(i).attr("action")).done(function(i){0==i.success?e.iterateErrors(i):1==i.success?(t.columns=i.data,t.key=$("#js-template_keys").html(),e.iterateKeys(i.data),o.refreshMap(),e.buildUL(),o.showItem($("#js-import_data")),$("#data_file").remove(),$("#file_file").clone().attr("id","data_file").addClass("d-none").appendTo("#js-import_data_ul")):(console.log("Don't know what to do!"),console.dir(i))})},sendData:function(i){this.postFile($(i),$(i).attr("action")).done(function(i){if(0==i.success)e.iterateErrors(i.data);else if(1==i.success){t.result=i;const n=e.iterateResults(t.result.data);o.showModal(`<h3 class="[ my-4 ]">\n                ${t.activeObject.name.toUpperCase()} IMPORT RESULTS\n              </h3>\n              <ul>\n                <li>Records imported: ${n.success}</li>\n                <li>Records with warnings: ${n.warning}</li>\n                <li>Records with errors: ${n.error}</li>\n              </ul>\n              <h3 class="[ my-4 ]">EXPORT RESULTS?</h3>`),o.clearLoading()}else console.log("Don't know what to do!"),console.dir(i)})},sendExport:function(e){$("#export_data").val(JSON.stringify(t.result.data)),$(e).closest("form").submit(),o.closeModal()},buildUL:function(){t.columns.forEach(function(e){$("#js-data_ul").append(`<li \n              class="[ row mb-4 align-items-baseline justify-content-center ]"\n             >\n              <div class="js-key [ col ]">\n                ${$(t.key)[0].outerHTML}\n              </div>\n              <div class="[ px-3 col-12 col-md-1 text-center ]">\n                <i class="fas fa-arrow-right c-blue--l arrow-import"></i>\n              </div>\n              <div class="js-value [ col ]"></div>\n            </li>`)}),e.appendNameList(".js-column_key")},appendNameList:function(t){$(t).each(function(t){$(this).attr("name",$(this).attr("name")+"-"+(t+1))})},changeObject:function(o){t.activeObject=t[o],console.log(t.activeObject),$(".js-value").each(function(){$(this).html(t.activeObject.li)}),e.appendNameList(t.activeObject.class)},postFile:function(t,e){console.log("Post route: "+e);let o=new FormData($(t)[0]);return $.ajax({type:"POST",url:e,processData:!1,contentType:!1,data:o})},iterateErrors:function(t){for(const e in t.data)console.log("ERROR ITEM: "+e),i.a.addErrors(e+": "+t.data[e])},iterateKeys:function(e){for(const o of e)t.key=$(t.key).append($("<option></option>").attr("value",o).text(o))},iterateResults:function(t){return t.reduce((t,e)=>(1==e.success?t.success++:t.error++,e.warning.length>0&&t.warning++,t),{success:0,warning:0,error:0})},resetImport:function(){t.columns=[],t.activeObject=null,t.result=[],t.key=$("#js-template_keys").html(),$("#file_text").html(""),console.log("file text: ",$("#file_text").html())}},o={init:function(){this.sendFile(),this.sendData(),this.changeObject(),this.closeModal(),this.sendExport(),this.selectFile()},sendFile:function(){$("#js-post_file").on("click",function(t){t.preventDefault(),e.sendFile($("#js-form_import_file"))})},sendData:function(){$("#js-post_data").on("click",function(t){t.preventDefault(),e.sendData($("#js-form_import_data")),o.addLoading()})},changeObject:function(){$("#class_object").change(function(t){let i=o.getVal();i&&(e.changeObject(i),$("#js-data_ul").removeClass("d-none"))})},getVal:function(){return $("#class_object").val()},selectFile:function(){$(document).on("change","#file_file",function(t){console.log("changing file!"),$("#file_text").html(this.files[0].name)})},showItem:function(t){$(t).removeClass("d-none")},hideItem:function(t){$(t).addClass("d-none")},showModal:function(t){$("#js-modal_results").modal("show").find("div.modal-body").html(t)},closeModal:function(){$("#js-modal_results").modal("hide"),$("#js-modal_results").on("hidden.bs.modal",function(t){console.log("resetModal!"),o.resetImport()})},sendExport:function(){$("#js-modal-post_export").on("click",function(t){t.preventDefault(),e.sendExport(this)})},resetImport:function(){o.hideItem("#js-import_data"),$("#file_file").trigger("reset"),$("#js-form_import_file").trigger("reset"),$("#js-form_import_data").trigger("reset"),$("#js-form_export").trigger("reset"),o.refreshMap(),o.clearLoading(),e.resetImport()},refreshMap:function(){$("#class_object").val(""),$("#js-data_ul").empty().addClass("d-none")},addLoading:function(){$(".js-cancel-import, .js-post-import").prop("disabled",!0),o.showItem("#js-post_loading"),$(".js-spinner").addClass("is-spinning"),o.hideItem("#js-post_label")},clearLoading:function(){$(".js-cancel-import, .js-post-import").prop("disabled",!1),o.hideItem("#js-post_loading"),o.showItem("#js-post_label")}};e.init()}()})}]);