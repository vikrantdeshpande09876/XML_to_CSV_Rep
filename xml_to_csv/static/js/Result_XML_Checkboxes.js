$(document).ready(function(){
  array=JSON.parse($("#result_xml_checkboxes").text());
  x="";
  $("#sample").text(typeof(array));
  $("#sample").append(array);
  
});