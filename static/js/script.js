// Fake Document Generator - JavaScript Functions

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));

    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    const targetContent = document.getElementById(tabName);
    if (targetContent) {
        targetContent.classList.add('active');
    }
}

function showResult(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    if (element) {
        const alertClass = isError ? 'alert-error' : 'alert-success';
        element.innerHTML = '<div class="alert ' + alertClass + '">' + message + '</div>';
    }
}

function showContent(elementId, content) {
    let element = document.getElementById(elementId);
    if (!element) {
        const elementsByClass = document.getElementsByClassName(elementId);
        if (elementsByClass.length > 0) {
            element = elementsByClass[0];
        }
    }
    if (element) {
        element.innerHTML = content;
    } else {
        console.warn('Element with id or class "' + elementId + '" not found.');
    }
}

// Make Docs Function - Generate Fake Passport Documents
async function makeDocs() {
    const docsBtn = document.getElementById('make-docs-btn');
    const originalText = docsBtn ? docsBtn.innerHTML : '';

    // Set loading state
    if (docsBtn) {
        docsBtn.classList.add('loading');
        docsBtn.disabled = true;
        docsBtn.innerHTML = '⏳ Generating Documents...';
    }

    try {
        // Call API to generate fake documents
        const response = await fetch('/api/make-docs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });

        const result = await response.json();

        if (response.ok && result.status === 'success') {
            // Display passport documents
            displayPassportDocs(result.data);
        } else {
            showResult('docs-result', '❌ Error: ' + (result.message || 'Failed to generate documents'), true);
        }
    } catch (error) {
        showResult('docs-result', '❌ Network Error: ' + error.message, true);
    } finally {
        // Reset button state
        if (docsBtn) {
            docsBtn.classList.remove('loading');
            docsBtn.disabled = false;
            docsBtn.innerHTML = originalText;
        }
    }
}

// Display Passport Documents in the specified format
function displayPassportDocs(data) {
    const resultDiv = document.getElementById('docs-result');
    
    if (!data || !data.passports || data.passports.length === 0) {
        resultDiv.innerHTML = '<p>⚠️ No documents generated</p>';
        return;
    }

    let html = '<div style="margin-top: 20px;">';
    html += '<h3>Generated Passport Documents:</h3>';
    html += '<hr>';
    html += '<p><strong>No. | Passport Number | Name | Date of Birth | Address</strong></p>';
    html += '<hr>';
    
    data.passports.forEach(function(passport, index) {
        html += '<p>';
        html += 'Passport ' + (index + 1) + ': ';
        html += passport.passport_number + ' - ';
        html += passport.name + ' - ';
        html += 'DOB: ' + passport.dob + ' - ';
        html += 'Address: ' + passport.address;
        html += '</p>';
    });
    
    html += '<hr>';
    html += '<p style="margin-top: 15px;"><strong>Total: ' + data.passports.length + ' documents</strong></p>';
    html += '</div>';
    
    resultDiv.innerHTML = html;
}
