document.body.appendChild(document.getElementById('page').cloneNode(true))
;(()=>{
  let p = new URLSearchParams(location.search)
  if(p.has('q'))document.getElementsByName('q')[0].value = p.get('q')
})()
