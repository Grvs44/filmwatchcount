let db
async function CompareLoad(){
    let openreq = indexedDB.open("fw-db",1)
    /*openreq.onsuccess = () => {
        db = openreq.result
    }*/
    openreq.onupgradeneeded = (e) => {
        db = openreq.result
        switch(e.oldVersion){
            case 0:
                db.createObjectStore("filmcompare",{keyPath:"id",autoIncrement:true})
                break
        }
    }
    if(localStorage.filmCompare === undefined || localStorage.filmCompare === ""){
        let text1 = document.createElement("p")
        text1.innerText = "No films have been added to compare\nGo to the film list, choose some films, click the \"Add to compare\" button, then return here"
        let text2 = document.createElement("p")
        text2.innerText = "Alternatively, you can view stored comparisons by selecting one below"
        let ul = document.createElement("ul")
        ul.id = "storelist"
        let button = document.createElement("button")
        button.innerText = "Search stored comparisons"
        button.onclick = SearchStored
        document.getElementById("content").append(text1,text2,ul,button)
    }
    else{
        let resptext = await(await fetch("filmcompare" + localStorage.filmCompare)).text()
        document.getElementById("content").innerHTML = resptext
        SetLinks()
        let transaction = db.transaction("filmcompare","readwrite")
        let filmcompare = transaction.objectStore("filmcompare")
        let item = {
            content:resptext,
            idlist:localStorage.filmCompare,
            title:"hello!"
        }
        let request = filmcompare.add(item)
        request.onsuccess = () => {
            console.log("item added to the store", request.result)
        }
        request.onerror = () => {
            console.log("Error", request.error)
        }
    }
}
function SetLinks(){
    var links = document.getElementById("content").getElementsByTagName("a")
    for(var link of links)
        link.addEventListener("click",ObjectClick)
}
function ObjectClick(e){
    e.preventDefault()
    open(e.target.href,e.target.href,"height=500,width=500")
}
function SearchStored(e){
    e.target.remove()
    let ul = document.getElementById("storelist")
    let transaction = db.transaction("filmcompare","readonly")
    let filmcompare = transaction.objectStore("filmcompare")
    let objects = filmcompare.getAll()
    console.log(objects)
    let li,btn
    if(objects.result.length == 0){
        li = document.createElement("li")
        li.innerText = "No stored comparisons"
        ul.appendChild(li)
    }
    else{
        for(let item of objects.result){
            li = document.createElement("li")
            btn = document.createElement("button")
            btn.innerText = item.title
            btn.comparisonid = item.id
            btn.onclick = item => StoredSelect(item.url)
            li.appendChild(btn)
            ul.appendChild(li)
        }
    }
}
async function StoredSelect(url){
    let cache = await caches.open("fw-filmcompare")
    let path = new URLPattern(url).pathname
    console.log(path)
    document.getElementById("content").innerHTML = await(await cache.match(path)).text()
    SetLinks()
}