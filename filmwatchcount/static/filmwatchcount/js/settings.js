import {CheckUpdates} from "./pwaupdate.js"
function Onload(){
    document.getElementById("update").addEventListener("click",UpdateClick)
    document.getElementById("back").addEventListener("click",BackClick)
    document.getElementById("cache").addEventListener("click",ClearCache)
    document.getElementById("data").addEventListener("click",ClearData)
    let lastUpdate = localStorage.fw_lastUpdate
    let lastCheck = localStorage.fw_lastCheck
    document.getElementById("lastupdate").innerText = (lastUpdate === undefined || isNaN(lastUpdate))? "never": new Date(Number(lastUpdate))
    document.getElementById("lastcheck").innerText = (lastCheck === undefined || isNaN(lastCheck))? "never": new Date(Number(lastCheck))
}
async function UpdateClick(e){
    e.target.disabled = true
    let updated = await CheckUpdates()
    document.getElementById("lastcheck").innerText = new Date(Number(localStorage.fw_lastCheck))
    if(updated){
        document.getElementById("lastupdate").innerText = new Date(Number(localStorage.fw_lastUpdate))
        e.target.innerText = "Updated"
    }
    else e.target.innerText = "Already up-to-date"
}
function BackClick(e){
    if(document.referrer === "") location.href = "../"
    else history.back()
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
window.Onload = Onload