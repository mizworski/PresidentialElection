var unitName = '';
var isCommunity = false;

function addCandidatesResults(serializedData, candidatesResults) {
    while (candidatesResults.children.length !== 0) {
        candidatesResults.removeChild(candidatesResults.firstChild);
    }

    var token = localStorage.getItem('token');
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

    /// Fill table
    var tableBody = document.createElement("tbody");
    var cand_table = data['cand_table'];
    for (var i = 0; i < cand_table.length; ++i) {
        var table_row = document.createElement("tr");
        var candidate = cand_table[i];
        table_row.appendChild(document.createElement('td'))
            .appendChild(document.createTextNode(i + 1));
        table_row.appendChild(document.createElement('td'))
            .appendChild(document.createTextNode(candidate[0]));


        if (token !== '' && isCommunity === 'true') {
            var input_wrapper = document.createElement('div');
            var inputField = document.createElement('input');
            inputField.name = candidate[0];
            inputField.value = candidate[1];
            inputField.type = 'text';
            inputField.class = 'input';
            input_wrapper.appendChild(inputField);
            table_row.appendChild(document.createElement('td'))
                .appendChild(input_wrapper);
        } else {
            table_row.appendChild(document.createElement('td'))
                .appendChild(document.createTextNode(candidate[1]));
        }

        var inner_percentage_bar = document.createElement('div');

        inner_percentage_bar.style.width = '' + candidate[2] + '%';
        inner_percentage_bar.style.backgroundColor = candidate[3];

        var result_row = document.createElement('tr');

        result_row.appendChild(document.createElement('td'))
            .appendChild(document.createElement('div'))
            .appendChild(inner_percentage_bar);

        result_row.appendChild(document.createElement('td'))
            .appendChild(document.createElement('div'))
            .appendChild(document.createTextNode(candidate[2] + '%'));

        table_row.appendChild(document.createElement('td'))
            .appendChild(document.createElement('table'))
            .appendChild(document.createElement('tbody'))
            .appendChild(result_row);

        tableBody.appendChild(table_row)
    }


    candidatesResults.appendChild(tableHead);
    candidatesResults.appendChild(tableBody);
}

function addGeneralInfo(serializedData, generalInfo) {
    while (generalInfo.children.length !== 0) {
        generalInfo.removeChild(generalInfo.firstChild);
    }

    var token = localStorage.getItem('token');
    var data = JSON.parse(serializedData);
    for (var i = 0; i < data.length; ++i) {
        var row = data[i];
        var label = row['label'];
        var value = row['value'];

        var row_wrapper = document.createElement('div');

        var label_wrapper = document.createElement('div');
        label_wrapper.innerHTML = label;
        row_wrapper.appendChild(label_wrapper);

        if (token !== '' && isCommunity === 'true') {
            var value_wrapper = document.createElement('div');
            var inputField = document.createElement('input');
            inputField.name = row['short'];
            inputField.value = value;
            inputField.type = 'text';
            inputField.class = 'input';

            value_wrapper.appendChild(inputField);
            row_wrapper.appendChild(value_wrapper);
        } else {
            var value_wrapper = document.createElement('div');
            value_wrapper.innerHTML = value;
            row_wrapper.appendChild(value_wrapper);
        }
        generalInfo.appendChild(row_wrapper);
    }

}

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


function submitUpdate(generalInfo, candidatesResults, resultsDetailed, unitName) {
    var generalInfoInputs = generalInfo.getElementsByTagName('input');
    var candidatesResultsInputs = candidatesResults.getElementsByTagName('input');

    var updateData = {'name': unitName};

    /// uprawnionych < kart ważnych
    if (generalInfoInputs[0].value < generalInfoInputs[1].value) {
        return;
    }

    /// kart waznych < glosow waznych + glosow niewaznych
    if (generalInfoInputs[1].value < generalInfoInputs[2].value + generalInfoInputs[3].value) {
        return
    }

    for (var i = 0; i < generalInfoInputs.length; ++i) {
        if (generalInfoInputs[i].value < 0) {
            return;
        }
        updateData[generalInfoInputs[i].name] = generalInfoInputs[i].value
    }

    for (var j = 0; j < candidatesResultsInputs.length; ++j) {
        if (candidatesResultsInputs[j].value < 0) {
            return;
        }
        updateData[candidatesResultsInputs[j].name] = candidatesResultsInputs[j].value
    }

    var updateRequest = new XMLHttpRequest();
    var token = localStorage.getItem('token');
    var token_header = 'Token ' + token;
    var csrftoken = Cookies.get('csrftoken');

    updateRequest.open("POST", "/api/update");
    updateRequest.setRequestHeader("Authorization", token_header);
    updateRequest.setRequestHeader("Content-Type", "application/json");
    updateRequest.setRequestHeader('X-CSRFToken', csrftoken);

    updateRequest.send(JSON.stringify(updateData));

    updateRequest.addEventListener('load', function () {
        reload(generalInfo, candidatesResults, resultsDetailed, unitName, isCommunity)
    })
}

