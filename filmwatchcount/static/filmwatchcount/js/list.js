;(()=>{
  let p = new URLSearchParams(location.search)
  if(p.has('q'))document.getElementsByName('q')[0].value = p.get('q')
})()
const clear=()=>document.getElementsByName('sort').forEach(e=>e.checked=false)
