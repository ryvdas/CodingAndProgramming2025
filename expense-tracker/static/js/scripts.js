document.addEventListener("DOMContentLoaded", function() {
    // Fetch the expense data from the backend
    const expenseData = JSON.parse('{{ expenses | tojson | safe }}');
    
    const categories = {};
    
    // Categorize the expenses and sum the amounts per category
    expenseData.forEach(expense => {
        const category = expense[2];
        const amount = expense[3];
        if (categories[category]) {
            categories[category] += amount;
        } else {
            categories[category] = amount;
        }
    });
    
    // Prepare the data for the chart
    const labels = Object.keys(categories);
    const data = Object.values(categories);
    
    const ctx = document.getElementById('expenseChart').getContext('2d');
    const expenseChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses by Category',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});