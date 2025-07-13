// --- Pyodide Engine & UI Orchestration ---

async function setupPyodide() {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '<p class="status-loading">Initializing Python Environment...</p>';
    try {
        let pyodide = await loadPyodide();
        outputDiv.innerHTML = '<p class="status-loading">Loading Physics Disentangler Engine...</p>';
        
        // Fetch and run your main Python script
        const pythonCode = await (await fetch('./law_discovery.py')).text();
        pyodide.runPython(pythonCode);
        
        // Create an instance of the engine
        const engineInstanceCode = "engine = EnhancedPhysicsDisentangler()";
        pyodide.runPython(engineInstanceCode);

        outputDiv.innerHTML = '<p class="status-ready">✅ Environment Ready. Please define a hypothesis.</p>';
        console.log("Physics Disentangler engine is ready.");
        return pyodide;
    } catch (error) {
        outputDiv.innerHTML = `<p class="status-error">CRITICAL ERROR during initialization: ${error}</p>`;
        console.error("Initialization failed:", error);
    }
}

let pyodideReadyPromise = setupPyodide();

async function runDiscovery() {
    const discoverButton = document.getElementById('discoverButton');
    const outputDiv = document.getElementById('output');

    discoverButton.disabled = true;
    outputDiv.innerHTML = '<p class="status-loading">Disentangling...</p>';

    let pyodide = await pyodideReadyPromise;
    if (!pyodide) {
        outputDiv.innerHTML = '<p class="status-error">Initialization failed. Please refresh the page.</p>';
        discoverButton.disabled = false;
        return;
    }

    // Get values from the UI
    const output_quantity = document.getElementById('output_quantity').value.trim();
    const input_quantities_str = document.getElementById('input_quantities').value.trim();
    const constants_str = document.getElementById('constants_to_include').value.trim();
    const auto_search = document.getElementById('auto_search').checked;

    if (!output_quantity || !input_quantities_str) {
        outputDiv.innerHTML = '<p class="status-error">Please provide at least an Output and one Input quantity.</p>';
        discoverButton.disabled = false;
        return;
    }

    // Convert comma-separated strings to JS arrays, filtering out empty strings
    const input_quantities = input_quantities_str.split(',').map(s => s.trim()).filter(Boolean);
    const constants_to_include = constants_str.split(',').map(s => s.trim()).filter(Boolean);

    try {
        // Get a proxy for the engine instance
        const engine = pyodide.globals.get('engine');
        
        // Call the Python method. Pyodide automatically converts JS types.
        const resultProxy = engine.discover_relationship(
            output_quantity,
            input_quantities,
            constants_to_include,
            auto_search,
            true // verbose mode for the search
        );

        // Convert the Python dictionary (PyProxy) to a JavaScript object
        const result = resultProxy.toJs({ dict_converter: Object.fromEntries });
        
        displayResult(result);

    } catch (error) {
        outputDiv.innerHTML = `<p class="status-error">An error occurred during discovery:<br>${error}</p>`;
        console.error(error);
    } finally {
        discoverButton.disabled = false;
    }
}

function displayResult(result) {
    const outputDiv = document.getElementById('output');
    let html = '';

    if (result.get('success')) {
        html += `<div class="result-success">`;
        html += `<h3>✅ Discovery Successful</h3>`;
        if (result.has('message') && result.get('message').includes('Auto-search')) {
             html += `<p class="message-info">${result.get('message')}</p>`;
        }
        html += `<p class="formula">${result.get('formula')}</p>`;

        if (result.has('validation')) {
            const validation = result.get('validation');
            const confidence = validation.get('confidence_score') * 100;
            html += `<div class="validation-box">`;
            html += `<h4>Validation Report</h4>`;
            html += `<p><strong>Confidence Score:</strong> <span style="font-weight: bold; color: ${confidence > 80 ? 'green' : 'orange'};">${confidence.toFixed(0)}%</span></p>`;
            if (validation.has('warnings') && validation.get('warnings').length > 0) {
                 html += `<p><strong>Warnings:</strong></p><ul>`;
                 validation.get('warnings').forEach(w => {
                     html += `<li>- ${w}</li>`;
                 });
                 html += `</ul>`;
            } else {
                 html += `<p>No obvious physical inconsistencies detected.</p>`;
            }
            html += `</div>`;
        }
        html += `</div>`;
    } else {
        html += `<div class="result-failure">`;
        html += `<h3>❌ Discovery Failed</h3>`;
        // Use pre-wrap to preserve the detailed error message formatting
        html += `<pre class="error-message">${result.get('message')}</pre>`;
        html += `</div>`;
    }

    outputDiv.innerHTML = html;
}


// --- UI Event Listeners ---
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('discoverButton').addEventListener('click', runDiscovery);
    
    // Modal logic
    const modal = document.getElementById("quantitiesModal");
    const link = document.getElementById("showQuantitiesLink");
    const closeButton = modal.querySelector(".close-button");

    link.onclick = async function(event) {
        event.preventDefault();
        
        // Populate the list on demand
        let pyodide = await pyodideReadyPromise;
        if(pyodide) {
            const quantities = pyodide.globals.get('engine').quantities.toJs({ dict_converter: Object.fromEntries });
            const listElement = document.getElementById('quantityList');
            const searchInput = document.getElementById('quantitySearch');
            
            const renderList = (filter = '') => {
                listElement.innerHTML = ''; // Clear previous
                Object.keys(quantities).sort().forEach(key => {
                    if (key.toLowerCase().includes(filter.toLowerCase())) {
                       const li = document.createElement('li');
                       li.textContent = key;
                       listElement.appendChild(li);
                    }
                });
            };
            
            searchInput.onkeyup = () => renderList(searchInput.value);
            renderList(); // Initial render
        }
        
        modal.style.display = "block";
    }
    closeButton.onclick = function() { modal.style.display = "none"; }
    window.onclick = function(event) {
        if (event.target == modal) { modal.style.display = "none"; }
    }
});
