$(document).ready(function(){

  checkbox_name='MyPythonCheckbox'
  
  function generateServerURL(suffix){
    /*
      DOCSTRING:  Utility function to retrieve result-URL of Flask server-page
    */
    return 'http://localhost:5000/'+suffix;
  }

  $("#sendDataToCSV").on('click',
  function(){
    /*
      DOCSTRING:  Send the selected data over to Flask-python at backend using AJAX request
                  and finally redirect to the '/results' page
    */
    checkboxes=$('input:checkbox[name='+checkbox_name+']');
    root_tag=checkboxes[0].id;
    res_array=[['Primary_Key',''+root_tag,''+root_tag,''+root_tag],['Parent_Tag',''+root_tag,''+root_tag,''+root_tag]];
    for (i=1;i<checkboxes.length;i++){
      if(checkboxes[i].checked){
        res_array.push(['Child_Tag',''+checkboxes[i].id,''+root_tag,''+root_tag]);
      }
    }
    json_res_array={'res_array':res_array};
    console.log("Final Array is= "+json_res_array)
    $.ajax({
      type:'POST',
      url:generateServerURL('home/result'),
      data:JSON.stringify(json_res_array),
      datatype:'json',
      success:function (){
        window.location.href=generateServerURL('result')
      },
    }).done(function(){
      console.log('Your data is now sent. Data='+JSON.stringify(json_res_array));
    });
  });
  





 $(document).delegate('#root', 'click', function()
 {
   /*
    DOCSTRING:  Generic handler function for clickable hierarchy of nested checkboxes
   */
   $('input[type="checkbox"]').change(function(e) {
     var checked = $(this).prop("checked"),
       container = $(this).parent(),
       siblings = container.siblings();
   
     container.find('input[type="checkbox"]').prop({
       indeterminate: false,
       checked: checked
     });
   
     function checkSiblings(el) {
       var parent = el.parent().parent(),
         all = true;
   
       el.siblings().each(function() {
         let returnValue = (all =
           $(this)
             .children('input[type="checkbox"]')
             .prop("checked") === checked);
         return returnValue;
       });
   
       if (all && checked) {
         parent.children('input[type="checkbox"]').prop({
           indeterminate: false,
           checked: checked
         });
   
         checkSiblings(parent);
       } else if (all && !checked) {
         parent.children('input[type="checkbox"]').prop("checked", checked);
         parent
           .children('input[type="checkbox"]')
           .prop(
             "indeterminate",
             parent.find('input[type="checkbox"]:checked').length > 0
           );
         checkSiblings(parent);
       } else {
         el.parents("li")
           .children('input[type="checkbox"]')
           .prop({
             indeterminate: true,
             checked: false
           });
       }
     }
   
     checkSiblings(container);
   });
});
  
});