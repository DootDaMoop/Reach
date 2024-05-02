
let invitedMemberList = document.querySelectorAll('.invited-member');
const invitedMemberListButton = document.getElementById('activate-invited-members');

let memberList = document.querySelectorAll('.member');
const memberListButton = document.getElementById('activate-members');

invitedMemberListButton.addEventListener('click', showInvitedMembers);
memberListButton.addEventListener('click', showMembers);

const inviteButtons = document.querySelectorAll('.invite-button');
const removeInviteButtons = document.querySelectorAll('.remove-invite-button')

const searchBarInvited = document.getElementById('search-bar-invited');
searchBarInvited.addEventListener('input', filterInvitedMembers);
const searchBarUninvited = document.getElementById('search-bar-uninvited');
searchBarUninvited.addEventListener('input', filterUninvitedMembers);

inviteButtons.forEach(button => {
    button.addEventListener('click', function() {
        const eventId = button.dataset.eventId;
        const userId = button.dataset.userId;
        inviteUser(eventId, userId);
    });
});

removeInviteButtons.forEach(button => {
    button.addEventListener('click', function() {
        const eventId = button.dataset.eventId;
        const userId = button.dataset.userId;
        removeInvitedUser(eventId, userId);
    })
})

function showInvitedMembers() {
    updateQueryInformation();
    memberListButton.classList.remove('active');
    memberList.forEach(function (member) {
        member.classList.add('hidden');
    });
    
    invitedMemberListButton.classList.add('active');
    invitedMemberList.forEach(function(member) {
        member.classList.remove('hidden');
    });

    searchBarInvited.classList.remove('hidden');
    searchBarUninvited.classList.add('hidden');
}

function showMembers() {
    updateQueryInformation();
    memberListButton.classList.add('active');
    memberList.forEach(function (member) {
        member.classList.remove('hidden');
    });
    
    invitedMemberListButton.classList.remove('active');
    invitedMemberList.forEach(function(member) {
        member.classList.add('hidden');
    });

    searchBarInvited.classList.add('hidden');
    searchBarUninvited.classList.remove('hidden');
}

function inviteUser(eventId, userId) {
    fetch('/invite_to_event', {
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
            var elementId = 'user-id-' + userId;
            var attending = 'attending-status-' + userId;
            const memberCard = document.getElementById(elementId);
            const attendingPara = document.getElementById(attending);
            memberCard.classList.remove('member');
            memberCard.classList.add('invited-member');
            memberCard.classList.add('hidden');
            attendingPara.classList.remove('hidden');
            attendingPara.textContent = 'Attending: Pending';
            toggleInviteButtons(userId);
        } else {
            console.error('Error inviting user');
        }
    }).catch(error => {
        console.error('Error: ', error);
    });
}

function removeInvitedUser(eventId, userId) {
    fetch('/remove_invite_to_event', {
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
            var elementId = 'user-id-' + userId;
            var attending = 'attending-status-' + userId;
            const memberCard = document.getElementById(elementId);
            const attendingPara = document.getElementById(attending);
            memberCard.classList.remove('invited-member');
            memberCard.classList.add('member');
            memberCard.classList.add('hidden');
            attendingPara.classList.add('hidden');
            toggleInviteButtons(userId);
        } else {
            console.error('Error removing user invite');
        }
    }).catch(error => {
        console.error('Error: ', error);
    });
}

function filterInvitedMembers() {
    const searchQuery = searchBarInvited.value.toLowerCase();
    const allMembers = document.querySelectorAll('.invited-member');

    allMembers.forEach(member => {
        const memberName = member.querySelector('.member-name').textContent.toLowerCase();
        if(memberName.includes(searchQuery)) {
            member.classList.remove('hidden');
        } else {
            member.classList.add('hidden');
        }
    });
}

function filterUninvitedMembers() {
    const searchQuery = searchBarUninvited.value.toLowerCase();
    const allMembers = document.querySelectorAll('.member');

    allMembers.forEach(member => {
        const memberName = member.querySelector('.member-name').textContent.toLowerCase();
        if(memberName.includes(searchQuery)) {
            member.classList.remove('hidden');
        } else {
            member.classList.add('hidden');
        }
    });
}

function toggleInviteButtons(userId) {
    var elementId = 'user-id-' + userId;
    const memberCard = document.getElementById(elementId);
    const inviteButton = memberCard.querySelector('.invite-button');
    const removeInviteButton = memberCard.querySelector('.remove-invite-button');

    inviteButton.classList.toggle('hidden');
    removeInviteButton.classList.toggle('hidden');
}

function updateQueryInformation() {
    memberList = document.querySelectorAll('.member');
    invitedMemberList = document.querySelectorAll('.invited-member');
}