let updateHeaders = new Headers()
updateHeaders.append("pragma","no-cache")
async function CheckUpdates(){
    let updated = false
    let details = await(await fetch("/pwadate",{headers:updateHeaders})).json()
    for(let file of Object.keys(details)){
        let filename = "/" + file
        let cachematch = await caches.match(filename)
        if(cachematch === undefined){
            updated = true
            await UpdateFile(filename)
        }
        else{
            let date = (new Date(cachematch.headers.get("date")).getTime() / 1000)
            if(date < details[file]){
                updated = true
                await UpdateFile(filename)
            }
        }
    }
    localStorage.lastUpdate = Date.now()
    return updated
}
async function UpdateFile(filename){
    let fileresponse = await fetch(filename,{headers:updateHeaders})
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
async function AutoUpdate(){
    if(localStorage && localStorage.lastUpdate){
        let last = Number(localStorage.lastUpdate)
        if(Date.now() >= 14400000 + last) return await CheckUpdates()
        else localStorage.lasUpdate = Date.now()
    }
    else return await CheckUpdates()
    return false
}
export {CheckUpdates,AutoUpdate}