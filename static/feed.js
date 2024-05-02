'use strict'
// - - - - - THIS SECTION GRABS THE ELEMENTS WE NEED - - - - -
let events = document.querySelectorAll('.card'); // event cards, stored in NodeList
const eventButton = document.getElementById('activate-event');
const calendar = document.getElementById('calendar'); // calendar 
const calendarButton = document.getElementById('activate-calendar');
let choiceEvents = document.querySelectorAll('.choice-card');
const choiceEventButton = document.getElementById('activate-choice-events');
const acceptButtons = document.querySelectorAll('.accept-button');
const declineButtons = document.querySelectorAll('.decline-button');
const revertButtons = document.querySelectorAll('.revert-button');
// - - - - -THIS SECTION GRABS THE ELEMENTS WE NEED -- END OF SECTION --  - - - - -

//- - - - - FUNCTION CALLS - - - - - //
eventButton.addEventListener('click', showEvent);
calendarButton.addEventListener('click', showCalendar);
choiceEventButton.addEventListener('click', showChoiceEvent);

acceptButtons.forEach(button => {
    button.addEventListener('click', function() {
        const eventId = button.dataset.eventId;
        const userId = button.dataset.userId;
        acceptEvent(eventId, userId);
    });
});

declineButtons.forEach(button => {
    button.addEventListener('click', function() {
        const eventId = button.dataset.eventId;
        const userId = button.dataset.userId;
        declineEvent(eventId, userId);
    });
});

revertButtons.forEach(button => {
    button.addEventListener('click', function() {
        const eventId = button.dataset.eventId;
        const userId = button.dataset.userId;
        revertEventChoice(eventId, userId);
    });
});

//- - - - - END OF FUNCTION CALLS - - - - - //

// EVERYTHING BELOW THIS COMMENT ARE DEFINING FUNCTIONS 

function showEvent() {
    updateAllEvents();
    eventButton.classList.add('active');
    events.forEach(function(event) {
        event.classList.remove('hidden');
    });

    choiceEventButton.classList.remove('active');
    choiceEvents.forEach(function (event) {
        event.classList.add('hidden');
    });

    calendarButton.classList.remove('active');
    calendar.classList.add('hidden');
}

function showCalendar() {
    updateAllEvents();
    calendarButton.classList.add('active');
    calendar.classList.remove('hidden');

    eventButton.classList.remove('active');
    events.forEach(function (event) {
        event.classList.add('hidden');
    });

    choiceEventButton.classList.remove('active');
    choiceEvents.forEach(function (event) {
        event.classList.add('hidden');
    });
}

function showChoiceEvent() {
    updateAllEvents();
    choiceEventButton.classList.add('active');
    choiceEvents.forEach(function(event) {
        event.classList.remove('hidden');
    });

    eventButton.classList.remove('active');
    events.forEach(function (event) {
        event.classList.add('hidden');
    });

    calendarButton.classList.remove('active');
    calendar.classList.add('hidden');
}

function acceptEvent(eventId, userId) {
    fetch('/accept_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            eventId: eventId,
            userId: userId
        })
    }).then(response => {
        if(response.ok) {
            var elementId = 'event-id-' + eventId;
            const eventCard = document.getElementById(elementId);
            eventCard.classList.remove('card');
            eventCard.classList.add('choice-card');
            eventCard.classList.add('accepted');
            eventCard.classList.add('hidden');
            toggleChoiceButtons(eventId);
        } else {
            console.error('Error accepting event');
        }
    }).catch(error => {
        console.error('Error: ', error);
    });
}

function declineEvent(eventId, userId) {
    fetch('/decline_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            eventId: eventId,
            userId: userId
        })
    }).then(response => {
        if(response.ok) {
            var elementId = 'event-id-' + eventId;
            const eventCard = document.getElementById(elementId);
            eventCard.classList.remove('card');
            eventCard.classList.add('choice-card');
            eventCard.classList.add('declined');
            eventCard.classList.add('hidden');
            toggleChoiceButtons(eventId);
        } else {
            console.error('Error declining event');
        }
    }).catch(error => {
        console.error('Error: ', error);
    });
}

function revertEventChoice(eventId, userId) {
    fetch('/revert_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            eventId: eventId,
            userId: userId
        })
    }).then(response => {
        if(response.ok) {
            var elementId = 'event-id-' + eventId;
            const eventCard = document.getElementById(elementId);
            eventCard.classList.remove('choice-card');
            eventCard.classList.add('card');
            eventCard.classList.remove('accepted');
            eventCard.classList.remove('declined');
            eventCard.classList.add('hidden');
            toggleChoiceButtons(eventId);
        } else {
            console.error('Error reverting event');
        }
    }).catch(error => {
        console.error('Error: ', error);
    });
}

function toggleChoiceButtons(eventId) {
    var elementId = 'event-id-' + eventId;
    const eventCard = document.getElementById(elementId);
    const acceptButton = eventCard.querySelector('.accept-button');
    const declineButton = eventCard.querySelector('.decline-button');
    const revertButton = eventCard.querySelector('.revert-button');

    acceptButton.classList.toggle('hidden');
    declineButton.classList.toggle('hidden');
    revertButton.classList.toggle('hidden');
}

function updateAllEvents() {
    events = document.querySelectorAll('.card');
    choiceEvents = document.querySelectorAll('.choice-card');
}