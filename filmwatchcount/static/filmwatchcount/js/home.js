async function Onload() {
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
