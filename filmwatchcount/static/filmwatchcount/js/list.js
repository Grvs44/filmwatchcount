(()=>{
  let p = new URLSearchParams(location.search)
  if(p.has('q'))document.getElementsByName('q')[0].value = p.get('q')
  if(p.has('sort'))document.getElementsByName('sort')[0].value=p.get('sort')
})()
