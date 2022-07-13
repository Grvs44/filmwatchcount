var shouldrefresh = false
function Onload(){
    document.getElementById("add").addEventListener("click",ObjectClick)
    addEventListener("focus",e => {if(shouldrefresh) location.reload()})
    var list = document.getElementById("objectlist").children
    for(var li of list)
        li.getElementsByTagName("a")[0].addEventListener("click",ObjectClick)
}
function ObjectClick(e){
    e.preventDefault()
    if(e.target.tagName == "BUTTON") var href = e.target.parentElement.href
    else var href = e.target.href
    open(href,href,"height=500,width=500")
}