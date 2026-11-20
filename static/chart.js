
const chartCanvas = document.getElementById("emailChart");

if (chartCanvas && typeof Chart !== "undefined") {

    const spamCount = Number(chartCanvas.dataset.spam);
    const hamCount = Number(chartCanvas.dataset.ham);

    new Chart(chartCanvas, {

        type: "doughnut",

        data: {
            labels: ["Spam Emails", "Legitimate Emails"],

            datasets: [{
                data: [spamCount, hamCount],

                backgroundColor: [
                    "#ef6262",
                    "#36b77b"
                ],

                borderWidth: 0,
                hoverOffset: 8
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });

} else {
    console.error("Chart.js or emailChart canvas not found.");
}
