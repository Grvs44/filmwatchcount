async function CompareLoad(){
    if(localStorage.filmCompare === undefined || localStorage.filmCompare === "" || localStorage.filmCompare === "[]"){
        let text1 = document.createElement("p")
        text1.innerText = "No films have been added to compare\nGo to the film list, choose some films, click the \"Add to compare\" button, then return here"
        document.getElementById("content").appendChild(text1)
    }
    else{
        let resptext = await(await fetch("filmcompare" + localStorage.filmCompare)).text()
        document.getElementById("content").innerHTML = resptext
        SetLinks()
        let savebtn = document.createElement("button")
        savebtn.innerText = "Save"
        savebtn.onclick = Save
        document.getElementById("savearea").appendChild(savebtn)
    }
}
function SetLinks(){
    if(!/android|iphone|ipad|ipod|blackberry/i.test(navigator.userAgent)){
        var links = document.getElementById("content").getElementsByTagName("a")
        for(var link of links)
            link.addEventListener("click",ObjectClick)
    }
}
function ObjectClick(e){
    e.preventDefault()
    open(e.target.href,e.target.href,"height=500,width=500")
}
function Save(e){
    let fileContent = "<html><head><title>Film Comparison</title><style>body{font-family:'Segoe UI';}</style></head><body><h1>Film Comparison</h1>"
    for(let div of document.getElementById("content").getElementsByTagName("div")){
        fileContent += "<h2>" + div.getElementsByTagName("h2")[0].innerText + "</h2>"
        let uls = div.getElementsByTagName("ul")
        let ols = div.getElementsByTagName("ol")
        for(let li of ((uls.length)? uls: ols)[0].getElementsByTagName("li")){
            fileContent += "<li>" + li.innerText + "</li>"
        }
    }
    fileContent += "</body></html>"
    let file = new File([fileContent],"Film Comparison.html",{type:"text/html;charset=utf-8"})
    saveAs(file)
}