$(document).ready(function(){
  var data='';

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


  
  $("#load").on('click',function(){
    parser=new DOMParser();
    xmldoc=parser.parseFromString(data,"text/xml");
    x = xmldoc.documentElement.childNodes;
    console.log(xmldoc.documentElement.nodeName);
    txt='';
    console.log("Number of child nodes= "+x.length)
    for (i = 0; i < x.length ;i++) {
        if(x[i].nodeType==1) {
          txt += x[i].nodeName +  "\n";
        }
    }
    $("#res").text(txt);
  });
  
});