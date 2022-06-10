//Checking of Fisrt name field
function checkName() {
    var name = document.getElementById("name").value;
    var regex = /^[a-zA-Z\s]{2,15}$/;

    if (regex.test(name)) { 
        document.getElementById("first_Check").style.color = "green";
        document.getElementById("first_Check").innerHTML = ":)";
        return true;
    }
    else {
        document.getElementById("first_Check").style.color = "red";
        document.getElementById("first_Check").innerHTML = "Please, enter 2-15 characters";
        return false;
    }
}

function checkEmail() {
    var email = document.getElementById("email").value;
    var regex = /^[\w-\.]+@[\w-]+\.[a-z]{2,4}$/i;

    if (regex.test(email)) { 
        document.getElementById("email_Check").style.color = "green";
        document.getElementById("email_Check").innerHTML = ":)";
        return true;
    }
    else {
        document.getElementById("email_Check").style.color = "red";
        document.getElementById("email_Check").innerHTML = "Please, enter the correct email";
        return false;
    }
}


function checkMessage() {
    var mes = document.getElementById("message").value;
    var regex = /^[a-zA-Z\s]{10,250}$/;

    if (regex.test(mes)) {
        document.getElementById("message_Check").style.color = "green";
        document.getElementById("message_Check").innerHTML = ":)";
        return true;
    }
    else {
        document.getElementById("message_Check").style.color = "red";
        document.getElementById("message_Check").innerHTML = "Please, enter 10-250 characters";
        return false;
    }
}

function outputData() {
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var mes = document.getElementById("message").value;

    if (name != "" && email != "" && mes != "") {
        return true
    }
    else {
        document.getElementById("summary").style.color="red";
        document.getElementById("summary").innerHTML = "Please, fill in all the fields...";
    }
}

$(document).ready(function() {
    $('.menu-burger__header').click(function(){
        $('.menu-burger__header').toggleClass('open-menu');
        $('.header__nav').toggleClass('open-menu');
    });
});