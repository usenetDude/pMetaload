
(function ($) {
jQuery.expr[':'].Contains = function(a,i,m){
  return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
};

function listFilter() {
$("#searchinput").change( function(){
  var filtertext = $(this).val();
  if (filtertext){
      $("#list").find(".sitename:not(:Contains(" + filtertext +"))").parent().hide();
      $("#list").find(".sitename:Contains(" + filtertext +")").parent().show();
  } else {
      $("#list").find(".entry").show();
  }
  return false;
})
.keyup( function(){
        $(this).change();
});
}

$(function () {
listFilter();
});
}(jQuery));