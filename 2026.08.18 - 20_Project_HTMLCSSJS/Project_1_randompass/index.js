const btnEl =document.querySelector(".btn");
const inputEl = document.getElementById("input");
const copyEl = document.querySelector(".fa-copy");
const alertContainerEl = document.querySelector(".alert-container");

btnEl.addEventListener("click",()=>{
    createPassword();
});

copyEl.addEventListener("click",()=>{
    if (inputEl.value) {
        copyPassword();
    }
});

function createPassword(){
    const chars = "123456789abcdefghijklmnopqrstuvwxtz!@#$%^&*()_+:{}[]ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    const passwordlength = 14;
    let password = ""
    for (let index = 0; index < passwordlength; index++) {
        const randomNumber = Math.floor( Math.random() * chars.length);
        password += chars.substring(randomNumber, randomNumber + 1);
    }
    inputEl.value = password; 
}

function copyPassword(){
    inputEl.select();
    inputEl.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(inputEl.value);
    showAlert("Password copied to clipboard!");
}

function showAlert(message) {
    alertContainerEl.innerText = message;
    alertContainerEl.classList.remove("active");
    setTimeout(() => {
        alertContainerEl.classList.add("active");
    }, 3000);
}
