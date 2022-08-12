import {CheckUpdates} from "./pwaupdate.js"
function Onload(){
    document.getElementById("update").addEventListener("click",UpdateClick)
    document.getElementById("back").addEventListener("click",BackClick)
    let lastUpdate = localStorage.lastUpdate
    let lastCheck = localStorage.lastCheck
    document.getElementById("lastupdate").innerText = (lastUpdate === undefined || isNaN(lastUpdate))? "never": new Date(Number(lastUpdate))
    document.getElementById("lastcheck").innerText = (lastCheck === undefined || isNaN(lastCheck))? "never": new Date(Number(lastCheck))
}
async function UpdateClick(e){
    e.target.disabled = true
    let updated = await CheckUpdates()
    document.getElementById("lastcheck").innerText = new Date(Number(localStorage.lastCheck))
    if(updated){
        document.getElementById("lastupdate").innerText = new Date(Number(localStorage.lastUpdate))
        e.target.innerText = "Updated"
    }
    else e.target.innerText = "Already up-to-date"
}
function BackClick(e){
    if(document.referrer === "") location.href = "../"
    else history.back()
}
window.Onload = Onload