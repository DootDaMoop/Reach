function renderCalendar(year, month) {
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

    for(let i = 0; i <42; i++) {
        if(i < startingDayOfWeek) {
            const prevMonthDay = prevMonthLastDay - startingDayOfWeek + i + 1;
            calendarHTML.push(`<td class="calendar-day prev-month-calendar-day" onclick="prevMonth()">${prevMonthDay}</td>`);
        } else if(i >= startingDayOfWeek + numDaysInMonth) {
            const nextMonthDay = i - startingDayOfWeek - numDaysInMonth + 1;
            calendarHTML.push(`<td class="calendar-day next-month-calendar-day"onclick="nextMonth()">${nextMonthDay}</td>`);
        } else {
            dayCounter++;
            calendarHTML.push(`<td class="calendar-day" onclick="selectDate(${dayCounter})">${dayCounter}</td>`);
        }

        // Creates new row
        if((i + 1) % 7 === 0) {
            calendarHTML.push('</tr><tr>');
        }
    }
    calendarHTML.push('</tr></table>');

    calendarDiv.innerHTML = calendarHTML.join('');
}

function nextMonth() {
    if(currentMonth === 11) {
        currentYear++;
        currentMonth = 0;
    } else {
        currentMonth++;
    }
    renderCalendar(currentYear, currentMonth);
}

function prevMonth() {
    if(currentMonth === 0) {
        currentYear--;
        currentMonth = 11;
    } else {
        currentMonth--;
    }
    renderCalendar(currentYear, currentMonth);
}

function selectDate(date) {
    alert(`You selected: ${date}`);
}

const currentDate = new Date();
let currentYear = currentDate.getFullYear();
let currentMonth = currentDate.getMonth();
renderCalendar(currentYear, currentMonth);