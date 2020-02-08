$(document).ready(function(){
  array=JSON.parse($("#result_xml_checkboxes").text());
  x="";
  $("#sample").text(array)
  for (i=0;i<array.length;i++){
    $("#sample").append(array[i]+"\n");
  }
});