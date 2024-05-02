"use strict";

const profile_btn = document.getElementById('picon'); // Remove the # symbol
const menu = document.getElementById('menu');

profile_btn.addEventListener('click', slideMenu)

function slideMenu() {
    if(!menu.classList.contains('hidden')){
        menu.classList.toggle('hidden');
        menu.style.animation = 'menuSlider 300ms forwards';
    } else {
        menu.classList.toggle('hidden');
        menu.style.animation = '';
    }

}
