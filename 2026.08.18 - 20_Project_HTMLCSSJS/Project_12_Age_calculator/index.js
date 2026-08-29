const birthdayEl = document.getElementById('birthday')
const btnEl = document.getElementById('btn')
const resultEl = document.getElementById('result')

function calculateAge(){
    const birthdayValue = birthdayEl.value;
    if(birthdayValue ===""){
        alert("Please enter your birthday")
    }else{
        const age =getAge(birthdayValue)

        resultEl.innerHTML(age)
    }
}
// từ nay hãy học code bằng cách kêu claude đưa ra gợi ý và các kiến thức mới và code theo
function getAge(birthdayValue){
    const currentDate = new Date();
    const birthdayDate = new Date(birthdayValue);
    const age = currentDate.getFullYear() - birthdayDate.getFullYear();
    const month = currentDate.getMonth() - birthdayDate.getMonth();
// xíu về làm giấy phần này
    if (month < 0 || month === 0 && currentDate.getDate() < birthdayDate.getDate()){
        age--
    }
}

btnEl.addEventListener("click",calculateAge)