const kicks = document.querySelectorAll('.kick-user');
const confirmation = document.querySelector('.kick-confirm');
const dimmed = document.querySelector('.dimmed-background');
const cancel = document.querySelector('.cancel');
const confirm = document.querySelector('.confirm');

confirm.addEventListener('click', function(){
    confirmation.classList.toggle('hidden')
})
cancel.addEventListener('click', function(){
    confirmation.classList.toggle('hidden')
})

kicks.forEach(function(kick){
    kick.addEventListener('click', askConfirmation);
    
})


function askConfirmation(){
    confirmation.classList.toggle('hidden')
    dimmed.style.display = 'block';
    document.body.classList.add('no-scroll');
    confirmElement.style.display = 'block';
}

