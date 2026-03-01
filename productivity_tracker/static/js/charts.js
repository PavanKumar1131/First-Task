// charts.js - handles chart rendering using Chart.js
// displays weekly progress and category breakdown

// simple clean colors
const chartColors = {
    primary: '#2563eb',
    secondary: '#6b7280',
    accent: '#8b5cf6',
    success: '#16a34a',
    warning: '#f59e0b',
    danger: '#dc2626'
};

// category colors - simple distinct colors
const categoryColors = {
    'Work': '#2563eb',
    'Study': '#8b5cf6',
    'Personal': '#06b6d4',
    'Health': '#16a34a',
    'Other': '#6b7280'
};

// initialize all charts on page load
function initCharts() {
    // fetch data from server
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            renderWeeklyChart(data.weeklyData);
            renderCategoryChart(data.categoryTime);
            renderStatusChart(data.statusData);
        })
        .catch(error => {
            console.error('Error loading chart data:', error);
        });
}

// weekly completed tasks bar chart
function renderWeeklyChart(weeklyData) {
    let ctx = document.getElementById('weeklyChart');
    if (!ctx) return;
    
    let labels = Object.keys(weeklyData);
    let values = Object.values(weeklyData);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Completed Tasks',
                data: values,
                backgroundColor: chartColors.primary,
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// time spent per category doughnut chart
function renderCategoryChart(categoryTime) {
    let ctx = document.getElementById('categoryChart');
    if (!ctx) return;
    
    let labels = Object.keys(categoryTime);
    let values = Object.values(categoryTime);
    let colors = labels.map(cat => categoryColors[cat] || '#999');
    
    // check if there's any data
    let hasData = values.some(v => v > 0);
    
    if (!hasData) {
        // show message if no data
        ctx.parentElement.innerHTML += '<p class="text-center mt-20">No time tracked yet</p>';
    }
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let mins = context.raw;
                            let hrs = Math.floor(mins / 60);
                            let remainMins = mins % 60;
                            if (hrs > 0) {
                                return `${context.label}: ${hrs}h ${remainMins}m`;
                            }
                            return `${context.label}: ${mins}m`;
                        }
                    }
                }
            }
        }
    });
}

// completed vs pending pie chart
function renderStatusChart(statusData) {
    let ctx = document.getElementById('statusChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Completed', 'Pending'],
            datasets: [{
                data: [statusData.Completed, statusData.Pending],
                backgroundColor: [chartColors.success, chartColors.warning],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// pdf export using jspdf
function exportToPDF() {
    // make sure jspdf is loaded
    if (typeof jspdf === 'undefined' && typeof window.jspdf === 'undefined') {
        alert('PDF library not loaded. Please try again.');
        return;
    }
    
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // title
    doc.setFontSize(20);
    doc.setTextColor(74, 111, 165);
    doc.text('Productivity Report', 20, 20);
    
    // date
    doc.setFontSize(10);
    doc.setTextColor(100);
    let today = new Date().toLocaleDateString();
    doc.text(`Generated: ${today}`, 20, 30);
    
    // get stats from page
    let totalTasks = document.getElementById('stat-total')?.textContent || '0';
    let completedTasks = document.getElementById('stat-completed')?.textContent || '0';
    let pendingTasks = document.getElementById('stat-pending')?.textContent || '0';
    let totalTime = document.getElementById('stat-time')?.textContent || '0h 0m';
    
    // summary section
    doc.setFontSize(14);
    doc.setTextColor(0);
    doc.text('Summary', 20, 45);
    
    doc.setFontSize(11);
    doc.text(`Total Tasks: ${totalTasks}`, 25, 55);
    doc.text(`Completed: ${completedTasks}`, 25, 63);
    doc.text(`Pending: ${pendingTasks}`, 25, 71);
    doc.text(`Total Time: ${totalTime}`, 25, 79);
    
    // add note
    doc.setFontSize(9);
    doc.setTextColor(100);
    doc.text('This report was generated from the Productivity Tracker app.', 20, 100);
    
    // save the pdf
    doc.save('productivity_report.pdf');
}

// load charts when dom is ready
document.addEventListener('DOMContentLoaded', function() {
    // only init charts if we're on dashboard page
    if (document.getElementById('weeklyChart')) {
        initCharts();
    }
});
