function Onload() {
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
}