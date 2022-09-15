function Onload(){
    document.getElementById('title').innerText = 'Settings'
    document.getElementById("cache").addEventListener("click",ClearCache)
    document.getElementById("data").addEventListener("click",ClearData)
}
async function ClearCache(e){
    e.target.disabled = true
    e.target.innerText = "Clearing cache..."
    let cacheNames = await caches.keys()
    for(let cache of cacheNames){
        if(cache.substring(0,3) === "fw-") await caches.delete(cache)
    }
    e.target.innerText = "Cleared cache"
}
function ClearData(e){
    e.target.disabled = true
    e.target.innerText = "Clearing data..."
    let dataKeys = Object.keys(localStorage)
    for(let key of dataKeys){
        if(key.substring(0,3) === "fw_") localStorage.removeItem(key)
    }
    e.target.innerText = "Cleared data"
}
addEventListener('load',Onload)