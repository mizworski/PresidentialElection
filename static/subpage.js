// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addCandidatesResults(serializedData, candidatesResults) {
    while (candidatesResults.children.length !== 0) {
        candidatesResults.removeChild(candidatesResults.firstChild);
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

        if (isLogged === 'True' && isCommunity === 'True') {
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

    var data = JSON.parse(serializedData);
    for (var i = 0; i < data.length; ++i) {
        var row = data[i];
        var label = row['label'];
        var value = row['value'];

        var row_wrapper = document.createElement('div');

        var label_wrapper = document.createElement('div');
        label_wrapper.innerHTML = label;
        row_wrapper.appendChild(label_wrapper);

        if (isLogged === 'True' && isCommunity === 'True') { // super kurwa język
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

window.addEventListener("load", function () {
    var generalInfo = document.getElementById("zbiorcze_info");
    var candidatesResults = document.getElementById("wyniki_ogolne_zawartosc");
    var resultsDetailed = document.getElementById("wyniki_szczegolowe_zawartosc");

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
    if (isCommunity === 'False') {
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

});