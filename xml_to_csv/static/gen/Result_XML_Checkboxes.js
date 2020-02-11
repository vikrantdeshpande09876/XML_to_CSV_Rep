$(document).ready(function(){
  var temp_depth=0;
  var checkbox_name='dynamicCheckbox';


  /*
    DOCSTRING:  Utility function to retrieve result-URL of Flask server-page
  */
  function generateServerURL(suffix){
    return 'http://localhost:5000/'+suffix;
  }



  /*
    DOCSTRING:  Handler for Input Field for file- #fileid
  */
  $("#fileid").on('change',function(){
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
      alert('The File APIs are not fully supported in this browser.');
      return;
    }
    var filereader=new FileReader();
    filereader.onload=function() {
      data=filereader.result;
      console.log("You're file contains this data: \n"+data)
    };
    filereader.readAsText($("#fileid").prop('files')[0]);
  });



  /*
    DOCSTRING:  Depth First Search (DFS) implementation for displaying hierarchical unordered lists of XML tag-names.
                Need to make the IDs of checkboxes as concatenated tag-names of parents
  */
  function depthFirst(node, parser, depth, tagname) {
    if(!parser || !node){
      return;
    }
    if (tagname!=''){
      tempid+='.'+node.nodeName;
    }
    else {
      tempid=node.nodeName
    }
    text='<li><input type="checkbox" name="'+checkbox_name+'" id="'+tempid+'">'+
                        '<label for="'+tempid+'"><b>'+node.nodeName+'</b></label>';
    if (depth>temp_depth){
      text='<ul>'+text;
    }
    temp_depth=depth;
    console.log(node.nodeName + ': has Depth: '+depth + ', Temp_Depth: '+temp_depth+' and id='+ tempid );
    for(child of node.childNodes){
      if(child.nodeType === 3){
        continue;
      }
      text += depthFirst(child, parser, depth+1,tempid+'.'+child.nodeName);
    }
    if (depth<temp_depth) {
      while(depth!=temp_depth){
        text+='</ul>';
        temp_depth-=1;
      }
    }
    text+='</li>';
    return text;
  }



  /*
    DOCSTRING:  Handler to load file into code for button- #load
                Use the DOMParser to parse the text/xml file that user selected, into an XMLdocument object.
                Then execute the above DFS algorithm to generate the nested XML tags as HTML checkboxes.
  */
  $("#load").on('click',function(){
    if($("input[name='ftype']:checked").val()=='XML'){
      parser=new DOMParser();
      xmldoc=parser.parseFromString(data,"text/xml");
      xml = xmldoc.documentElement;
      checkboxHTML='';
      try {
        checkboxHTML='<ul>'+depthFirst(xml,parser,0,'')+'</ul>';
      } catch (error) {
        checkboxHTML='<br>Could not parse the XML File!';
        alert('Could not parse the XML File: '+error);
      }
      $("#res").html(checkboxHTML);
    }
    else {
      $("#res").html('<br>You still need to handle this part of the code for XSD files!');
      alert('<br>You still need to handle this part of the code for XSD files');
    }
  });

  


  /*
    DOCSTRING:  Send the selected data over to Flask-python at backend using AJAX request
                Need to make the IDs of checkboxes as concatenated tag-names of parents
  */
  $("#sendDataToFlask").on('click',function(){
    checkboxes=$('input:checkbox[name='+checkbox_name+']');
    res_array=[];
    for (i=0;i<checkboxes.length;i++){
      if(checkboxes[i].checked){
        //console.log(i+') '+checkboxes[i].id);
        res_array.push([checkboxes[i].id,i+'']);
      }
    }
    json_res_array={'res_array':res_array};
    $.ajax({
      type:'POST',
      url:generateServerURL('result'),
      data:JSON.stringify(json_res_array),
      datatype:'json'
    }).done(function(){
      console.log('Your data is now sent. Data='+JSON.stringify(json_res_array));
    });
  });
  



  /*
    DOCSTRING:  Generic handler function for clickable hierarchy of nested checkboxes
  */
  $(document).delegate('#res', 'click', function()
  {
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