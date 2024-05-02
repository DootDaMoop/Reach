async function renderCalendar(year, month) {
    const calendarDiv = document.getElementById('calendar');
    const monthNames = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December'];

    const firstDayOfMonth = new Date(year, month, 1);
    const startingDayOfWeek = firstDayOfMonth.getDay();
    const lastDayOfMonth = new Date(year, month + 1, 0)
    const numDaysInMonth = lastDayOfMonth.getDate();

    let calendarHTML = []; 
    calendarHTML.push(`<h2 class="calendar-header text-3xl font-bold">${monthNames[month]} ${year}</h2><table class="calendar-table"><tr>`);

    ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(dayName => {
        calendarHTML.push(`<th>${dayName}</th>`);
    })
    calendarHTML.push('</tr><tr>');

    let dayCounter = 0;
    const prevMonthLastDay = new Date(year, month, 0).getDate();

    for(let i = 0; i < 42; i++) {
        if(i < startingDayOfWeek) {
            const prevMonthDay = prevMonthLastDay - startingDayOfWeek + i + 1;
            calendarHTML.push(`<td class="calendar-day prev-month-calendar-day" onclick="prevMonth()">${prevMonthDay}</td>`);
        } else if(i >= startingDayOfWeek + numDaysInMonth) {
            const nextMonthDay = i - startingDayOfWeek - numDaysInMonth + 1;
            calendarHTML.push(`<td class="calendar-day next-month-calendar-day"onclick="nextMonth()">${nextMonthDay}</td>`);
        } else {
            dayCounter++;
            const dayEvents = await getNumEventsOnDay(year, month+1, dayCounter);
            console.log(dayEvents)
                if(dayEvents > 0) {
                    calendarHTML.push(`<td class="calendar-day has-event" id="${year}-${month+1}-${dayCounter}" onclick="selectDate(${dayCounter})">${dayCounter}</td>`);
                } else {
                    calendarHTML.push(`<td class="calendar-day" id="${year}-${month+1}-${dayCounter}" onclick="selectDate(${dayCounter})">${dayCounter}</td>`);
                }
            
            }
            // Creates new row
            if((i + 1) % 7 === 0) {
                calendarHTML.push('</tr><tr>');
            }
        }
    calendarHTML.push('</tr></table>');
    calendarDiv.innerHTML = calendarHTML.join('');
}

async function nextMonth() {
    if(currentMonth === 11) {
        currentYear++;
        currentMonth = 0;
    } else {
        currentMonth++;
    }
    await renderCalendar(currentYear, currentMonth);
}

async function prevMonth() {
    if(currentMonth === 0) {
        currentYear--;
        currentMonth = 11;
    } else {
        currentMonth--;
    }
    await renderCalendar(currentYear, currentMonth);
}

function selectDate(year, month, day) {
    
}

async function getNumEventsOnDay(year, month, day) {
    try {
        const response = await fetch('/get_num_events_for_day', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                year: year,
                month: month,
                day: day
            })
        });

        if(!response.ok) {
            console.error('Failed to fetch events for day');
            return 0;
        }
        const data = await response.json();
        const length = Object.keys(data).length;
        console.log(length);
        return length;
    }
    catch(error) {
        console.error('Error: ', error);
        return 0;
    }
}

const currentDate = new Date();
let currentYear = currentDate.getFullYear();
let currentMonth = currentDate.getMonth();
renderCalendar(currentYear, currentMonth);