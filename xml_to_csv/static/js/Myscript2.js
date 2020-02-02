let i =0;
let nrepos=10;
$(document).ready(function(){
    $("#loading").css('visibility','visible');
    $("#root").css('visibility','hidden');
    $.get("https://api.github.com/repositories",function(){
        console.log("Success");
        }).done(function (json, status){
        json=json.slice(0,nrepos); //to retrive only the top 10 json object-repositories
            json.forEach(repos => {
                    //add a new row if all 3 card-positions have been filled
                    if(i%3==0)
                    {
                        let newrow= '<div id="row'+Math.floor(i/3)+'" class="row center-block">'+
                        '</div>';
                        $("#root").append(newrow);
                    }
                    //append the card element to current position
                    let description= repos.description + "";
                    if(description.length >=42)
                    {
                        description=description.substring(0,40) + "...";
                    }
                    let htmlcard = 
                        '<div class="col-md-4 ">'+
                        '<div class="card card-block" onclick="window.open(\'' +repos.html_url+ '\')">'+
                        '<img src="'+repos.owner.avatar_url+'" alt="GIT Repo Placeholder" onclick="window.open(\'' +repos.owner.html_url+ '\')">'+
                        '<h4>'+repos.name.charAt(0).toUpperCase() + repos.name.slice(1)+'</h4>'+
                        '<p>'+description+'</p>'+
                        '<h6 class="text-muted" onclick="window.open(\'' +repos.owner.html_url+ '\')">'+"-"+repos.owner.login+'</h6>'+
                        '</div>'+
                        '</div>';
                    $("#row"+Math.floor(i/3)).append(htmlcard);
                    i++;
                    if(i==nrepos){
                        $("body").css({"margin-top":"200px"});
                        $("#loading").remove();
                        $("#root").css('visibility','visible');
                    }
            });
        }).fail(function (){
        let error = 'The API call was unsuccessful!\nTry refreshing the page or open the link to check the response: \nhttps://api.github.com/repositories';
        alert(error);
    });

    $("h2","#header1").on('click',function(){
        window.open("https://www.github.com/","_blank");
    });
    $("i","#gotogithub").on('click',function(){
        window.open("https://www.github.com/","_blank");
    });

      $("#gototop").on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({scrollTop:0}, '300');
      });
      $(window).scroll(function() {
        if ($(window).scrollTop() > 300) {
          $("#gototop").addClass('show');
        } else {
          $("#gototop").removeClass('show');
        }
      });
});