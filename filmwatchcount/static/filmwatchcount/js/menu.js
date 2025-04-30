function ToggleMenu(e){
  var menu = document.getElementById('menu')
  if(menu.style.display === 'block'){
      menu.style.display = 'none'
  }
  else{
      menu.style.display = 'block'
  }
}
addEventListener('pageshow',()=>{
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
})
addEventListener('load',()=>{
  document.getElementById('menubtn').addEventListener('click',ToggleMenu)
})
