import fileCache from "./filecache.json" assert {type:"json"}
async function CheckUpdates(){
    let updateHeaders = new Headers()
    updateHeaders.append("pragma","no-cache")
    let updated = false
    let details = await(await fetch("pwadate",{headers:updateHeaders})).json()
    for(let file of details){
        let cachename = fileCache[file[0]]
        let cache = await caches.open((cachename === undefined)? "fw-offline": "fw-" + cachename)
        let cachematch = await cache.match(file[0])
        if(cachematch === undefined || (new Date(cachematch.headers.get("date")).getTime() / 1000) < file[1]){
            updated = true
            if(file[0].endsWith("-sw.js")){
                await cache.delete(file[0])
                navigator.serviceWorker.getRegistrations().then(function(registrations){
                    if(registrations.length)
                      for(let registration of registrations)
                        registration.unregister()
                });
            }
            else{
                let fileresponse = await fetch(file[0],{headers:updateHeaders})
                await cache.put(file[0],fileresponse)
            }
        }
    }
    let now = Date.now()
    if(updated) localStorage.fw_lastUpdate = now
    localStorage.fw_lastCheck = now
    return updated
}
async function AutoUpdate(){
    if(localStorage && localStorage.fw_lastUpdate){
        let last = localStorage.fw_lastCheck
        if(isNaN(last) || Date.now() >= 14400000 + Number(last)) return await CheckUpdates()
    }
    else return await CheckUpdates()
    return false
}
export {CheckUpdates,AutoUpdate}