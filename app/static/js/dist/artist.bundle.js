!function(t){var e={};function o(i){if(e[i])return e[i].exports;var a=e[i]={i:i,l:!1,exports:{}};return t[i].call(a.exports,a,a.exports,o),a.l=!0,a.exports}o.m=t,o.c=e,o.d=function(t,e,i){o.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},o.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},o.t=function(t,e){if(1&e&&(t=o(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(o.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)o.d(i,a,function(e){return t[e]}.bind(null,a));return i},o.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return o.d(e,"a",e),e},o.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},o.p="",o(o.s=7)}([function(t,e,o){"use strict";o.d(e,"a",function(){return i});const i={Obj:function(t){this.name=t,this.div={id:"#js-div_"+t},this.ul={class:".js-ul_"+t,html:""},this.li={class:".js-li_"+t,html:$("#js-template_"+t).html()},this.children={},this.datalist=".js-datalist_"+t,this.modal={id:"#js-modal_"+t,html:'<form id="js-form-modal_'+t+'" action="" method="POST">'+$("#js-form_"+t).html()+"</form>"},this.form={id:"#js-form_"+t,modalID:"#js-form-modal_"+t},this.post={create:"/"+t+"s/create",edit:$("form").attr("action")}},activeObject:null,createButton:[null]}},function(t,e,o){"use strict";o.d(e,"a",function(){return n});var i=o(0),a=o(2);let n={init:function(){a.a.init()},determineObject:function(t){var e=t.id.split("_")[1];return console.log("Selected object type: "+e),e},selectActiveObject:function(t){i.a.activeObject=i.a[t],console.log("New active object: "+i.a[t].name)},showSection:function(t){this.selectActiveObject(t),$(".js-create-div").hide(),$(i.a[t].div.id).show(),$(".js-submit-div").show(),this.iterateFieldlists(i.a.activeObject.form.id)},appendUL:function(t){var e=this.determineObject(t);$(t).closest(".row").nextAll("ul").append(i.a[e].li.html),this.iterateFieldlists("#"+$(t).closest("form").attr("id"))},removeLI:function(t){this.determineObject(t);$(t).closest("li").remove()},showModal:function(t){i.a.createButton.push(t),console.log("createbutton: "),console.dir(i.a.createButton);var e=this.determineObject(t);this.selectActiveObject(e),$(i.a[e].modal.id).modal("show").find("div.modal-body").html(i.a[e].modal.html),this.iterateFieldlists(i.a.activeObject.form.modalID)},valSwitch:function(t){var e,o;try{$(t+' [id^="js-datalist_"]').each(function(i){if(e=$(this).val(),console.log("Temp val: "+e),void 0===(o=$(t+" option").filter(function(){return this.value==e}).data("value")))throw e+" is not a recognized value.";console.log("ID val: "+o),$(this).val(o)})}catch(t){return n.addErrors(t),!1}},iterateFieldlists:function(t){console.log("iterate obj ID: "+t);for(const e in i.a.activeObject.children){console.log("Updating "+e+" datalists");let o=i.a.activeObject.children[e];console.log(t+" "+o.id),$.each($(t+" "+o.id),function(){console.log("ID: "+$(this).attr("id")),console.log("LENGTH: "+$(this).closest("ul").children("li").length),$(this).attr("id",$(this).attr("id")+"-"+o.count),$(this).attr("name",$(this).attr("name")+"-"+o.count),o.count++})}},popModalList:function(){let t=i.a.createButton.pop();return console.log("createbutton: "),console.dir(i.a.createButton),t},removeModal:function(t){this.popModalList(),this.selectActiveObject(a.a.getVal())},submitModal:function(t){var e=this.determineObject(t);this.postData(i.a[e],i.a[e].form.modalID,i.a[e].post.create).done(function(t){if(0==t.success)for(var o in console.log("Form Error(s)!"),console.dir(t),t.data)console.log("ITEM: "+o),n.addErrors(o+": "+t.data[o]);else{console.log("Form Sucess!"),console.dir(t),n.addSuccess("Success! Created "+t.data.name+"!"),i.a[e].li.html=n.updateTemplate(i.a[e].li.html,t.data);try{$("#"+i.a[e].name+"s").each(function(e){$(this).append('<option data-value="'+t.data.id+'" value="'+t.data.name+'"></option>')})}catch(t){console.log("Catch: "+t)}a.a.closeModal(),n.selectActiveObject(a.a.getVal())}}).fail(function(t){console.log("AJAX error!"),console.dir(t)})},submitForm:function(t){console.log("submitForm form ID: "+i.a.activeObject.form.id),console.log("submitForm form post route: "+i.a.activeObject.post),this.postData(i.a.activeObject,i.a.activeObject.form.id,i.a.activeObject.post.create).done(function(t){if(0==t.success)for(var e in console.log("Form Error(s)!"),console.dir(t),t.data)console.log("ITEM: "+e),n.addErrors(e+": "+t.data[e]);else{console.log("Form Sucess!"),console.dir(t),n.addSuccess("Success! Created "+t.data.name+"!"),i.a.activeObject.li.html=n.updateTemplate(i.a.activeObject.li.html,t.data);try{$("#"+i.a.activeObject.name+"s").each(function(e){$(this).append('<option data-value="'+t.data.id+'" value="'+t.data.name+'"></option>')})}catch(t){console.log("Catch: "+t)}$(i.a.activeObject.form.id).trigger("reset")}})},submitUpdate:function(t){if(null===i.a.activeObject){var e=this.determineObject(t);this.selectActiveObject(e)}console.dir(i.a.activeObject),this.postData(i.a.activeObject,i.a.activeObject.form.id,i.a.activeObject.post.edit).done(function(t){if(null==t.success)console.log("Unexpected response! "+t),location.assign("/login");else if(0==t.success)for(var e in console.log("Form Error(s)!"),console.dir(t),t.data)console.log("ITEM: "+e),n.addErrors(e+": "+t.data[e]);else 1==t.success&&(console.log("Form Sucess!"),window.location.reload(!0))})},postData:function(t,e,o){return console.log("Form ID: "+e),console.log("Post data: "+$(e).serialize()),console.log("Post route: "+o),$.ajax({url:o,data:$(e).serialize(),type:"POST"})},retrieveResponse:function(t){},addErrors:function(t){var e=$("<div/>");$(e).html($("#js-template_error").html()).find(".js-error-notice").append(t),$(".js-alert").append($(e).html())},addSuccess:function(t){var e=$("<div/>");$(e).html($("#js-template_success").html()).find(".js-success-message").append(t),$(".js-alert").append($(e).html())},addCreatedItem:function(t){},selectCreatedItem:function(t){},updateTemplate:function(t,e){var o=document.createElement("div");return $(o).html(t),$(o).find("datalist").append('\t<option data-value="'+e.id+'" value="'+e.name+'"></option>'),$(o).html()},toggleInputs:function(t){var e=this.determineObject(t);this.selectActiveObject(e),$(i.a[e].form.id).find(":input").not(":button").each(function(){$(this).attr("readonly",!1),$(this).attr("disabled",!1),$(this).toggleClass("form-control-plaintext").toggleClass("form-control")}),$(i.a[e].form.id).find(".d-none").each(function(){$(this).toggleClass("d-none")}),$(i.a[e].form.id).find(".is-active").each(function(){$(this).toggleClass("is-active").toggleClass("d-none")}),$(t).addClass("invisible"),this.iterateFieldlists(i.a.activeObject.form.id)},showLogin:function(t){$("body").append(t),$("#js-modal_login").modal("show")},getLogout:function(){console.log("Logout clicked!"),$.get("/logout",function(t){console.log(t),n.addSuccess(t)})}}},function(t,e,o){"use strict";o.d(e,"a",function(){return a});var i=o(1);let a={init:function(){this.hideDivs(),this.selectForm(),this.addLI(),this.deleteLI(),this.createModal(),this.cancelModal(),this.postForm(),this.postModal(),this.editForm(),this.cancelForm(),this.updateForm(),this.logoutUser()},hideDivs:function(){$(".js-create-div").hide(),$(".js-submit-div").hide()},getVal:function(){return $("#js-create_object").val()},selectForm:function(){$("#js-create_object").change(function(t){i.a.showSection(a.getVal())})},addLI:function(){$("body").on("click",".js-add-li",function(t){t.preventDefault(),i.a.appendUL(this)})},deleteLI:function(){$("body").on("click",".js-delete-li",function(t){t.preventDefault(),$(this).closest("li").remove()})},createModal:function(){$("body").on("click",".js-create-modal",function(t){t.preventDefault(),i.a.showModal(this)})},cancelModal:function(){$(".modal").on("hide.bs.modal",function(t){i.a.removeModal(this)})},closeModal:function(){$(".modal").modal("hide"),i.a.removeModal(this)},postModal:function(){$("body").on("click",".js-post-modal",function(t){t.preventDefault(),i.a.submitModal(this)})},postForm:function(){$("body").on("click",".js-post-form",function(t){t.preventDefault(),i.a.submitForm(this)})},editForm:function(){$(".js-form-edit").on("click",function(t){i.a.toggleInputs(this)})},updateForm:function(){$("body").on("click",".js-update-form",function(t){t.preventDefault(),i.a.submitUpdate(this)})},cancelForm:function(){$(".js-cancel-form").on("click",function(t){window.location.reload(!0)})},logoutUser:function(){$("#js-logout").on("click",function(t){i.a.getLogout()})}}},,,,,function(t,e,o){"use strict";o.r(e);var i=o(1),a=o(0);o(2);a.a.artist=new a.a.Obj("artist"),a.a.artwork=new a.a.Obj("artwork"),a.a.artist.children={artwork:{count:$(".js-datalist_artwork").length+1,class:".js-datalist_artwork",id:"#js-datalist_artwork"}},i.a.init()}]);