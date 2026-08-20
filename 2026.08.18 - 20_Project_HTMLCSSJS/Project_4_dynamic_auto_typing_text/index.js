const containerEl = document.querySelector(".container");

const careers = ['Freelancer', 'Web Developer', 'Engineer', 'All-Rounder Staff', 'Youtuber'];

let characterIndex = 0;
let careerIndex = 0;

updateText();
function updateText() {
    characterIndex++
    containerEl.innerHTML =`<h1>Hi, i am a ${careers[careerIndex].slice(0,characterIndex)}</h1>`;
    if (characterIndex === careers[careerIndex].length){
        careerIndex++
        characterIndex = 0;
    }
    if (careerIndex === careers[careerIndex].length){
        careerIndex =0;
    }
    setTimeout(updateText, 200);
}
