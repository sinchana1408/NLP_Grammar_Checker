async function checkText(){

let text = document.getElementById("inputText").value.trim()

if(text === ""){
alert("Please enter a sentence")
return
}

let resultBox = document.getElementById("resultBox")
let output = document.getElementById("output")

resultBox.style.display="block"

output.innerText="Checking grammar..."

let response = await fetch("/correct",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({text:text})

})

let data = await response.json()

output.innerText=data.corrected

}