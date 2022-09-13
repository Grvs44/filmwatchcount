async function Onload() {
    var deferredPrompt
    const installbtn = document.getElementById('installbtn')
    addEventListener('beforeinstallprompt', e => {
        installbtn.style.display = "inline"
        deferredPrompt = e
    })
    installbtn.addEventListener('click', async () => {
        if (deferredPrompt !== null) {
            deferredPrompt.prompt()
            const {outcome} = await deferredPrompt.userChoice
            if (outcome === 'accepted') {
                deferredPrompt = null
                installbtn.remove()
            }
        }
    })
    var content = document.getElementById('content')
    var headers = new Headers()
    headers.append('cache-control','public,max-age=31536000')
    var response = await fetch('api/',{headers:headers})
    if(response.status == 200){
        var responseData = await response.json()
        for(var key of Object.keys(responseData)){
            var heading = document.createElement('h2')
            heading.innerText = key
            heading.onclick = event => ShowData(event,responseData[key])
            var div = document.createElement('div')
            var li = document.createElement('li')
            li.append(heading,div)
            content.append(li)
        }
    }
    else{
        var li = document.createElement('li')
        li.innerText = 'Couldn\'t download data'
        content.append(li)
    }
}
async function ShowData(event,url){
    let div = event.target.parentElement.getElementsByTagName('div')[0]
    let response = await fetch(url)
    if(response.status == 200){
        div.innerText = await response.text()
    }
}
