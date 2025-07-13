// main.js (This is the correct version. Use this.)

async function setupPyodide() {
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = '<p class="status-loading">Initializing Python Environment...</p>';
    try {
        let pyodide = await loadPyodide();
        
        outputDiv.innerHTML = '<p class="status-loading">Loading Scientific Libraries (NumPy, SymPy)...</p>';
        await pyodide.loadPackage(["numpy", "sympy"]);

        outputDiv.innerHTML = '<p class="status-loading">Loading Physics Disentangler Engine...</p>';
        
        const cacheBuster = '?v=' + new Date().getTime();
        const pythonCode = await (await fetch('./law_discovery.py' + cacheBuster)).text();
        
        await pyodide.runPythonAsync(pythonCode);
        
        pyodide.runPython("engine = EnhancedPhysicsDisentangler()");
        const engine = pyodide.globals.get('engine');
        engine.initialize();
        
        outputDiv.innerHTML = '<p class="status-ready">✅ Environment Ready. Please define a hypothesis.</p>';
        console.log("Physics Disentangler engine is ready.");
        
        return pyodide;
    } catch (error) {
        console.error("A critical error occurred during initialization:", error);
        outputDiv.innerHTML = `<p class="status-error">CRITICAL ERROR during initialization. Check console. The error is: ${error}</p>`;
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

    const output_quantity = document.getElementById('output_quantity').value.trim();
    const input_quantities_str = document.getElementById('input_quantities').value.trim();
    const constants_str = document.getElementById('constants_to_include').value.trim();
    const auto_search = document.getElementById('auto_search').checked;

    const input_quantities = input_quantities_str.split(',').map(s => s.trim()).filter(Boolean);
    const constants_to_include = constants_str.split(',').map(s => s.trim()).filter(Boolean);

    try {
        const engine = pyodide.globals.get('engine');
        const resultProxy = engine.discover_relationship(
            output_quantity,
            input_quantities,
            constants_to_include,
            auto_search,
            true
        );
        
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
    
    if (result.success) {
        html += `<div class="result-success"><h3>✅ Discovery Successful</h3>`;
        if (result.message) {
             html += `<p class="message-info">${result.message}</p>`;
        }
        html += `<pre class="formula">${result.formula}</pre>`;
        if (result.validation) {
            const validation = result.validation;
            const confidence = validation.confidence_score * 100;
            html += `<div class="validation-box"><h4>Validation Report</h4><p><strong>Confidence Score:</strong> <span style="font-weight: bold; color: green;">${confidence.toFixed(0)}%</span></p>`;
            if (validation.warnings && validation.warnings.length > 0) {
                 html += `<p><strong>Warnings:</strong></p><ul>`;
                 validation.warnings.forEach(w => { html += `<li>- ${w}</li>`; });
                 html += `</ul>`;
            } else {
                 html += `<p>No obvious physical inconsistencies detected.</p>`;
            }
            html += `</div>`;
        }
        html += `</div>`;
    } else {
        html += `<div class="result-failure"><h3>❌ Discovery Failed</h3><pre class="error-message">${result.message}</pre></div>`;
    }
    outputDiv.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('discoverButton').addEventListener('click', runDiscovery);
    const modal = document.getElementById("quantitiesModal");
    const link = document.getElementById("showQuantitiesLink");
    const closeButton = modal.querySelector(".close-button");
    if (link && modal && closeButton) {
        link.onclick = async function(event) {
            event.preventDefault();
            let pyodide = await pyodideReadyPromise;
            if(pyodide) {
                const engine = pyodide.globals.get('engine');
                if (engine && typeof engine.quantities !== 'undefined') {
                    // This part is safe because the echo test doesn't have quantities, it will just be empty.
                    const quantities = (typeof engine.quantities.toJs === 'function') ? engine.quantities.toJs({ dict_converter: Object.fromEntries }) : {};
                    const listElement = document.getElementById('quantityList');
                    const searchInput = document.getElementById('quantitySearch');
                    const renderList = (filter = '') => {
                        listElement.innerHTML = '';
                        Object.keys(quantities).sort().forEach(key => {
                            if (key.toLowerCase().includes(filter.toLowerCase())) {
                               const li = document.createElement('li');
                               li.textContent = key;
                               listElement.appendChild(li);
                            }
                        });
                    };
                    searchInput.onkeyup = () => renderList(searchInput.value);
                    renderList();
                }
            }
            modal.style.display = "block";
        }
        closeButton.onclick = function() { modal.style.display = "none"; }
        window.onclick = function(event) {
            if (event.target == modal) { modal.style.display = "none"; }
        }
    }
});
