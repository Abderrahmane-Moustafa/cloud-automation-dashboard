// data-loader.js - Data Loading Module

async function loadDashboardData() {
    try {
        document.body.classList.add('loading');

        // Fetch data from your FastAPI endpoints
        const [awsData, azureData] = await Promise.all([
            fetch('/api/vm/aws').then(r => r.json()),
            fetch('/api/vm/azure').then(r => r.json())
        ]);

        // Update stats
        updateStats(awsData, azureData);

        // Update charts
        updateCharts(awsData, azureData);

        // Load VM status table
        await loadVMStatus();

        // Load billing data for overview
        await loadBillingData();

        // Update timestamp
        document.getElementById('lastUpdated').textContent = new Date().toLocaleString();

    } catch (error) {
        console.error('Error loading dashboard data:', error);
    } finally {
        document.body.classList.remove('loading');
    }
}

async function loadBillingData() {
    try {
        // Fetch billing data from your FastAPI endpoints
        const [awsCurrent, azureCurrent, awsSummary, azureSummary] = await Promise.all([
            fetch('/api/billing/aws').then(r => r.json()),
            fetch('/api/billing/azure').then(r => r.json()),
            fetch('/api/billing/aws/summary?months=6').then(r => r.json()),
            fetch('/api/billing/azure/summary?months=6').then(r => r.json())
        ]);

        // Update current month costs
        if (!awsCurrent.error) {
            document.getElementById('awsCurrentCost').textContent = `$${awsCurrent.totalCost}`;
            document.getElementById('awsCurrentMonth').textContent = awsCurrent.month;
        }

        if (!azureCurrent.error) {
            document.getElementById('azureCurrentCost').textContent = `$${azureCurrent.totalCost}`;
            document.getElementById('azureCurrentMonth').textContent = azureCurrent.month;
        }

        // Update 6-month summary
        if (!awsSummary.error) {
            document.getElementById('aws6MonthCost').textContent = `$${awsSummary.totalCost}`;
            document.getElementById('aws6MonthPeriod').textContent = `${awsSummary.start} to ${awsSummary.end}`;
        }

        if (!azureSummary.error) {
            document.getElementById('azure6MonthCost').textContent = `$${azureSummary.totalCost}`;
            document.getElementById('azure6MonthPeriod').textContent = `${azureSummary.start} to ${azureSummary.end}`;
        }

        // Update total cost in overview
        const totalCost = (awsCurrent.totalCost || 0) + (azureCurrent.totalCost || 0);
        document.getElementById('totalCost').textContent = `$${totalCost.toFixed(2)}`;

    } catch (error) {
        console.error('Error loading billing data:', error);
    }
}

