const birthdayEl = document.getElementById('birthday')
const btnEl = document.getElementById('btn')
const resultEl = document.getElementById('result')

function calculateAge(){
    const birthdayValue = birthdayEl.value;
    if(birthdayValue ===""){
        // hiện thông báo yêu cầu người dùng nhập ngày sinh
        alert("Please enter your birthday")
    }else{
        const age =getAge(birthdayValue)
        // hiển thị kết quả tuổi của người dùng 'cấu trúc condition ? True : False' để hiển thị số nhiều hoặc số ít
        resultEl.innerText = `Your age is ${age} ${age > 1 ? "years" : "year"} old`;
    }
}
// từ nay hãy học code bằng cách kêu claude đưa ra gợi ý và các kiến thức mới và code theo
function getAge(birthdayValue){
    const currentDate = new Date();
    // lấy ngày sinh của người dùng từ input và chuyển đổi sang định dạng Date
    // định dạng Date trong JavaScript là một đối tượng được sử dụng để làm việc với ngày và giờ. Khi bạn tạo một đối tượng Date mới bằng cách sử dụng `new Date()`, nó sẽ lấy ngày và giờ hiện tại của hệ thống. Bạn cũng có thể tạo một đối tượng Date từ một chuỗi ngày tháng, ví dụ: `new Date('YYYY-MM-DD')`.
    const birthdayDate = new Date(birthdayValue);
    //  let là từ khóa dùng để khai biến có thể thay đổi trong khi đó const là gán một biến duy nhất và không thể thay đổi giá trị sau khi đã gán. Sử dụng let khi bạn cần thay đổi giá trị của biến, và const khi bạn muốn giữ giá trị cố định.
    let age = currentDate.getFullYear() - birthdayDate.getFullYear();
    const month = currentDate.getMonth() - birthdayDate.getMonth();
        if (month < 0 || month === 0 && currentDate.getDate() < birthdayDate.getDate()){
        age--
    }
    return age;
}

btnEl.addEventListener("click",calculateAge)