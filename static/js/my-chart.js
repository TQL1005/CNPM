function drawRevenueChart(labels, data, type) {
const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lượt bay',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'rgba(198, 111, 90, 0.8)', 'rgba(255, 199, 120, 0.8)']
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
}