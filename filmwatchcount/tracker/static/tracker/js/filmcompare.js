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
        let graphbtn = document.createElement("button")
        graphbtn.innerText = "Show graph"
        graphbtn.onclick = ToggleGraph
        document.body.appendChild(graphbtn)
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
    e.target.disabled = true
    e.target.innerText = "Saving"
    let content = document.createElement("body")
    content.innerHTML = "<h1>Film Comparison</h1>" + document.getElementById("content").innerHTML
    let graph = document.getElementById("graph")
    if(graph && graph.style.display === "block") content.innerHTML += graph.innerHTML
    let anchors = content.getElementsByTagName("a")
    while(anchors.length){
        anchors[0].outerHTML = anchors[0].innerHTML
    }
    let fileContent = "<!DOCTYPE html><html><head><title>Film Comparison</title><style>body{font-family:'Segoe UI';}</style></head>" + content.outerHTML + "</html>"
    let file = new File([fileContent],"Film Comparison.html",{type:"text/html;charset=utf-8"})
    saveAs(file)
    setTimeout(RestoreSave,2000,e.target)
}
function RestoreSave(btn){
    btn.innerText = "Save"
    btn.disabled = false
}
async function ToggleGraph(e){
    let graph = document.getElementById("graph")
    if(graph){
        if(graph.style.display === "block"){
            graph.style.display = "none"
            e.target.innerText = "Show graph"
        }
        else{
            graph.style.display = "block"
            e.target.innerText = "Hide graph"
        }
    }
    else{
        graph = document.createElement("div")
        graph.id = "graph"
        graph.innerHTML = await(await fetch("filmcomparegraph")).text()
        document.body.appendChild(graph)
        e.target.innerText = "Hide graph"
    }
}