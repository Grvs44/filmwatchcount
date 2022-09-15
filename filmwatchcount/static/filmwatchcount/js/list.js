var fields
async function GetData(url){
    var response = await fetch(url)
    if(response.status == 200){
        var content = await response.json()
        var table = document.getElementById('data')
        var row
        var col
        for(var record of content.results){
            row = document.createElement('tr')
            row.data = record
            for(var field in fields){
                if(field === 'id') continue
                col = document.createElement('td')
                col.innerText = record[field]
                row.appendChild(col)
            }
            table.appendChild(row)
        }
        document.getElementById('total').innerText = content.count
        document.getElementById('shown').innerText = table.children.length - 1
        if(content.next == null) document.getElementById('more').style.display = 'none'
        else document.getElementById('more').onclick = ()=>GetData(content.next)
    }
}
async function Onload(){
    var url = document.getElementById('api').content + document.getElementById('table').content + "/"
    var response = await fetch(url,{method:'OPTIONS'})
    if(response.status == 200){
        var responseData = await response.json()
        document.getElementById('title').innerText = document.title = responseData.name
        fields = responseData.actions.POST
        var table = document.getElementById('data')
        table.innerHTML = ''
        var row = document.createElement('tr')
        var col
        for(var field in fields){
            if(field === 'id') continue
            col = document.createElement('th')
            col.innerText = fields[field].label
            row.appendChild(col)
        }
        table.appendChild(row)
        await GetData(url)
        document.getElementById('more').style.display = 'block'
    }
}
addEventListener('load',Onload)