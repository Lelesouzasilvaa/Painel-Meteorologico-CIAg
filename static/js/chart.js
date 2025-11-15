    window.onload = () => {
  
    const ctx = document.getElementById('graficoHorario').getContext('2d');

    const labels = typeof CHART_TIMES !== 'undefined' ? CHART_TIMES : [];
    const temperatures = typeof CHART_TEMPS !== 'undefined' ? CHART_TEMPS : [];

    const hourlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Temperatura (°C)',
                data: temperatures,
                borderColor: 'var(--highlight-blue)', 
                backgroundColor: 'rgba(0, 188, 212, 0.15)', 
                pointBackgroundColor: 'var(--highlight-blue)',
                tension: 0.4, 
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    display: false,
                    grid: { display: false }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: 'var(--text-muted)' }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'var(--card-dark)',
                    titleColor: 'var(--text-light)',
                    bodyColor: 'var(--text-light)',
                    borderColor: 'var(--highlight-blue)',
                    borderWidth: 1
                }
            }
        }
    });
};