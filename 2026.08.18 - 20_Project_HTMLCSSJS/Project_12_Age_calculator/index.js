const birthdayEl = document.getElementById('birthday')
const btnEl = document.getElementById('btn')
const resultEl = document.getElementById('result')

function calculateAge(){
    const birthdayValue = birthdayEl.value;
    if(birthdayValue ===""){
        alert("Please enter your birthday")
    }else{
        const age =getAge(birthdayValue)
        resultEl.innerText = `Your age is ${age} ${age > 1 ? "years" : "year"} old`;
    }
}
// từ nay hãy học code bằng cách kêu claude đưa ra gợi ý và các kiến thức mới và code theo
function getAge(birthdayValue){
    const currentDate = new Date();
    const birthdayDate = new Date(birthdayValue);
    let age = currentDate.getFullYear() - birthdayDate.getFullYear();
    const month = currentDate.getMonth() - birthdayDate.getMonth();
// xíu về làm giấy phần này
    if (month < 0 || month === 0 && currentDate.getDate() < birthdayDate.getDate()){
        age--
    }

    return age;
}

btnEl.addEventListener("click",calculateAge)