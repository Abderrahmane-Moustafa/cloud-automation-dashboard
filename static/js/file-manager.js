// file-manager.js - File Management Module

async function loadS3Files() {
    const bucketName = document.getElementById('s3BucketName').value.trim();
    const fileListDiv = document.getElementById('s3FileList');

    if (!bucketName) {
        fileListDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #e74c3c;">Please enter a bucket name</div>';
        return;
    }

    try {
        fileListDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">Loading files...</div>';

        const response = await fetch(`/api/storage/aws/list?container_name=${encodeURIComponent(bucketName)}`);
        const result = await response.json();

        if (result.error || result.files.error) {
            fileListDiv.innerHTML = `<div style="text-align: center; padding: 20px; color: #e74c3c;">Error: ${result.error || result.files.error}</div>`;
        } else {
            const files = result.files;

            if (files.length === 0) {
                fileListDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">No files found in this bucket</div>';
            } else {
                fileListDiv.innerHTML = files.map(file => `
                    <div class="file-item">
                        <div class="file-info">
                            <div class="file-name">📄 ${file.name}</div>
                            <div class="file-size">${formatFileSize(file.size)}</div>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        fileListDiv.innerHTML = `<div style="text-align: center; padding: 20px; color: #e74c3c;">Error loading files: ${error.message}</div>`;
    }
}

async function loadAzureFiles() {
    const containerName = document.getElementById('azureContainerName').value.trim();
    const fileListDiv = document.getElementById('azureFileList');

    if (!containerName) {
        fileListDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #e74c3c;">Please enter a container name</div>';
        return;
    }

    try {
        fileListDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">Loading files...</div>';

        const response = await fetch(`/api/storage/azure/list?container_name=${encodeURIComponent(containerName)}`);
        const result = await response.json();

        if (result.error || result.files.error) {
            fileListDiv.innerHTML = `<div style="text-align: center; padding: 20px; color: #e74c3c;">Error: ${result.error || result.files.error}</div>`;
        } else {
            const files = result.files;

            if (files.length === 0) {
                fileListDiv.innerHTML = '<div style="text-align: center; padding: 20px; color: #666;">No files found in this container</div>';
            } else {
                fileListDiv.innerHTML = files.map(file => `
                    <div class="file-item">
                        <div class="file-info">
                            <div class="file-name">📄 ${file.name}</div>
                            <div class="file-size">${formatFileSize(file.size)}</div>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        fileListDiv.innerHTML = `<div style="text-align: center; padding: 20px; color: #e74c3c;">Error loading files: ${error.message}</div>`;
    }
}