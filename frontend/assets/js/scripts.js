// Form Validation Logic
document.addEventListener('DOMContentLoaded', function () {

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        } else {
          event.preventDefault(); // For demo purposes, we usually prevent real submission
          // Example: Show success message or trigger a sweetalert
          alert("Success! Form was valid.");
        }

        form.classList.add('was-validated')
      }, false)
    })

  // Sticky navbar for Landing Page
  const navbar = document.querySelector('.navbar-custom');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  // Dashboard Initialize Charts (if on dashboard page)
  initCharts();
});

function initCharts() {
  const billingChartCtx = document.getElementById('billingChart');
  if (billingChartCtx) {
    new Chart(billingChartCtx, {
      type: 'doughnut',
      data: {
        labels: ['Pending', 'Paid'],
        datasets: [{
          data: [32, 68],
          backgroundColor: [
            '#f5b942', // Dash yellow
            '#1bb2a6'  // Dash teal
          ],
          borderWidth: 0,
          cutout: '75%'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              usePointStyle: true,
              boxWidth: 8
            }
          }
        }
      }
    });
  }

  const consultationChartCtx = document.getElementById('consultationChart');
  if (consultationChartCtx) {
    new Chart(consultationChartCtx, {
      type: 'bar',
      data: {
        labels: ['Phone', 'Video', 'Offline'],
        datasets: [{
          data: [4, 12, 24],
          backgroundColor: [
            '#f5b942', // Yellow
            '#1bb2a6', // Teal
            '#816bfb'  // Purple
          ],
          borderRadius: 5,
          barThickness: 15
        }]
      },
      options: {
        indexAxis: 'y', // Horizontal bar chart
        responsive: true,
        scales: {
          x: { display: false },
          y: { 
            grid: { display: false },
            border: { display: false }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}
