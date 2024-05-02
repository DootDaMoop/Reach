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

// ELEMENT GRABBING
const edit = document.querySelector(".edit-icon");
const group_card = document.querySelector(".group-edit-card");
const group_id = document.querySelector(".group-identifier");
const group_name = document.querySelector(".group-name");
const description = document.querySelector(".description");
const privacy = document.querySelector(".privacy");
const groupInfo = document.querySelector(".group-info");
const image = document.querySelector(".group-image-container");
const myson = document.querySelector(".krevat-2hour-trip-to-uncc");

// ELEMENT GRABBING

// - - - SPECIAL ELEMENT GRABBING SECTION - - - //

// - - - SPECIAL ELEMENT GRABBING SECTION - - - //


edit.addEventListener('click', edit_mode)

function edit_mode(){
    const form = document.createElement("form");
    const input1 = document.createElement("input");
    const input2 = document.createElement("input");
    const textarea = document.createElement("textarea");
    const submit = document.createElement("button")

    const label_input1 = document.createElement("label");
    const label_input2 = document.createElement("label");
    const label_textarea = document.createElement("label");

    const div1 = document.createElement("div");
    const div2 = document.createElement("div");
    const div3 = document.createElement("div");
    div1.classList.add('form-group');
    div2.classList.add('form-group');
    div3.classList.add('form-group');


    // Lines above creates the form and input elements needed
    label_input1.setAttribute('for', 'group-name');
    label_input2.setAttribute('for', 'privacy');
    label_textarea.setAttribute('for', 'description');

    // Set the name attributes for the input elements
    form.setAttribute('method', 'post');
    //form.setAttribute('action', '/groups/{{ membership.group_id }}/group_edit/')
    input1.setAttribute('name', 'group-name');
    input2.setAttribute('name', 'privacy');
    input2.setAttribute('type', 'checkbox');
    textarea.setAttribute('name', 'description');
    submit.setAttribute('href', '/groups/'+group_id+'/group_edit/');

    // --- Content of form --- //
    label_input1.textContent = 'Group Name:';
    label_input2.textContent = 'Private? ';
    label_textarea.textContent = 'Description:';
    submit.textContent = 'Save';


    // Now we want to add a class for the purpose of styling
    form.classList.add("form");
    input1.classList.add("form-control");
    label_input2.classList.add("mr-4");
    textarea.classList.add("form-control");
    div1.classList.add("form-group");
    div2.classList.add("form-group");
    div3.classList.add("form-group");
    submit.classList.add("btn");
    submit.classList.add("btn-primary");


    // Append divs to form
    form.appendChild(div1);
    form.appendChild(div3);
    form.appendChild(div2);
    form.appendChild(submit);

    // Append labels and inputs to respective divs
    div1.appendChild(label_input1);
    div1.appendChild(input1);
    div2.appendChild(label_input2);
    div2.appendChild(input2);
    div3.appendChild(label_textarea);
    div3.appendChild(textarea);

    // Finally, append form to groupInfo
    groupInfo.appendChild(form);

    input1.value = group_name.textContent; 
    if(privacy.textContent.includes('Private')){ // if group is private, automatically checks the checkbox 
        input2.checked = true;
    }
    else{
        input2.checked = false;
    }
    textarea.value = description.textContent;

    group_card.style.height = '400px';
    textarea.style.height = '100px';
    // Now we want to remove the existing elements inside the group card
    myson.remove(); 
    // making krevat life easier by removing his 2 hour commute 




}