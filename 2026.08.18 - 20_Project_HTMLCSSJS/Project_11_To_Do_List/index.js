const inputEl = document.querySelector('.input')
const formEl = document.querySelector('.form')
const ulEl = document.querySelector(".list")

formEl.addEventListener('submit',(event)=>{
    event.preventDefault();
    toDoList()
});

function toDoList(){
    let newTask = inputEl.value;
    const liEl = document.createElement("li");
    liEl.innerText = newTask;
    ulEl.appendChild(liEl)
}