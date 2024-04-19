'use strict'
// - - - - - THIS SECTION GRABS THE ELEMENTS WE NEED - - - - -
const events = document.querySelectorAll('.card'); // event cards, stored in NodeList
const eventButton = document.getElementById('activate-event');
const calendar = document.getElementById('calendar'); // calendar 
const calendarButton = document.getElementById('activate-calendar');
// - - - - -THIS SECTION GRABS THE ELEMENTS WE NEED -- END OF SECTION --  - - - - -

//- - - - - FUNCTION CALLS - - - - - //
eventButton.addEventListener('click', showEvent);
calendarButton.addEventListener('click', showCalendar);
//- - - - - END OF FUNCTION CALLS - - - - - //

// EVERYTHING BELOW THIS COMMENT ARE DEFINING FUNCTIONS 

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