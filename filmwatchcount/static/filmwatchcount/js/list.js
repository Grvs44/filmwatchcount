var fields
var initialTitle
var fieldTypes = {'integer':'number','string':'text'}
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
async function Refresh(){
    var url = document.getElementById('api').content + document.getElementById('table').content + "/"
    var response = await fetch(url,{method:'OPTIONS'})
    if(response.status == 200){
        var responseData = await response.json()
        initialTitle = responseData.name
        SetTitle(initialTitle)
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
async function Onload(){
    await Refresh()
    document.getElementById('data').onclick = ItemClicked
    document.getElementById('ref').onclick = Refresh
}
function ItemClicked(event){
    var data = event.target.parentElement.data
    if(data !== undefined){
        console.log(data)
        document.getElementById('content').style.display = 'none'
        var item = document.createElement('div')
        item.className = 'item'
        var form = document.createElement('form')
        form.onsubmit = ItemSaved
        var p,label,input
        for(var field in data){
            if(fields[field].read_only) continue
            p = document.createElement('p')
            input = document.createElement('input')
            if(fields[field].type in fieldTypes){
                input.type = fieldTypes[fields[field].type]
            }
            else{
                input.type = fields[field].type
            }
            input.required = fields[field].required
            input.value = data[field]
            label = document.createElement('label')
            label.innerText = fields[field].label
            label.htmlFor = input
            p.append(label,input)
            form.appendChild(p)
        }
        p = document.createElement('p')
        input = document.createElement('input')
        input.type = 'submit'
        input.value = 'Save'
        p.appendChild(input)
        form.appendChild(p)
        var heading = document.createElement('h1')
        heading.innerText = data.Name
        var closeBtn = document.createElement('button')
        closeBtn.className = 'close'
        closeBtn.onclick = ItemClosed
        closeBtn.innerText = 'X'
        item.append(closeBtn,heading,form)
        document.body.appendChild(item)
        document.getElementById('back').onclick = ItemClosed
        SetTitle(data.Name)
    }
}
function ItemClosed(event){
    console.log('itemclosed')
    event.target.parentElement.remove()
    document.getElementById('content').style.display = 'inherit'
    SetTitle(initialTitle)
}
function ItemSaved(event){
    event.preventDefault()
    var item = event.target.parentElement
    console.log('itemsaved',event.target)
}
addEventListener('load',Onload)