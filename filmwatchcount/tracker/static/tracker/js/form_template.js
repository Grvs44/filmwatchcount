function Onload(){
    if(opener)
        for(var form of document.forms)
            if(form.method == "post") form.addEventListener("submit",e => {opener.shouldrefresh = true})
}