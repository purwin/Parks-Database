!function(t){function e(e){for(var n,a,l=e[0],i=e[1],c=e[2],d=0,p=[];d<l.length;d++)a=l[d],s[a]&&p.push(s[a][0]),s[a]=0;for(n in i)Object.prototype.hasOwnProperty.call(i,n)&&(t[n]=i[n]);for(u&&u(e);p.length;)p.shift()();return r.push.apply(r,c||[]),o()}function o(){for(var t,e=0;e<r.length;e++){for(var o=r[e],n=!0,l=1;l<o.length;l++){var i=o[l];0!==s[i]&&(n=!1)}n&&(r.splice(e--,1),t=a(a.s=o[0]))}return t}var n={},s={5:0},r=[];function a(e){if(n[e])return n[e].exports;var o=n[e]={i:e,l:!1,exports:{}};return t[e].call(o.exports,o,o.exports,a),o.l=!0,o.exports}a.m=t,a.c=n,a.d=function(t,e,o){a.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:o})},a.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},a.t=function(t,e){if(1&e&&(t=a(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var o=Object.create(null);if(a.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)a.d(o,n,function(e){return t[e]}.bind(null,n));return o},a.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return a.d(e,"a",e),e},a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},a.p="";var l=window.webpackJsonp=window.webpackJsonp||[],i=l.push.bind(l);l.push=e,l=l.slice();for(var c=0;c<l.length;c++)e(l[c]);var u=i;r.push([14,0]),o()}({14:function(t,e,o){"use strict";o.r(e),function(t){var e=o(1);t(document).ready(function(){!function(){let o={columns:[],activeObject:null,result:[],routeExport:"/export",key:t("#js-template_keys").html(),exhibition:{name:"exhibition",li:t("#js-template_exhibition").html(),class:".js-column_exhibition"},artwork:{name:"artwork",li:t("#js-template_artwork").html(),class:".js-column_artwork"},park:{name:"park",li:t("#js-template_park").html(),class:".js-column_park"},artist:{name:"artist",li:t("#js-template_artist").html(),class:".js-column_artist"},org:{name:"org",li:t("#js-template_org").html(),class:".js-column_org"}},n={init:function(){s.init()},sendFile:function(e){this.postFile(t(e),t(e).attr("action")).done(function(e){if(console.log(e),0==e.success)console.log("Form Error(s)!"),console.dir(e),n.iterateErrors(e);else if(1==e.success){o.columns=e.data;for(const n of e.data)o.key=t(o.key).append(t("<option></option>").attr("value",n).text(n));console.log(o.columns),n.buildUL(),s.toggleVisible(t("#js-import_data")),t("#data_file").remove(),t("#file_file").clone().attr("id","data_file").addClass("d-none").appendTo("#js-import_data_ul")}else console.log("Don't know what to do!"),console.dir(e)})},sendData:function(e){this.postFile(t(e),t(e).attr("action")).done(function(t){if(0==t.success)console.log("Form Error(s)!"),console.dir(t),n.iterateErrors(t);else if(1==t.success){o.result=t,console.log(o.result);let e=o.result.data.reduce((t,e)=>(1==e.success?t.success++:t.error++,e.warning.length>0&&t.warning++,t),{success:0,warning:0,error:0});console.dir(e),s.showModal(`<h3>\n                ${o.activeObject.name.toUpperCase()} IMPORT RESULTS\n              </h3>\n              <ul>\n                <li>Records imported: ${e.success}</li>\n                <li>Records with warnings: ${e.warning}</li>\n                <li>Records with errors: ${e.error}</li>\n              </ul>`)}else console.log("Don't know what to do!"),console.dir(t)})},sendExport:function(){this.postExport(o.routeExport,o.result.data).done(function(t){console.log("EXPORT DONE!"),console.log(t)})},buildUL:function(){t("#js-data_ul").html(),o.columns.forEach(function(e){t("#js-data_ul").append(`<li \n              class="[ row mb-3 align-items-baseline justify-content-center ]"\n             >\n              <div class="js-key">${t(o.key)[0].outerHTML}</div>\n              <div class="[ px-3 ]">\n                <i class="fas fa-arrow-right c-blue--l"></i>\n              </div>\n              <div class="js-value"></div>\n            </li>`)}),n.appendNameList(".js-column_key")},appendNameList:function(e){t(e).each(function(e){t(this).attr("name",t(this).attr("name")+"-"+(e+1))})},changeObject:function(e){o.activeObject=o[e],console.log(o.activeObject),t(".js-value").each(function(){t(this).html(o.activeObject.li)}),n.appendNameList(o.activeObject.class)},postFile:function(e,o){console.log("Post route: "+o);let n=new FormData(t(e)[0]);return console.log(n),t.ajax({type:"POST",url:o,processData:!1,contentType:!1,data:n})},iterateErrors:function(t){for(const o in t.data)console.log("ERROR ITEM: "+o),e.a.addErrors(o+": "+t.data[o])},postExport:function(e,o){let n=t("meta[name=csrf-token]").attr("content");return t.ajaxSetup({beforeSend:function(t,e){/^(GET|HEAD|OPTIONS|TRACE)$/i.test(e.type)||this.crossDomain||t.setRequestHeader("X-CSRFToken",n)}}),t.ajax({url:e,type:"POST",contentType:"application/json; charset=utf-8",dataType:"json",data:JSON.stringify(o),processData:!1,success:(t,e,o)=>{console.log("jqXhr: ",jqXhr),console.log("textStatus: ",e),console.log("errorThrown: ",errorThrown)},error:(t,e,o)=>{console.log("jqXhr: ",t),console.log("textStatus: ",e),console.log("errorThrown: ",o)}})}},s={init:function(){this.sendFile(),this.sendData(),this.changeObject(),this.sendExport()},sendFile:function(){t("#js-post_file").on("click",function(e){e.preventDefault(),n.sendFile(t("#js-form_import_file"))})},sendData:function(){t("#js-post_data").on("click",function(e){e.preventDefault(),n.sendData(t("#js-form_import_data"))})},changeObject:function(){t("#class_object").change(function(e){let o=s.getVal();o&&(n.changeObject(o),t("#js-data_ul").removeClass("d-none"))})},getVal:function(){return t("#class_object").val()},toggleVisible:function(e){t(e).removeClass("d-none")},showModal:function(e){t("#js-modal_results").modal("show").find("div.modal-body").html(e)},sendExport:function(){t("#js-modal-post_export").on("click",function(t){t.preventDefault(),n.sendExport()})}};n.init()}()})}.call(this,o(2))}});
//# sourceMappingURL=import.bundle.js.map