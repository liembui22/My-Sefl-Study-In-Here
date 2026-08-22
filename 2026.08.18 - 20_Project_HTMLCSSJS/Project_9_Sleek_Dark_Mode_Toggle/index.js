const inputEl = document.getElementById("dark-mode")
const bodyEl = document.querySelector("body")

function updatebody(){
    if(inputEl.checked){
        bodyEl.style.background = "black"
    } else{
        bodyEl.style.background = "white"
    }
}

inputEl.addEventListener("input", () => {
    updatebody()
})
