let compareList, id, added = false
function FilmLoad(){
    let comparebtn = document.getElementById("addcompare")
    comparebtn.onclick = CompareClick
    id = Number(document.getElementsByName("fw-filmid")[0].content)
    compareList = (localStorage.filmCompare === undefined)? []: JSON.parse(localStorage.filmCompare)
    if(compareList.includes(id)){
        comparebtn.innerText = "Remove from comparison"
        added = true
    }
}
function CompareClick(e){
    if(added){
        compareList.pop(compareList.indexOf(id))
        e.target.innerText = "Add to compare"
    }
    else{
        compareList.push(id)
        e.target.innerText = "Remove from comparison"
    }
    localStorage.filmCompare = JSON.stringify(compareList)
    added = !added
}
