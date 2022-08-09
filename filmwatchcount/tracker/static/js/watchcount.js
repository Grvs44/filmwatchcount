async function WatchCount(btn){
    btn.parentElement.innerHTML = "Watch count: " + await(await fetch(location.href + "/count")).text()
}