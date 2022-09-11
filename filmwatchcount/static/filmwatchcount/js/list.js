var shouldrefresh = false
function Onload(){
    addEventListener("focus",e => {if(shouldrefresh) location.reload()})
    if(!/android|iphone|ipad|ipod|blackberry/i.test(navigator.userAgent)){
        document.getElementById("add").addEventListener("click",ObjectClick)
        var list = document.getElementById("objectlist")
        for(var li of list.children)
            li.getElementsByTagName("a")[0].addEventListener("click",ObjectClick)
    }
}
function ObjectClick(e){
    e.preventDefault()
    if(e.target.tagName == "BUTTON") var href = e.target.parentElement.href
    else var href = e.target.href
    open(href,href,"height=500,width=500")
}