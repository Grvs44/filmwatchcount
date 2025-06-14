;(()=>{
  let p = new URLSearchParams(location.search)
  if(p.has('q'))document.getElementsByName('q')[0].value = p.get('q')
  if(p.has('sort')){
    const v = p.get('sort')
    document.getElementsByName('sort').forEach(e=>e.checked=e.value==v)
  }
})()
const clear=()=>document.getElementsByName('sort').forEach(e=>e.checked=false)