function reload(generalInfo, candidatesResults, resultsDetailed, unitName, isCommunity) {

    /// Candidates results
    var storedCandidatesResults = localStorage.getItem("candidates" + unitName);
    if (storedCandidatesResults !== null) {
        addCandidatesResults(storedCandidatesResults, candidatesResults);
    }

    var candidatesInfoRequest = new XMLHttpRequest();
    candidatesInfoRequest.addEventListener("load", function () {
        addCandidatesResults(this.responseText, candidatesResults);
        localStorage.setItem("candidates" + unitName, this.responseText);
    });

    candidatesInfoRequest.open("GET", "/api/kandydaci/" + unitName);
    candidatesInfoRequest.send();

    /// General info
    var storedGeneralInfo = localStorage.getItem("general" + unitName);
    if (storedGeneralInfo !== null) {
        addGeneralInfo(storedGeneralInfo, generalInfo);
    }

    var generalInfoRequest = new XMLHttpRequest();
    generalInfoRequest.addEventListener("load", function () {
        addGeneralInfo(this.responseText, generalInfo);
        localStorage.setItem("general" + unitName, this.responseText);
    });

    generalInfoRequest.open("GET", "/api/zbiorcze/" + unitName);
    generalInfoRequest.send();

    /// Detailed info
    if (isCommunity === 'false') {
        var storedDetailedInfo = localStorage.getItem("detailed" + unitName);
        if (storedDetailedInfo !== null) {
            addDetailedInfo(storedDetailedInfo, resultsDetailed);
        }

        var detailedInfoRequest = new XMLHttpRequest();
        detailedInfoRequest.addEventListener("load", function () {
            addDetailedInfo(this.responseText, resultsDetailed);
            localStorage.setItem("detailed" + unitName, this.responseText);
        });

        detailedInfoRequest.open("GET", "/api/szczegolowe/" + unitName);
        detailedInfoRequest.send();
    }
}

function updateOnTokenStatusChange(right_box, unitName, isCommunity) {
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
            updateOnTokenStatusChange(right_box);
            if (isCommunity === 'true') {
                var generalInfo = document.getElementById("zbiorcze_info");
                var candidatesResults = document.getElementById("wyniki_ogolne_zawartosc");
                var resultsDetailed = document.getElementById("wyniki_szczegolowe_zawartosc");
                reload(generalInfo, candidatesResults, resultsDetailed, unitName, isCommunity);
                addSubmitButtons(generalInfo, candidatesResults, resultsDetailed);
            }
        });
    } else {
        right_box.innerHTML = '';
        var loginButton = document.createElement('a');
        loginButton.appendChild(document.createElement('div'))
            .appendChild(document.createTextNode('login'));
        loginButton.href = '/login';
        loginButton.name = 'login';

        var registerButton = document.createElement('a');
        registerButton.appendChild(document.createElement('div'))
            .appendChild(document.createTextNode('register'));
        registerButton.href = '/signup';
        registerButton.name = 'register';

        right_box.appendChild(loginButton);
        right_box.appendChild(registerButton);
    }
}

function addSubmitButtons(generalInfo, candidatesResults, resultsDetailed, unitName) {
    var token = localStorage.getItem('token');

    var buttonBoxes = document.getElementsByClassName('button_box');

    if (token !== '') {
        for (var i = 0; i < buttonBoxes.length; ++i) {
            var button = document.createElement('button');
            button.innerHTML = 'Wyślij';
            button.type = 'button';
            button.className = 'submit_button';
            buttonBoxes[i].appendChild(button);
            button.addEventListener('click', function () {
                submitUpdate(generalInfo, candidatesResults, resultsDetailed, unitName);
            })
        }
    } else {
        for (var j = 0; j < buttonBoxes.length; ++j) {
            buttonBoxes[j].innerHTML = ''
        }
    }
}
function queryToDict(query) {

    var arr = query.split("&");
    var result = {};
    for (i = 0; i < arr.length; i++) {
        k = arr[i].split('=');
        result[k[0].replace('?', '')] = (k[1] || '');
    }

    // console.log(result);
    return result
}

function replacePolishChars(query) {
    query = query.replace(/%C4%99/g, 'ę');
    query = query.replace(/%C5%9A/g, 'Ś');
    query = query.replace(/%C5%9B/g, 'ś');
    query = query.replace(/%20/g, ' ');
    query = query.replace(/%C3%B3/g, 'ó');
    query = query.replace(/%C5%82/g, 'ł');
    query = query.replace(/%C5%81/g, 'Ł');
    query = query.replace(/%C4%85/g, 'ą');
    query = query.replace(/%C5%84/g, 'ń');
    query = query.replace(/%C4%87/g, 'ć');
    query = query.replace(/%C4%86/g, 'Ć');
    query = query.replace(/%C5%BA/g, 'ź');
    query = query.replace(/%C5%BB/g, 'Ż');
    query = query.replace(/%C5%BC/g, 'ż');
    return query;
}
window.addEventListener("load", function () {
    var query = document.location.search;
    query = replacePolishChars(query);

    if (query === '') {
        unitName = '';
        isCommunity = 'false';
    } else {
        var metadata = queryToDict(query);
        unitName = metadata['name'];
        isCommunity = metadata['is_community'];
    }
    var generalInfo = document.getElementById("zbiorcze_info");
    var candidatesResults = document.getElementById("wyniki_ogolne_zawartosc");
    var resultsDetailed = document.getElementById("wyniki_szczegolowe_zawartosc");

    var right_box = document.getElementById('right_box');

    updateOnTokenStatusChange(right_box, unitName, isCommunity);

    reload(generalInfo, candidatesResults, resultsDetailed, unitName, isCommunity);

    if (isCommunity === 'true') {
        addSubmitButtons(generalInfo, candidatesResults, resultsDetailed, unitName);
    }

});