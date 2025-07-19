// tab-manager.js - Tab Management Module

let currentUploadProvider = 'aws';
let currentVmProvider = 'aws';
let currentDeleteProvider = 'aws';

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked nav tab
    event.target.classList.add('active');

    // Load data for specific tabs
    if (tabName === 'billing') {
        loadBillingData();
    } else if (tabName === 'monitoring') {
        loadCPUData();
    }
}

function selectUploadProvider(provider) {
    currentUploadProvider = provider;

    // Update provider buttons
    const parentDiv = event.target.closest('.provider-selector');
    parentDiv.querySelectorAll('.provider-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

function selectVmProvider(provider) {
    currentVmProvider = provider;

    // Update provider buttons
    const parentDiv = event.target.closest('.provider-selector');
    parentDiv.querySelectorAll('.provider-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Show/hide appropriate options
    const awsOptions = document.querySelectorAll('.aws-option');
    const azureOptions = document.querySelectorAll('.azure-option');

    if (provider === 'aws') {
        awsOptions.forEach(opt => opt.style.display = 'block');
        azureOptions.forEach(opt => opt.style.display = 'none');
    } else {
        awsOptions.forEach(opt => opt.style.display = 'none');
        azureOptions.forEach(opt => opt.style.display = 'block');
    }

    // Reset form values
    document.getElementById('vmSizeId').value = '';
    document.getElementById('vmRegion').value = '';
}

function selectDeleteProvider(provider) {
    currentDeleteProvider = provider;

    // Update provider buttons
    const parentDiv = event.target.closest('.provider-selector');
    parentDiv.querySelectorAll('.provider-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Show/hide region group for AWS
    const regionGroup = document.getElementById('deleteRegionGroup');
    if (provider === 'aws') {
        regionGroup.style.display = 'block';
    } else {
        regionGroup.style.display = 'none';
    }
}