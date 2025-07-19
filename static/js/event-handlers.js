// event-handlers.js - Event Handlers Module

function setupEventListeners() {
    // File upload form
    document.getElementById('uploadForm').addEventListener('submit', handleFileUpload);

    // Create VM form
    document.getElementById('createVmForm').addEventListener('submit', handleCreateVm);

    // Delete VM form
    document.getElementById('deleteVmForm').addEventListener('submit', handleDeleteVm);

    // File input change
    document.getElementById('uploadFile').addEventListener('change', function(e) {
        const fileSelected = document.getElementById('fileSelected');
        if (e.target.files.length > 0) {
            fileSelected.textContent = `Selected: ${e.target.files[0].name}`;
            fileSelected.style.display = 'block';
        } else {
            fileSelected.style.display = 'none';
        }
    });
}

async function handleFileUpload(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const messageDiv = document.getElementById('uploadMessage');

    try {
        messageDiv.innerHTML = '<div class="message info">Uploading file...</div>';

        const endpoint = currentUploadProvider === 'aws' ?
            '/api/storage/aws/upload' : '/api/storage/azure/upload';

        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.error) {
            messageDiv.innerHTML = `<div class="message error">Error: ${result.error}</div>`;
        } else {
            messageDiv.innerHTML = `<div class="message success">
                ✅ File uploaded successfully!<br>
                <strong>Name:</strong> ${result.object_name}<br>
                <strong>Size:</strong> ${result.size} bytes<br>
                <strong>Provider:</strong> ${currentUploadProvider.toUpperCase()}
            </div>`;

            // Reset form
            e.target.reset();
            document.getElementById('fileSelected').style.display = 'none';
        }
    } catch (error) {
        messageDiv.innerHTML = `<div class="message error">Upload failed: ${error.message}</div>`;
    }
}

async function handleCreateVm(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const messageDiv = document.getElementById('createVmMessage');

    try {
        messageDiv.innerHTML = '<div class="message info">Creating virtual machine...</div>';

        const data = {
            name: formData.get('name'),
            image_id: formData.get('image_id'),
            size_id: formData.get('size_id'),
            region: formData.get('region')
        };

        // Add location_id for Azure
        if (currentVmProvider === 'azure') {
            data.location_id = data.region;
            delete data.region;
        }

        const endpoint = currentVmProvider === 'aws' ?
            '/api/vm/aws/create' : '/api/vm/azure/create';

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            messageDiv.innerHTML = `<div class="message error">Error: ${result.error}</div>`;
        } else {
            messageDiv.innerHTML = `<div class="message success">
                ✅ Virtual Machine created successfully!<br>
                <strong>Name:</strong> ${result.name}<br>
                <strong>ID:</strong> ${result.id}<br>
                <strong>State:</strong> ${result.state}<br>
                <strong>Provider:</strong> ${currentVmProvider.toUpperCase()}
            </div>`;

            // Reset form
            e.target.reset();

            // Refresh dashboard data
            loadDashboardData();
        }
    } catch (error) {
        messageDiv.innerHTML = `<div class="message error">VM creation failed: ${error.message}</div>`;
    }
}

async function handleDeleteVm(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const messageDiv = document.getElementById('deleteVmMessage');

    // Confirmation dialog
    const vmId = formData.get('node_id');
    if (!confirm(`Are you sure you want to delete VM with ID: ${vmId}?\n\nThis action cannot be undone!`)) {
        return;
    }

    try {
        messageDiv.innerHTML = '<div class="message info">Deleting virtual machine...</div>';

        const data = {
            node_id: vmId
        };

        // Add region for AWS
        if (currentDeleteProvider === 'aws') {
            data.region = formData.get('region');
        }

        const endpoint = currentDeleteProvider === 'aws' ?
            '/api/vm/aws/delete' : '/api/vm/azure/delete';

        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            messageDiv.innerHTML = `<div class="message error">Error: ${result.error}</div>`;
        } else {
            messageDiv.innerHTML = `<div class="message success">
                ✅ Virtual Machine deleted successfully!<br>
                <strong>VM ID:</strong> ${result.node_id}<br>
                <strong>Provider:</strong> ${currentDeleteProvider.toUpperCase()}
            </div>`;

            // Reset form
            e.target.reset();

            // Refresh dashboard data
            loadDashboardData();
        }
    } catch (error) {
        messageDiv.innerHTML = `<div class="message error">VM deletion failed: ${error.message}</div>`;
    }
}