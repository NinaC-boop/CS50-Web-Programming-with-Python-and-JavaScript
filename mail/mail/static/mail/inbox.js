// NOTE: hard reset everything before you refresh or else you won't see changes!

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // By default, load the inbox
    load_mailbox('inbox');
});

function show_email(id) {
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
    
        document.querySelector('#emails-view-heading').innerHTML = `<h3>${email.subject}</h3>`;
        document.querySelector('#emails-view-gallery').innerHTML = `<p>${email.body}</p>`;
    });
}

function send_email(recipients, subject, body) {
    // Send Mail: When a user submits the email composition form, add JavaScript code to actually send the email.
    // You’ll likely want to make a POST request to /emails, passing in values for recipients, subject, and body.
    // Once the email has been sent, load the user’s sent mailbox.
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

}


function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    document.querySelector('#compose-form').onsubmit = function() {
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;
        send_email(recipients, subject, body);
        load_mailbox('sent');
    };
    

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function mark_sent(id) {
    console.log("marked sent")
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
}

// gets a single dict of email and adds onto dom
// {
//     "id": 100,
//     "sender": "foo@example.com",
//     "recipients": ["bar@example.com"],
//     "subject": "Hello!",
//     "body": "Hello, world!",
//     "timestamp": "Jan 2 2020, 12:00 AM",
//     "read": false,
//     "archived": false
// }
function add_email_item(email) {

    // Create new email_item
    const email_item = document.createElement('div');
    // note: wrap onclick on div to make it all work
    email_item.setAttribute("onclick", `show_email(${email.id}); mark_sent(${email.id});`);

    var body = email.body;
    if (body.length > 200) {
        body = body.substring(0, 200) + "...";
    } else {
        body = body.substring(0, body.length - 1);
    }

    if (email.read == true) {
        email_item.className = "row border border-primary email-item rounded bg-light text-dark";
        email_item.innerHTML = `<div class="col-3" data-id=${email.id}><p>${email.sender}</p></div><div class="col" data-id=${email.id}><p>${email.subject}</p><p>${body}</p><p>${email.timestamp}</p></div>`;
    } else {
        email_item.className = "row border border-primary email-item rounded";
        email_item.innerHTML = `<div class="col-3" data-id=${email.id}><h5>${email.sender}</h5></div><div class="col" data-id=${email.id}><h5>${email.subject}</h5><p>${body}</p><p>${email.timestamp}</p></div>`;
    }
    
    // Add post to DOM
    document.querySelector('#emails-view-gallery').append(email_item);
};


function show_emails(mailbox) {
    fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        // Print emails
// REMOVE TESTS
        if (emails) {
            for (i = 0, len = emails.length; i < len; i++) {
                add_email_item(emails[i]);
            }
            // document.querySelector('#emails-view-gallery').innerHTML = text;
        }
    });
}

function load_mailbox(mailbox) { // mailbox: inbox, send, archive

    console.log("received");

    
    

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';


    // note: changing innerhtml also can reset all text within
    // Show the mailbox name
    document.querySelector('#emails-view-heading').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    document.querySelector('#emails-view-gallery').innerHTML = '';
    show_emails(mailbox);
}