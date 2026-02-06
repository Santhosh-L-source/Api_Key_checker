// Mode switching
document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const mode = this.getAttribute('data-mode');
        switchMode(mode);
    });
});

function switchMode(mode) {
    // Update buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');

    // Update content
    document.querySelectorAll('.mode-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${mode}-mode`).classList.add('active');
}

// Toggle password visibility
function togglePassword() {
    const input = document.getElementById('api-key');
    const type = input.type === 'password' ? 'text' : 'password';
    input.type = type;
}

// Validate single key
async function validateSingleKey() {
    const apiType = document.getElementById('api-type').value;
    const key = document.getElementById('api-key').value;

    if (!apiType) {
        showAlert('Please select an API type', 'error');
        return;
    }

    if (!key) {
        showAlert('Please enter an API key', 'error');
        return;
    }

    const btn = event.target;
    const loader = btn.querySelector('.loader');
    btn.disabled = true;
    loader.classList.remove('hidden');

    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                api_type: apiType,
                key: key,
            }),
        });

        const result = await response.json();

        if (!response.ok) {
            showAlert(result.error || 'Validation failed', 'error');
            return;
        }

        displaySingleResult(result);
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
        loader.classList.add('hidden');
    }
}

// Display single result
function displaySingleResult(result) {
    const resultBox = document.getElementById('result-single');
    resultBox.innerHTML = '';

    const statusClass = result.is_active ? 'success' : 'error';
    resultBox.className = `result-box show ${statusClass}`;

    let html = `
        <div class="result-item ${result.is_active ? 'active' : 'inactive'}">
            <div class="result-header">
                <div class="result-status">${result.status}</div>
                <div class="result-key-preview">${result.key_preview}</div>
            </div>
            <div class="result-details">
                <strong>API Type:</strong> ${result.api_type.toUpperCase()}<br>
                <strong>Format Valid:</strong> ${result.format_valid ? '✅ Yes' : '❌ No'}<br>
                <strong>Key Active:</strong> ${result.is_active ? '✅ Yes' : '❌ No'}
            </div>
    `;

    if (result.error) {
        html += `<div class="result-error"><strong>Error:</strong> ${result.error}</div>`;
    }

    html += `</div>`;
    resultBox.innerHTML = html;
}

// Validate batch keys
async function validateBatchKeys() {
    const apiType = document.getElementById('batch-api-type').value;
    const keysText = document.getElementById('batch-keys').value;

    if (!apiType) {
        showAlert('Please select an API type', 'error');
        return;
    }

    if (!keysText.trim()) {
        showAlert('Please enter at least one API key', 'error');
        return;
    }

    const keys = keysText.split('\n').filter(k => k.trim());

    const btn = event.target;
    const loader = btn.querySelector('.loader');
    btn.disabled = true;
    loader.classList.remove('hidden');

    try {
        const response = await fetch('/api/batch-validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                api_type: apiType,
                keys: keys,
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            showAlert(data.error || 'Validation failed', 'error');
            return;
        }

        displayBatchResults(data.results);
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
        loader.classList.add('hidden');
    }
}

// Display batch results
function displayBatchResults(results) {
    const resultBox = document.getElementById('result-batch');
    resultBox.innerHTML = '';

    const validCount = results.filter(r => r.is_active).length;
    const invalidCount = results.filter(r => !r.is_active && r.format_valid).length;
    const formatErrorCount = results.filter(r => !r.format_valid).length;

    const statusClass = validCount > 0 && invalidCount === 0 ? 'success' : invalidCount > 0 ? 'warning' : 'error';
    resultBox.className = `result-box show ${statusClass}`;

    let html = `
        <div class="batch-summary">
            <div class="summary-card valid">
                <h4>Valid & Active</h4>
                <div class="number">${validCount}</div>
            </div>
            <div class="summary-card invalid">
                <h4>Invalid/Inactive</h4>
                <div class="number">${invalidCount}</div>
            </div>
            <div class="summary-card">
                <h4>Format Errors</h4>
                <div class="number">${formatErrorCount}</div>
            </div>
        </div>
    `;

    results.forEach((result, index) => {
        const itemClass = result.is_active ? 'active' : result.format_valid ? 'inactive' : 'invalid-format';
        html += `
            <div class="result-item ${itemClass}">
                <div class="result-header">
                    <div class="result-status">#${index + 1}: ${result.status}</div>
                    <div class="result-key-preview">${result.key_preview}</div>
                </div>
                <div class="result-details">
                    <strong>Format Valid:</strong> ${result.format_valid ? '✅ Yes' : '❌ No'}<br>
                    <strong>Key Active:</strong> ${result.is_active ? '✅ Yes' : '❌ No'}
                </div>
        `;

        if (result.error) {
            html += `<div class="result-error"><strong>Error:</strong> ${result.error}</div>`;
        }

        html += `</div>`;
    });

    resultBox.innerHTML = html;
}

// Show alert
function showAlert(message, type = 'info') {
    const resultBox = document.querySelector('.result-box.show') || document.getElementById('result-single');
    resultBox.className = `result-box show ${type}`;
    resultBox.innerHTML = `<div style="padding: 15px;">${message}</div>`;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to validate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const btn = document.querySelector('.mode-content.active .btn-primary');
        if (btn) btn.click();
    }
});
