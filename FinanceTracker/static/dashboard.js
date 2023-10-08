document.addEventListener("DOMContentLoaded", function () {
    // Dummy data for the first chart (bar chart)
    const labels1 = ["January", "February", "March", "April", "May"];
    const data1 = [65, 59, 80, 81, 56];

    // Dummy data for the second chart (line chart)
    const labels2 = ["June", "July", "August", "September", "October"];
    const data2 = [45, 70, 42, 60, 75];

    // Dummy data for the third chart (donut chart)
    const labels3 = ["Red", "Blue", "Yellow"];
    const data3 = [30, 45, 25];
    const colors3 = ["#FF6384", "#36A2EB", "#FFCE56"];

    // Create the first Chart.js chart (bar chart)
    const ctx1 = document.getElementById("chart1").getContext("2d");
    const chart1 = new Chart(ctx1, {
        type: "bar",
        data: {
            labels: labels1,
            datasets: [
                {
                    label: "Data 1",
                    data: data1,
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });

    // Create the second Chart.js chart (line chart)
    const ctx2 = document.getElementById("chart2").getContext("2d");
    const chart2 = new Chart(ctx2, {
        type: "line",
        data: {
            labels: labels2,
            datasets: [
                {
                    label: "Data 2",
                    data: data2,
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 2,
                    fill: false,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });

    // Create the third Chart.js chart (donut chart)
    const ctx3 = document.getElementById("chart3").getContext("2d");
    const chart3 = new Chart(ctx3, {
        type: "doughnut",
        data: {
            labels: labels3,
            datasets: [
                {
                    data: data3,
                    backgroundColor: colors3,
                },
            ],
        },
    });
});
