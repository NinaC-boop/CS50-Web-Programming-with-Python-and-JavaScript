// NOTE: hard reset everything before you refresh or else you won't see changes!

document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    // note: use event listeners and setattributes, not hardcode onclick
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    document.querySelector('#reply').addEventListener('click', reply_email);
    document.querySelector('#archive').addEventListener('click', archive);
    document.querySelector('#unarchive').addEventListener('click', archive);
    document.querySelector('#compose-form').addEventListener('submit', function() {
        const recipients = document.querySelector('#compose-recipients').value;
        const subject = document.querySelector('#compose-subject').value;
        const body = document.querySelector('#compose-body').value;
        send_email(recipients, subject, body);
    });

    // By default, load the inbox
    load_mailbox('inbox');
});

function archive() {
    if (this.id == "archive") {
        mark_archived(this.dataset.id, true);
    } else {
        mark_archived(this.dataset.id, false);
    }
    
}

function mark_archived(id, bool) {
    if (bool) {
        console.log("marked archived");
    } else {
        console.log("marked unarchived");
    }
    
    fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: bool
        })
    }).then(response => {
        load_mailbox('inbox');
    })
}


function reply_email() {
    console.log(this.dataset.id);
    compose_email();
    document.querySelector('#compose-recipients').value = this.dataset.sender;

    if (this.dataset.subject.substring(0,4) == "Re: ") {
        document.querySelector('#compose-subject').value = this.dataset.subject;
    } else {
        document.querySelector('#compose-subject').value = "Re: " + this.dataset.subject;
    }
    

    document.querySelector('#compose-body').value = `On ${this.dataset.timestamp} ${this.dataset.sender} wrote: ${this.dataset.body}`;
}


function load_email(id) { // mailbox: inbox, send, archive

    

    // Show the mailbox and hide other views
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'none';
    show_email(id);

}

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
// email’s sender, recipients, subject, timestamp, and body.
function show_email(id) {
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
    
        var recipients = "";
        for (i = 0, len = email.recipients.length; i < len; i++) {
            if (i != 0 && i != len) {
                recipients += ', ';
            }
            recipients += email.recipients[i];
        }

        document.querySelector('#email-subject').innerHTML = `<h3>${email.subject}</h3>`;
        document.querySelector('#email-addresses').innerHTML = `<p><small>From: ${email.sender}</small><br><small>To: ${recipients}</small></p>`;
        document.querySelector('#email-body').innerHTML = `<p>${email.body}</p>`;
        document.querySelector('#email-timestamp').innerHTML = `<p><small>Sent ${email.timestamp}</small></p>`;

        // data of original email
        document.querySelector('#reply').setAttribute("data-id", `${id}`);
        document.querySelector('#reply').setAttribute("data-sender", `${email.sender}`);
        document.querySelector('#reply').setAttribute("data-recipients", `${recipients}`);
        document.querySelector('#reply').setAttribute("data-subject", `${email.subject}`);
        document.querySelector('#reply').setAttribute("data-body", `${email.body}`);
        document.querySelector('#reply').setAttribute("data-timestamp", `${email.timestamp}`);

        document.querySelector('#archive').setAttribute("data-id", `${id}`);
        document.querySelector('#unarchive').setAttribute("data-id", `${id}`);

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
        console.log("returning to sent");
        load_mailbox('sent');
    });

}


function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // document.querySelector('#compose-form').onsubmit = function() {
    //     const recipients = document.querySelector('#compose-recipients').value;
    //     const subject = document.querySelector('#compose-subject').value;
    //     const body = document.querySelector('#compose-body').value;
    //     send_email(recipients, subject, body);
    // };
    

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function mark_read(id) {
    console.log("marked read")
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
    email_item.setAttribute("onclick", `load_email(${email.id}); mark_read(${email.id});`);

    var body = email.body;
    if (body.length > 200) {
        body = body.substring(0, 200) + "...";
    } else {
        body = body.substring(0, body.length - 1);
    }

    if (email.read == true) {
        email_item.className = "row border border-primary email-item rounded bg-light text-dark";
        email_item.innerHTML = `<div class="col-3" data-id=${email.id}><p>${email.sender}</p></div><div class="col-9" data-id=${email.id}><p>${email.subject}</p><p>${body}</p><p>${email.timestamp}</p></div>`;
    } else {
        email_item.className = "row border border-primary email-item rounded";
        email_item.innerHTML = `<div class="col-3" data-id=${email.id}><h5>${email.sender}</h5></div><div class="col-9" data-id=${email.id}><h5>${email.subject}</h5><p>${body}</p><p>${email.timestamp}</p></div>`;
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
        }
    });
}

function load_mailbox(mailbox) { // mailbox: inbox, send, archive

    console.log("received");

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'none';

    if (mailbox == "inbox") {
        document.querySelector('#archive').style.display = 'inline-block';
        document.querySelector('#unarchive').style.display = 'none';
    } else if (mailbox == "sent") {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display = 'none';
    } else {
        document.querySelector('#archive').style.display = 'none';
        document.querySelector('#unarchive').style.display = 'inline-block';
    }


    // note: changing innerhtml also can reset all text within
    // Show the mailbox name
    document.querySelector('#emails-view-heading').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    document.querySelector('#emails-view-gallery').innerHTML = '';
    show_emails(mailbox);
}