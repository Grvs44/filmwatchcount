function Filters(){
  if(document.getElementById("chk").checked) for(var link of document.getElementsByClassName("filter")) link.href += "&sub"
  else for(var link of document.getElementsByClassName("filter")) link.href = link.href.replace("&sub","")
  onpageshow = Filters
}
async function WatchCount(){
  if(document.getElementById("chk").checked) var url = "/count?sub"
  else var url = "/count"
  document.getElementById("count").innerHTML = "Watch count: " + await(await fetch(location.href + url)).text()
}
