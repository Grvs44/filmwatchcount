var fields
var initialTitle
var fieldTypes = {'integer':'number','string':'text'}
async function GetData(url){
    var response = await fetch(url)
    if(response.status == 200){
        var content = await response.json()
        var ul = document.getElementById('data')
        var li
        for(var record of content.results){
            li = document.createElement('li')
            li.innerText = record.str
            li.dataID = record.id
            ul.appendChild(li)
        }
        document.getElementById('total').innerText = content.count
        document.getElementById('shown').innerText = ul.children.length
        if(content.next == null) document.getElementById('more').style.display = 'none'
        else document.getElementById('more').onclick = ()=>GetData(content.next)
    }
}
async function Refresh(){
    var url = document.getElementById('api').content + document.getElementById('table').content + "/"
    var response = await fetch(url,{method:'OPTIONS'})
    if(response.status == 200){
        var responseData = await response.json()
        fields = responseData.actions.POST
        await GetData(url + 'summary/')
        document.getElementById('more').style.display = 'block'
    }
}
async function Onload(){
    await Refresh()
    document.getElementById('data').onclick = ItemClicked
    document.getElementById('ref').onclick = Refresh
}
async function ItemClicked(event){
    console.log(event.target)
    if(event.target.tagName === 'LI'){
        var items = event.target.getElementsByClassName('item')
        if(items.length == 0){
            var item = document.createElement('div')
            item.className = 'item'
            var dataResponse = await fetch(document.getElementById('api').content + document.getElementById('table').content + "/" + event.target.dataID)
            if(dataResponse.status == 200){
                var data = await dataResponse.json()
                console.log(data)
                var form = document.createElement('form')
                form.onsubmit = ItemSaved
                var p,label,input
                for(var field in data){
                    if(fields[field].read_only) continue
                    p = document.createElement('p')
                    if(fields[field].long){
                        input = document.createElement('textarea')
                    }
                    else{
                        input = document.createElement('input')
                        if(fields[field].type in fieldTypes){
                            input.type = fieldTypes[fields[field].type]
                        }
                        else{
                            input.type = fields[field].type
                        }
                    }
                    input.required = fields[field].required
                    input.value = data[field]
                    label = document.createElement('label')
                    label.innerText = fields[field].label
                    label.htmlFor = input
                    p.append(label,document.createElement('br'),input)
                    form.appendChild(p)
                }
                p = document.createElement('p')
                input = document.createElement('input')
                input.type = 'submit'
                input.value = 'Save'
                p.appendChild(input)
                form.appendChild(p)
            }
            else{
                var form = document.createElement('p')
                form.innerText = 'Couldn\'t download data'
            }
            var closeBtn = document.createElement('button')
            closeBtn.className = 'close'
            closeBtn.innerText = 'X'
            closeBtn.onclick = ItemClosed
            item.append(closeBtn,form)
            event.target.appendChild(item)
        }
        else{
            items[0].remove()
        }
    }
}
function ItemClosed(event){
    event.target.parentElement.remove()
}
function ItemSaved(event){
    event.preventDefault()
    var item = event.target.parentElement
    console.log('itemsaved',event.target)
}
addEventListener('load',Onload)