function Filters(){
    if(document.getElementById("chk").checked) for(var link of document.getElementsByClassName("filter")) link.href += "&sub"
    else for(var link of document.getElementsByClassName("filter")) link.href = link.href.replace("&sub","")
}