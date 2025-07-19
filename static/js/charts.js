// charts.js - Chart Management Module
let vmStateChart, providerChart, cpuChart;
let vmCpuData = {}; // Store individual VM CPU data

function initializeCharts() {
    // VM State Pie Chart
    const vmStateCtx = document.getElementById('vmStateChart').getContext('2d');
    vmStateChart = new Chart(vmStateCtx, {
        type: 'pie',
        data: {
            labels: ['Running', 'Stopped'],
            datasets: [{
                data: [0, 0],
                backgroundColor: ['#27ae60', '#e74c3c'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

    // Provider Bar Chart
    const providerCtx = document.getElementById('providerChart').getContext('2d');
    providerChart = new Chart(providerCtx, {
        type: 'bar',
        data: {
            labels: ['AWS', 'Azure'],
            datasets: [{
                label: 'VM Count',
                data: [0, 0],
                backgroundColor: ['#FF9500', '#0078D4'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // CPU Usage Chart
    const cpuCtx = document.getElementById('cpuChart').getContext('2d');
    cpuChart = new Chart(cpuCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [] // Dynamic datasets for individual VMs
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        boxWidth: 20
                    }
                }
            }
        }
    });
}

function updateCharts(awsData, azureData) {
    const awsVMs = awsData.aws_instances || [];
    const azureVMs = azureData.azure_vms || [];

    const allVMs = [...awsVMs, ...azureVMs];
    const runningCount = allVMs.filter(vm => vm.state === 'running' || vm.state === 0).length;
    const stoppedCount = allVMs.length - runningCount;

    // Update VM State Chart (removed pending)
    vmStateChart.data.datasets[0].data = [runningCount, stoppedCount];
    vmStateChart.update();

    // Update Provider Chart
    providerChart.data.datasets[0].data = [awsVMs.length, azureVMs.length];
    providerChart.update();
}

function updateCPUChart() {
    const timeLabels = Object.keys(vmCpuData).sort();

    // Get all unique VM names across all time points
    const allVMs = new Set();
    timeLabels.forEach(time => {
        Object.keys(vmCpuData[time]).forEach(vm => allVMs.add(vm));
    });

    // Colors for different VMs
    const awsColors = ['#FF9500', '#FF7A00', '#FF6600', '#E55100', '#BF360C'];
    const azureColors = ['#0078D4', '#005A9E', '#004578', '#003052', '#001B2E'];

    // Create datasets for each VM
    const datasets = [];
    let awsIndex = 0;
    let azureIndex = 0;

    Array.from(allVMs).sort().forEach(vmName => {
        const isAWS = vmName.startsWith('AWS-');
        const displayName = vmName.replace('AWS-', '').replace('Azure-', '');

        const color = isAWS ? awsColors[awsIndex++ % awsColors.length] : azureColors[azureIndex++ % azureColors.length];

        const data = timeLabels.map(time => vmCpuData[time][vmName] || 0);

        datasets.push({
            label: `${isAWS ? '🟠 AWS' : '🔵 Azure'} - ${displayName}`,
            data: data,
            borderColor: color,
            backgroundColor: color + '20', // Add transparency
            fill: false,
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 3,
            pointHoverRadius: 5
        });
    });

    // Update chart
    cpuChart.data.labels = timeLabels;
    cpuChart.data.datasets = datasets;
    cpuChart.update();

    // Update status information
    const statusDiv = document.getElementById('cpuStatus');
    const lastUpdateSpan = document.getElementById('lastCpuUpdate');
    const dataPointsSpan = document.getElementById('cpuDataPoints');

    if (statusDiv && lastUpdateSpan && dataPointsSpan) {
        statusDiv.style.display = 'block';
        lastUpdateSpan.textContent = new Date().toLocaleTimeString();
        dataPointsSpan.textContent = `${timeLabels.length} time points, ${allVMs.size} VMs`;
    }
}