async function loadCPUData() {
    try {
        // First get the list of VMs from both providers
        const [awsVMs, azureVMs] = await Promise.all([
            fetch('/api/vm/aws').then(r => r.json()),
            fetch('/api/vm/azure').then(r => r.json())
        ]);

        const awsInstances = awsVMs.aws_instances || [];
        const azureInstances = azureVMs.azure_vms || [];

        const now = new Date().toLocaleTimeString();

        // Initialize vmCpuData structure if needed
        if (!vmCpuData[now]) {
            vmCpuData[now] = {};
        }

        // Fetch CPU usage for each AWS instance individually
        for (const instance of awsInstances) {
            if (instance.id && (instance.state === 'running' || instance.state === 0)) {
                try {
                    const response = await fetch(`/api/vm/aws/usage?instance_id=${instance.id}&region=us-east-1`);
                    const data = await response.json();

                    const vmKey = `AWS-${instance.name}`;
                    if (data.cpu_utilization_percent !== null && data.cpu_utilization_percent !== undefined && typeof data.cpu_utilization_percent === 'number') {
                        vmCpuData[now][vmKey] = data.cpu_utilization_percent;
                        console.log(`✅ AWS ${instance.name}: ${data.cpu_utilization_percent}%`);
                    } else {
                        vmCpuData[now][vmKey] = 0;
                        console.warn(`❌ No valid CPU data for AWS ${instance.name}`);
                    }
                } catch (error) {
                    console.error(`❌ Error fetching CPU for AWS instance ${instance.name}:`, error);
                    vmCpuData[now][`AWS-${instance.name}`] = 0;
                }
            }
        }

        // Fetch CPU usage for each Azure instance individually
        for (const instance of azureInstances) {
            if (instance.name && (instance.state === 'running' || instance.state === 0)) {
                try {
                    let resourceId;

                    if (instance.resource_id) {
                        resourceId = instance.resource_id;
                    } else {
                        const subscriptionId = "a6bd69c1-f4b9-498e-970f-008dcc1d677f";
                        const resourceGroup = "TH-MACHINE_GROUP";
                        resourceId = `/subscriptions/${subscriptionId}/resourceGroups/${resourceGroup}/providers/Microsoft.Compute/virtualMachines/${instance.name}`;
                    }

                    const response = await fetch(`/api/vm/azure/usage?resource_id=${encodeURIComponent(resourceId)}`);
                    const data = await response.json();

                    const vmKey = `Azure-${instance.name}`;
                    if (data.cpu_utilization_percent !== null && data.cpu_utilization_percent !== undefined && typeof data.cpu_utilization_percent === 'number') {
                        vmCpuData[now][vmKey] = data.cpu_utilization_percent;
                        console.log(`✅ Azure ${instance.name}: ${data.cpu_utilization_percent}%`);
                    } else {
                        vmCpuData[now][vmKey] = 0;
                        console.warn(`❌ No valid CPU data for Azure ${instance.name}`);
                    }
                } catch (error) {
                    console.error(`❌ Error fetching CPU for Azure instance ${instance.name}:`, error);
                    vmCpuData[now][`Azure-${instance.name}`] = 0;
                }
            }
        }

        // Keep only last 10 data points
        const timeKeys = Object.keys(vmCpuData);
        if (timeKeys.length > 10) {
            timeKeys.slice(0, timeKeys.length - 10).forEach(key => {
                delete vmCpuData[key];
            });
        }

        // Update chart
        updateCPUChart();

        console.log(`CPU Data Updated for time ${now}:`, vmCpuData[now]);

    } catch (error) {
        console.error('Error loading CPU data:', error);
    }
}

async function loadVMStatus() {
    try {
        const [awsStatus, azureStatus] = await Promise.all([
            fetch('/api/vm/aws/status').then(r => r.json()),
            fetch('/api/vm/azure/status').then(r => r.json())
        ]);

        const tbody = document.getElementById('vmTableBody');
        tbody.innerHTML = '';

        // Add AWS VMs
        (awsStatus.aws_status || []).forEach(vm => {
            const row = createVMRow(vm, 'AWS');
            tbody.appendChild(row);
        });

        // Add Azure VMs
        (azureStatus.azure_status || []).forEach(vm => {
            const row = createVMRow(vm, 'Azure');
            tbody.appendChild(row);
        });

        if (tbody.children.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 40px;">No VMs found</td></tr>';
        }

    } catch (error) {
        console.error('Error loading VM status:', error);
        document.getElementById('vmTableBody').innerHTML =
            '<tr><td colspan="5" style="text-align: center; padding: 40px;">Error loading VM data</td></tr>';
    }
}

function updateStats(awsData, azureData) {
    const awsVMs = awsData.aws_instances || [];
    const azureVMs = azureData.azure_vms || [];

    const totalVMs = awsVMs.length + azureVMs.length;
    const runningVMs = [...awsVMs, ...azureVMs].filter(vm =>
        vm.state === 'running' || vm.state === 0
    ).length;
    const stoppedVMs = totalVMs - runningVMs;

    document.getElementById('totalVMs').textContent = totalVMs;
    document.getElementById('runningVMs').textContent = runningVMs;
    document.getElementById('stoppedVMs').textContent = stoppedVMs;
}