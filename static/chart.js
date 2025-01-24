fetch('/api/expenses')
  .then(response => response.json())
  .then(data => {
    const ctx = document.getElementById('categoryPieChart').getContext('2d');
    const chart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Cost:',
          data: data.values,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 206, 86)',
            'rgb(75, 192, 192)',
            'rgb(153, 102, 255)',
            'rgb(255, 159, 64)'
          ]
        }]
      }
    });
  })
  .catch(error => console.error('Error fetching chart data:', error));
