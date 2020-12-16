// contains all of the js 

// to keep count, make variable

// javascript can change DOM or document object model on page

// backticks template literal which can sub in values


// find button and find onclick property, set value of onclick button equal to count variable
// equal to function. only when clicked on , runs function
// functional programming. functions are values which can be reassigned
// javascript console using inspect to find javascript errors
// listens to whole argument
// events happen when entire dom is loaded, can listen to clicks.

if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}


function count() {
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('h1').innerHTML=counter;
    // if (counter % 10 === 0) {
    //     alert(`The counter is now ${counter}`)
    // }
    localStorage.setItem('counter', counter);
}

document.addEventListener('DOMContentLoaded', function() { 
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    document.querySelector('button').onclick = count; 

    setInterval(count, 1000); //interval that runs function
}); // check application in F12 to see key and values in localstorage

//anonymouse function no name
    // function to run when event is listened
// can also add event listener for click .addeventlistener(click, count)
// cannot find button below because content has not loaded
// a. move to bottom
// b. add another event listener



// local storage is a dict basically getitem key, setitem key value