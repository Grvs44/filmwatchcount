var csrftoken;
function Onload(){
    csrfelement = document.getElementsByName("csrfmiddlewaretoken")[0]
    csrftoken = csrfelement.value
    csrfelement.remove()
    var watchdiv = document.createElement("div")
    var h2 = document.createElement("h2")
    h2.innerText = "Add film watch"
    var form = document.createElement("form")
    h2.onclick = ToggleFormVisibility
    form.name = "watch"
    form.onsubmit = FormSubmit
    var select = document.createElement("select")
    select.name = "select"
    select.required = true
    var label = document.createElement("label")
    label.htmlFor = select
    label.innerText = "Film: "
    var date = document.createElement("input")
    date.type = "date"
    date.name = "date"
    date.required = true
    var label2 = document.createElement("label")
    label2.innerText = "Date: "
    label2.htmlFor = date
    var notes = document.createElement("textarea")
    notes.name = "notes"
    var label3 = document.createElement("label")
    label3.innerText = "Notes:"
    label3.htmlFor = notes
    var submit = document.createElement("input")
    submit.value = "Add"
    submit.type = "submit"
    form.append(label,select,document.createElement("br"),label2,date,document.createElement("br"),label3,document.createElement("br"),notes,document.createElement("br"),submit)
    watchdiv.append(h2,form)

    var filmdiv = document.createElement("div")
    h2 = document.createElement("h2")
    h2.innerText = "Add film"
    form = document.createElement("form")
    h2.onclick = ToggleFormVisibility
    form.name = "film"
    form.onsubmit = FormSubmit
    select = document.createElement("select")
    select.name = "select"
    select.required = true
    label = document.createElement("label")
    label.htmlFor = select
    label.innerText = "Film group: "
    var film = document.createElement("input")
    film.type = "text"
    film.name = "film"
    film.maxLength = 30
    label2 = document.createElement("label")
    label2.innerText = "Name: "
    label2.htmlFor = film
    submit = document.createElement("input")
    submit.type = "submit"
    submit.value = "Add"
    form.append(label,select,document.createElement("br"),label2,film,document.createElement("br"),submit)
    filmdiv.append(h2,form)

    var groupdiv = document.createElement("div")
    h2 = document.createElement("h2")
    h2.innerText = "Add film group"
    form = document.createElement("form")
    h2.onclick = ToggleFormVisibility
    form.name = "group"
    form.onsubmit = FormSubmit
    film = document.createElement("input")
    film.type = "text"
    film.name = "name"
    film.maxLength = 30
    label = document.createElement("label")
    label.innerText = "Name: "
    label.htmlFor = film
    submit = document.createElement("input")
    submit.type = "submit"
    submit.value = "Add"
    form.append(label,film,document.createElement("br"),submit)
    groupdiv.append(h2,form)
    document.getElementById("content").append(watchdiv,filmdiv,groupdiv)
}
async function ToggleFormVisibility(e){
    var form = e.target.parentElement.getElementsByTagName("form")[0]
    if(form.style.display == "block") form.style.display = "none"
    else{
        form.style.display = "block"
        if(form.select && form.select.children.length == 0) GetFormData(form)
    }
}
async function GetFormData(form){
    var dataname;
    switch(form.name){
        case "watch":
            dataname = "film"
            break
        case "film":
            dataname = "group"
            break
    }
    var data = await(await fetch("/" + dataname)).json()
    var option;
    for(var item of data){
        option = document.createElement("option")
        option.recordid = item[0]
        option.innerText = item[1]
        form.select.appendChild(option)
    }
}
async function FormSubmit(e){
    e.preventDefault()
    const formdata = new FormData(e.target)
    formdata.set("csrfmiddlewaretoken",csrftoken)
    if(formdata.has("select")) formdata.set("select",e.target.select.selectedOptions[0].recordid)
    var request = await fetch("/" + e.target.name,{method:"POST",body:formdata})
    if(request.status == 200){
        e.target.reset()
        GetFormData(e.target)
    }
    else alert(await request.text())
}