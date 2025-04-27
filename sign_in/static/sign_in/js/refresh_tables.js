function refreshTable(url, elementId) {
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("Network response was not OK");
            return response.text();
        })
        .then(html => {
            document.getElementById(elementId).innerHTML = html;
        })
        .catch(err => {
            console.error(`Error refreshing ${elementId}:`, err);
        });
}

function setupAutoRefresh() {
    setInterval(() => {
        refreshTable('/partials/current/', 'current-students-table');
        refreshTable('/partials/recent/', 'recently-left-table');
    }, 5000); // Refreshes every 5 seconds
}

document.addEventListener("DOMContentLoaded", setupAutoRefresh);