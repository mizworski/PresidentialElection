function addDetailedInfo(serializedData, detailedInfo) {
    while (detailedInfo.children.length !== 0) {
        detailedInfo.removeChild(detailedInfo.firstChild);
    }

    var data = JSON.parse(serializedData);
    var tableHead = document.createElement("thead");
    var tableRow = document.createElement("tr");

    /// Create labels
    var labels = data['labels'];
    for (var key in labels) {
        var label = labels[key];
        tableRow.appendChild(document.createElement('th'))
            .appendChild(document.createTextNode(label))
    }
    tableHead.appendChild(tableRow);


    /// Fill with data
    var tableBody = document.createElement("tbody");

    var detailed_results = data['detailed_results'];
    for (var i = 0; i < detailed_results.length; ++i) {
        var table_row = document.createElement("tr");
        var electoral_unit_results = detailed_results[i];

        var unit_name_column = document.createElement("td");
        var unit_name_link = document.createElement("a");
        unit_name_link.href = electoral_unit_results[0];
        unit_name_link.innerHTML = electoral_unit_results[1];
        unit_name_column.appendChild(unit_name_link);
        table_row.appendChild(unit_name_column);

        for (var j = 2; j < electoral_unit_results.length; ++j) {
            var column = electoral_unit_results[j];
            table_row.appendChild(document.createElement('td'))
                .appendChild(document.createTextNode(column));
        }


        tableBody.appendChild(table_row)
    }

    detailedInfo.appendChild(tableHead);
    detailedInfo.appendChild(tableBody);
}

function updateNavBar(right_box) {
    var token = localStorage.getItem('token');

    if (token !== '') {
        right_box.innerHTML = '';
        var logoutButton = document.createElement('button');
        logoutButton.type = 'button';
        logoutButton.id = 'logout_button';
        logoutButton.innerHTML = 'logout';

        right_box.appendChild(document.createElement('div'))
            .appendChild(logoutButton);

        logoutButton.addEventListener('click', function () {
            localStorage.setItem('token', '');
            updateNavBar(right_box)
        });
    } else {
        right_box.innerHTML = '';
        var loginButton = document.createElement('a');
        loginButton.appendChild(document.createElement('div'))
            .appendChild(document.createTextNode('login'));
        loginButton.href = '/login';

        var registerButton = document.createElement('a');
        registerButton.appendChild(document.createElement('div'))
            .appendChild(document.createTextNode('register'));
        registerButton.href = '/signup';

        right_box.appendChild(loginButton);
        right_box.appendChild(registerButton);
    }
}

window.addEventListener("load", function () {
    var inputBox = document.querySelector("#input_field");
    var right_box = document.getElementById('right_box');

    updateNavBar(right_box);

    inputBox.addEventListener("input", function () {
        var results_detailed = document.getElementById("wyniki_szczegolowe_zawartosc");

        var detailedInfoRequest = new XMLHttpRequest();
        var queriedVal = inputBox.value;
        detailedInfoRequest.addEventListener("load", function () {
            if (queriedVal === inputBox.value) {
                addDetailedInfo(this.responseText, results_detailed);
            }
        });

        detailedInfoRequest.open("GET", "/api/search/" + inputBox.value);
        detailedInfoRequest.send();
    });
});
