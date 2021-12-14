const RANDOM_QUOTE = 'https://api.quotable.io/random?minLength=100'
const displayElement = document.getElementById('displayID')
const inputElement = document.getElementById('inputID')
const timerElement = document.getElementById('timerID')
const wpmElement = document.getElementById('wpmID')
let wpq = 0
let wpm = 0
let flag = 0
const averagewordlength = 4
inputElement.addEventListener('input', ()=>{
    const quotearray = displayElement.querySelectorAll('span')
    const value = inputElement.value.split('')

    if(timerElement.innerText == 60){
        startTimer()
    }

    let correct = true
    wpq = 0

    quotearray.forEach((characterSpan, index)=>{
        const character = value[index]
        if(character == null){
            characterSpan.classList.remove('correct')
            characterSpan.classList.remove('incorrect')
            correct = false
        }
        else if(character === characterSpan.innerText) {
            characterSpan.classList.add('correct')
            characterSpan.classList.remove('incorrect')
            wpq++
        }
        else{
            characterSpan.classList.add('incorrect')
            characterSpan.classList.remove('correct')
            correct = false
        }
    })

    if(correct)
        renderQuote()
})

function getQuote(){
    wpm += wpq
    return fetch(RANDOM_QUOTE)
        .then(response=>response.json())
        .then(data=>data.content)
}

async function renderQuote(){
    const quote = await getQuote()
    displayElement.innerText = ''
    quote.split('').forEach(character=>{
        const characterSpan = document.createElement('span')
        characterSpan.innerText = character
        displayElement.appendChild(characterSpan)
    })
    inputElement.value = null
}

let startTime
let intervalID
function startTimer(){
    flag = 0
    timerElement.innerText = "60"
    timerElement.setAttribute('aria-valuenow', '60')
    timerElement.setAttribute('width', '100')
    startTime = new Date()
    intervalID = setInterval(()=>{
        timerElement.innerText = getTime()
        let pcg = Math.floor(timerElement.innerText/60*100)
        timerElement.setAttribute('aria-valuenow', pcg)
        timerElement.setAttribute('style','width:'+Number(pcg)+'%')
    }, 500)
}

function endTime(){
    if(flag == 0) {
        wpm += wpq
        wpmElement.innerText = Math.floor(wpm/averagewordlength)
        inputElement.setAttribute("readonly", "")
        clearInterval(intervalID)
        flag = 1
        const xhttp = new XMLHttpRequest()
        xhttp.onload = function() {
            wpm = this.responseText;
        }
        xhttp.open("POST", "/type/"+wpm, true)
        xhttp.send()
    }
}

function getTime() {
    if(timerElement.innerText == 0){
        endTime()
    }
    else
        return Math.floor(20-((new Date() - startTime)/1000))
}

renderQuote()