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
    var inputBox = document.querySelector("#input_field");
    console.log(inputBox);

    inputBox.addEventListener("input", function () {
        var results_detailed = document.getElementById("wyniki_szczegolowe_zawartosc");

        var detailedInfoRequest = new XMLHttpRequest();
        console.log(inputBox.value)
        var queriedVal = inputBox.value
        detailedInfoRequest.addEventListener("load", function () {
            console.log(inputBox.value)
            console.log(queriedVal)
            if (queriedVal === inputBox.value) {
                addDetailedInfo(this.responseText, results_detailed);
            }
            // localStorage.setItem("detailed" + unitName, this.responseText);
        });

        detailedInfoRequest.open("GET", "/api/search/" + inputBox.value);
        detailedInfoRequest.send();

        // var data = localStorage.getItem("data" + unitName);
        // if (data !== null) {
        //     addCandidatesResults(data);
        // }

        // console.log(candidatesResults)
    });
});
