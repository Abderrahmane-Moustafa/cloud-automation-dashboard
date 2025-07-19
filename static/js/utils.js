// utils.js - Utility Functions Module

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function createVMRow(vm, provider) {
    const row = document.createElement('tr');

    const stateClass = vm.state === 'running' || vm.state === 0 ? 'status-running' : 'status-stopped';
    const pingClass = vm.ping_status === 'reachable' ? 'status-reachable' : 'status-unreachable';

    row.innerHTML = `
        <td><strong>${vm.name}</strong></td>
        <td>${provider}</td>
        <td><span class="status-badge ${stateClass}">${vm.state === 0 ? 'running' : vm.state}</span></td>
        <td>${vm.public_ip || 'N/A'}</td>
        <td><span class="status-badge ${pingClass}">${vm.ping_status}</span></td>
    `;

    return row;
}