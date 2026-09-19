function toggleMenu() {
    const menu = document.getElementById("navMenu");

    if (menu) {
        menu.classList.toggle("open");
    }
}


/*
   Analytics chart.
   Chart.js is loaded from a CDN only on this page.
*/
const chartElement = document.getElementById("comparisonChart");

if (chartElement) {

    const labels = Array.from({length: 16}, (_, i) => i);

    const romData = labels.map(x => (3 * x + 5) % 16);

    const formulaData = labels.map(x => (3 * x + 5) % 16);

    new Chart(chartElement, {
        type: "line",

        data: {
            labels: labels,

            datasets: [
                {
                    label: "ROM Output",
                    data: romData,
                    tension: 0.25,
                    borderWidth: 3
                },
                {
                    label: "Formula Output",
                    data: formulaData,
                    tension: 0.25,
                    borderWidth: 2
                }
            ]
        },

        options: {
            responsive: true,

            scales: {
                y: {
                    beginAtZero: true,
                    max: 15
                }
            }
        }
    });
}
