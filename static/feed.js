'use strict'

const events = document.querySelectorAll('.card'); // event cards, stored in NodeList
const eventButton = document.getElementById('activate-event');
const calendar = document.getElementById('calendar'); // calendar 
const calendarButton = document.getElementById('activate-calendar');

eventButton.addEventListener('click', showEvent);
calendarButton.addEventListener('click', showCalendar);


function showEvent(){
    if(!calendar.classList.contains('hidden')){ // toggle if hidden
        eventButton.classList.toggle('active')
        events.forEach(function(event){
            event.classList.toggle('hidden');
        });
    }
    if(!calendar.classList.contains('hidden')){
        calendarButton.classList.toggle('active');
        calendar.classList.toggle('hidden')
    } // toggle if not hidden
}

function showCalendar(){
    if(calendar.classList.contains('hidden')) //IF HIDDEN THEN UNHIDE
    {
        calendarButton.classList.toggle('active');
        calendar.classList.toggle('hidden');
    }
    if(!document.querySelector('.card').classList.contains('hidden')){
        eventButton.classList.toggle('active')
        events.forEach(function(event){
            event.classList.toggle('hidden');
        });
    }
}