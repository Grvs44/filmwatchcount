function Back(){
    history.back()
    if(opener) close()
}
function CheckBack(onload=null){
    if(history.state == 0 || history.length == 1 && !opener){
        history.pushState(0,location.href)
        document.getElementById("back").remove()
    }
    if(onload) onload()
}