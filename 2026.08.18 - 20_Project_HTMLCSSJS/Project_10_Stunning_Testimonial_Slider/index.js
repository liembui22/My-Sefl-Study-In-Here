const testimonials = [
    {
        name: "Liem Bui",
        photoUrl: "_BTL9578.jpg",
        text: "I never thought I'd look forward to working out, but my sessions at Nai Gym have completely changed that! It's super fun and keeps me energized all week! 🏋️‍♀️💥"
    },
    {
        name: "Duong Hau",
        photoUrl: "_BTL9700.jpg",
        position: 'center',
        text: "I’ve never felt better mentally and physically! The vibe at Nai Gym is so positive, and it really keeps me coming back for more. 💥😊"
    },
    {
        name: "Phuong Thao",
        photoUrl: "487922901_2711509675711983_6381743765000129239_n.jpg",
        text: "Just had the best workout at Nai Gym! The community here makes every session feel like catching up with friends, and I’m so grateful for that vibe! 🙌💖"
    },
    {
        name: "Minh Nhut",
        photoUrl: "503801566_2771133463082937_4087094785582155272_n.jpg",
        text: "Absolutely loving my time at Nai Gym! Every workout leaves me feeling accomplished and energized—can't wait to see my progress! 💪✨"
    },
]

const imgEl = document.querySelector('#user-image')
const usernameEl = document.querySelector('.username')
const textEl = document.querySelector('.text')


let idx = 0
updateTestimonial()

function updateTestimonial(){
    const {name,photoUrl,text} =
    testimonials[idx];

    imgEl.src = photoUrl;
    textEl.innerText = text;
    usernameEl.innerText = name;

    idx++
    if (idx === testimonials.length){
        idx=0;
    }
    setTimeout(()=> {
        updateTestimonial();
    },10000)
    
}