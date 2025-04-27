function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("records-table");
    switching = true;
    dir = "asc"; 

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;

            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];

            var xDataTime = x.getAttribute('data-time');
            var yDataTime = y.getAttribute('data-time');
            var xDataDate = x.getAttribute('data-date');
            var yDataDate = y.getAttribute('data-date');

            var xValue, yValue;

            if (xDataTime !== null && yDataTime !== null) {
                // Compare as Date objects
                xValue = new Date(xDataTime);
                yValue = new Date(yDataTime);
            } else if (xDataDate !== null && yDataDate !== null) {
                // Compare as Date objects
                xValue = new Date(xDataDate);
                yValue = new Date(yDataDate);
            } else {
                // Compare as strings
                xValue = x.innerText.toLowerCase();
                yValue = y.innerText.toLowerCase();
            }

            if (dir == "asc") {
                if (xValue > yValue) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (xValue < yValue) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
