(()=>{
for(let [k,v] of new URLSearchParams(location.search).entries()){
let e=document.getElementsByName(k)[0]
if(e)e.value=v
}
})()
