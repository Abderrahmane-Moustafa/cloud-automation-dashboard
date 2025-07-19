// main-dashboard.js - Main Dashboard Module

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    loadDashboardData();
    loadBillingData();
    loadCPUData();
    setupEventListeners();

    // Auto-refresh every 60 seconds
    setInterval(loadDashboardData, 60000);
});