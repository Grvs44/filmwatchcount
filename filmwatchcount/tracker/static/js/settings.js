import {CheckUpdates} from "./pwaupdate.js"
function Onload(){
    document.getElementById("update").addEventListener("click",UpdateClick)
    let lastUpdate = localStorage.lastUpdate
    document.getElementById("lastupdate").innerText = (lastUpdate === undefined || isNaN(lastUpdate))? "never": new Date(Number(lastUpdate))
}
async function UpdateClick(e){
    e.target.disabled = true
    let updated = await CheckUpdates()
    document.getElementById("lastupdate").innerText = new Date(Number(localStorage.lastUpdate))
    e.target.innerText = updated? "Updated": "Already up-to-date"
    setTimeout(ResetUpdateBtn,4000,e.target)
}
function ResetUpdateBtn(btn){
    btn.disabled = false
    btn.innerText = "Check for updates"
}
window.Onload = Onload