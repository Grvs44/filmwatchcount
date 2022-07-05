function Onload(){
    var list = document.getElementById("objectlist").children
    for(var li of list)
        li.getElementsByTagName("a")[0].addEventListener("click",ObjectClick)
}
function ObjectClick(e){
    e.preventDefault()
    open(e.target.href,e.target.href,"height=500,width=500")
}