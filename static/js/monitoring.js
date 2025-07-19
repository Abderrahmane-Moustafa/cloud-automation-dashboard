// monitoring.js - Monitoring Module

let autoRefreshInterval = null;

function refreshMonitoringData() {
    const button = event.target;
    const originalText = button.textContent;

    button.textContent = '🔄 Refreshing...';
    button.disabled = true;

    loadCPUData().finally(() => {
        button.textContent = originalText;
        button.disabled = false;
    });
}

function toggleAutoRefresh() {
    const button = document.getElementById('autoRefreshText');

    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        button.textContent = 'Enable Auto-Refresh';
    } else {
        autoRefreshInterval = setInterval(loadCPUData, 30000); // Refresh every 30 seconds
        button.textContent = 'Disable Auto-Refresh';
    }
}