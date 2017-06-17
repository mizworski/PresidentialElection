function submitForm(loginRequest) {
    var username = document.getElementById('username');
    var password = document.getElementById('password');


    var updateData = {
        'username': username.value,
        'password': password.value
    };

    loginRequest.open("POST", "/api/login/");
    loginRequest.send(JSON.stringify(updateData));
}

function processResponse(serializedData) {
    var data = JSON.parse(serializedData);
    if (data['status'] === 'success') {
        localStorage.setItem("token", data['token']);
        window.location.replace('/static/index.html');
    } else {
        var msgBox = document.getElementById('message_box');
        msgBox.innerHTML = data['message']
    }
}

window.addEventListener("load", function () {
    var buttons = document.getElementsByTagName('button');

    var login = new XMLHttpRequest();

    for (var i = 0; i < buttons.length; ++i) {
        buttons[i].addEventListener('click', function () {
            submitForm(login);
        })
    }

    login.addEventListener('load', function () {
        processResponse(this.responseText)
    })
});
