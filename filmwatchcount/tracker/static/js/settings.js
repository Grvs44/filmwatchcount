function Onload(){
    document.getElementById("update").addEventListener("click",CheckUpdates)
}
async function CheckUpdates(e){
    e.target.disabled = true
    let details = await(await fetch("/pwadate")).json()
    let updated = 0
    for(let file of Object.keys(details)){
        let filename = "/" + file
        let cachematch = await caches.match(filename)
        if(cachematch === undefined){
            await UpdateFile(filename)
            updated++
        }
        else{
            if((new Date(cachematch.headers.get("date")).getTime() / 1000) < details[file]){
                await UpdateFile(filename)
                updated++
            }
        }
    }
    e.target.disabled = false
    alert(updated + " file(s) were updated")
}
async function UpdateFile(filename){
    let fileresponse = await fetch(filename)
    let contenttype = fileresponse.headers.get("content-type")
    let cache
    if(contenttype.includes("javascript"))
        cache = await caches.open("javascript")
    else if(contenttype.includes("json"))
        cache = await caches.open("json")
    else
        cache = await caches.open("offline")
    await cache.put(filename,fileresponse)
}