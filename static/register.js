function submitForm(signupRequest) {
    var username = document.getElementById('username');
    var password = document.getElementById('password');


    var updateData = {
        'username': username.value,
        'password': password.value
    };

    signupRequest.open("POST", "/api/signup/");
    signupRequest.send(JSON.stringify(updateData));
}

function processResponse(serializedData) {
    var requestPath = document.getElementById('request_path');
    var data = JSON.parse(serializedData);
    if (data['status'] === 'success') {
        localStorage.setItem("token", data['token']);
        window.location.replace(requestPath.value);
    } else {
        var msgBox = document.getElementById('message_box');
        msgBox.innerHTML = data['message']
    }
}

window.addEventListener("load", function () {
    var buttons = document.getElementsByTagName('button');

    var signupRequest = new XMLHttpRequest();

    for (var i = 0; i < buttons.length; ++i) {
        buttons[i].addEventListener('click', function () {
            submitForm(signupRequest);
        })
    }

    signupRequest.addEventListener('load', function () {
        processResponse(this.responseText)
    })
});
