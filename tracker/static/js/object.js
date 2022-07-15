function Back(){
    if(opener && history.state == 1) close()
    else history.back()
}
function CheckBack(onload=null){
    if (opener && history.length == 1) history.pushState(1,location.href)
    else if(history.state == 0 || history.length == 1 && !opener){
        history.pushState(0,location.href)
        document.getElementById("back").remove()
    }
    if(onload) onload()
}