const hourEl = document.querySelector(".hour")
const minuteEl = document.querySelector(".minute")
const secondEl = document.querySelector(".second")

function updateClock(){
    const currentDate = new Date();

    const hour = currentDate.getHours();
    const minute = currentDate.getMinutes();
    const second = currentDate.getSeconds();
    
    const hourDeg = hour*30;
    const minuteDeg = minute*6;
    const secondDeg = second*6;

    hourEl.style.transform = `rotate(${hourDeg}deg)`;
    minuteEl.style.transform = `rotate(${minuteDeg}deg)`;
    secondEl.style.transform = `rotate(${secondDeg}deg)`;
}

setInterval(updateClock,1000);