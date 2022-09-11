async function WatchCount(){
    document.getElementById("count").innerHTML = "Watch count: " + await(await fetch(location.href + "/count")).text()
}