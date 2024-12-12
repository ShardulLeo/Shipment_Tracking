// Route Optimization
document.getElementById('route-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const origin = document.getElementById('origin-route').value.trim();
    const destination = document.getElementById('destination-route').value.trim();

    if (!origin || !destination) {
        document.getElementById('route-details').innerHTML = '<p>Please provide both origin and destination.</p>';
        return;
    }

    try {
        const response = await fetch(`/api/optimize_route?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const route = await response.json();
        // Display sanitized route details
        document.getElementById('route-details').innerHTML = `
            <pre>${JSON.stringify(route, null, 2)}</pre>
        `;
    } catch (error) {
        console.error('Error fetching optimized route:', error);
        document.getElementById('route-details').innerHTML = `<p>${error.message}</p>`;
    }
});

// Submit Feedback
document.getElementById('feedback-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const message = document.getElementById('message').value.trim();

    if (!message || message.length > 500) {
        document.getElementById('feedback-response').innerHTML = '<p>Feedback must be between 1 and 500 characters.</p>';
        return;
    }

    try {
        const response = await fetch('/api/feedback_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: sessionStorage.getItem('user_id'), message })
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const result = await response.json();
        document.getElementById('feedback-response').innerHTML = result.message;
    } catch (error) {
        console.error('Error submitting feedback:', error);
        document.getElementById('feedback-response').innerHTML = `<p>${error.message}</p>`;
    }
});

// Track Shipment
document.getElementById('tracking-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const trackingNumber = document.getElementById('tracking-number').value.trim();

    if (!trackingNumber) {
        document.getElementById('shipment-info').innerHTML = '<p>Please enter a tracking number.</p>';
        return;
    }

    try {
        const response = await fetch(`/api/shipments?tracking_number=${encodeURIComponent(trackingNumber)}`);
        const shipmentInfoDiv = document.getElementById('shipment-info');

        if (response.ok) {
            const shipment = await response.json();
            shipmentInfoDiv.innerHTML = `
                <p><strong>Status:</strong> ${shipment.status}</p>
                <p><strong>Origin:</strong> ${shipment.origin}</p>
                <p><strong>Destination:</strong> ${shipment.destination}</p>
                <p><strong>Estimated Delivery:</strong> ${shipment.estimated_delivery}</p>
            `;
        } else {
            const error = await response.json();
            shipmentInfoDiv.innerHTML = `<p>${error.error || 'An error occurred.'}</p>`;
        }
    } catch (error) {
        document.getElementById('shipment-info').innerHTML = `<p>Error fetching shipment data.</p>`;
    }
});

// Search Shipments
document.getElementById('search-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const status = document.getElementById('status').value.trim();
    const origin = document.getElementById('origin').value.trim();
    const destination = document.getElementById('destination').value.trim();

    try {
        const response = await fetch(`/api/search_shipments?status=${encodeURIComponent(status)}&origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`);
        const searchResultsDiv = document.getElementById('search-results');

        if (response.ok) {
            const results = await response.json();
            searchResultsDiv.innerHTML = `<pre>${JSON.stringify(results, null, 2)}</pre>`;
        } else {
            searchResultsDiv.innerHTML = `<p>Error fetching search results.</p>`;
        }
    } catch (error) {
        searchResultsDiv.innerHTML = `<p>An error occurred while searching shipments.</p>`;
    }
});

// Load Analytics
async function loadAnalytics() {
    const analyticsDiv = document.getElementById('statusChart');

    try {
        const response = await fetch('/api/analytics');
        if (!response.ok) {
            throw new Error('Failed to load analytics data.');
        }
        const data = await response.json();
        if (!data.status_summary || !data.status_summary.length) {
            throw new Error('No analytics data available.');
        }
        const ctx = analyticsDiv.getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.status_summary.map(item => item.status),
                datasets: [{
                    label: 'Total Shipments',
                    data: data.status_summary.map(item => item.total),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                }]
            },
        });
    } catch (error) {
        console.error('Error loading analytics:', error);
        analyticsDiv.innerHTML = `<p>Could not load analytics data.</p>`;
    }
}

loadAnalytics();