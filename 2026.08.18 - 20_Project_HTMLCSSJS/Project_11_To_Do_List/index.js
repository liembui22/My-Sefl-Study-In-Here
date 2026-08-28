const inputEl = document.querySelector('.input')
const formEl = document.querySelector('.form')
const ulEl = document.querySelector(".list")



let list = JSON.parse(localStorage.getItem("list")) || []
list.forEach(task =>{
    toDoList(task)
})

formEl.addEventListener('submit',(event)=>{
    event.preventDefault();
    toDoList()
});

function toDoList(task){
// Nhập text vào ô
    let newTask = inputEl.value;
// khi gọi hàm if(task) = False nếu chưa có gì
// true thì new task = task.name là Do cũ
    if (task){
        newTask = task.name
    }
// tạo 1 li nhỏ khác trong ul, khai-> gán li -> gán ul appendChild(liel) và cho inputEl.value=''
    const liEl = document.createElement("li");
    liEl.innerText = newTask;
// nếu có task && task đã check thì check vào
    if (task && task.checked){
        liEl.classList.add("checked")
    }
    ulEl.appendChild(liEl)
    inputEl.value =""
// tạo nút check
    const checkBtnEl = document.createElement("div")
    checkBtnEl.innerHTML = `
    <i class="fa-solid fa-square-check">
    `;
    liEl.appendChild(checkBtnEl)
//tạo nút trash -> khai trash và tạo 1 thẻ div cho nó ->
    const trashBtnEl = document.createElement("div")
    trashBtnEl.innerHTML = `
    <i class="fa-solid fa-trash">
    `;
// thêm vào li đã tạo ở trên
    liEl.appendChild(trashBtnEl)
//add listener nếu checkBtnEl "click",() hàm đợi=>{} thực thi
    checkBtnEl.addEventListener('click',()=>{
// class list là danh sách các class Css đang gắn trên ptu liEl là li của task này
// toggle là công tắc cho checked
        liEl.classList.toggle("checked")
        updateLocalStorage()
    })
    trashBtnEl.addEventListener('click',()=>{
        liEl.remove();
        updateLocalStorage()
    })

    updateLocalStorage()
}

function updateLocalStorage(){
    const liEls = document.querySelectorAll('li')
    list = []
// LiEls lúc này là mảng nhiều li, .forEach là duyệt từng li
    liEls.forEach(liEl => {
// push vào list name và checked. lấy text của biến liEl chứa input
        list.push({
            name: liEl.innerText,
            checked: liEl.classList.contains("checked")
        })
    })
    // localstorage chỉ được lưu string -> .setItem cho list, JSON.stringify(list)
    localStorage.setItem('list', JSON.stringify(list))
}