console.log("app.js loaded");

document.addEventListener("DOMContentLoaded", fetchdata);

const ctx = document.getElementById("myChart").getContext("2d");

async function fetchdata() {
    let hashtags = [];
    try {
        const response = await fetch("/data/hashtags");
        hashtags = await response.json();

        // convert string date to date object
        hashtags.forEach((hashtag) => {
            hashtag.first_appearance_date = str_to_date(hashtag.first_appearance_date);
            hashtag.last_appearance_date = str_to_date(hashtag.last_appearance_date);
        });

    } catch (e) {
        console.error("Error fetching the data:", e);
    }
    draw_radar_chart(ctx, hashtags)
}

function draw_radar_chart(ctx, hashtags) {
    // Define the month labels
    const labels = ["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"];

    // Count hashtag usage by month
    let first_appearance_date_counts = Array(12).fill(0); // Initialize counts for each month
    hashtags.forEach((hashtag) => {
        let month = hashtag.first_appearance_date.getMonth(); // 0-based index for months
        first_appearance_date_counts[month]++; 
    });
    let last_appearance_date_counts = Array(12).fill(0);
    hashtags.forEach((hashtag) => {
        let month = hashtag.last_appearance_date.getMonth(); // 0-based index for months
        last_appearance_date_counts[month]++; 
    });
    
    console.log("First appearance counts:", first_appearance_date_counts);
    console.log("Last appearance counts:", last_appearance_date_counts);

    // Create the radar chart
    new Chart(ctx, {
        type: "radar",
        data: {
            labels: labels, // Month labels
            datasets: [
                {
                    label: "Hashtag First Appearance",
                    data: first_appearance_date_counts, // Data for each month
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
                {
                    label: "Hashtag Last Appearance",
                    data: last_appearance_date_counts, // Data for each month
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1,
                },
            ],
        },
    });
}

// {
//     label: "Hashtag last appearance",
//     data: last_appearance_date_counts, // Data for each month
//     backgroundColor: "rgba(255, 99, 132, 0.2)",
//     borderColor: "rgba(255, 99, 132, 1)",
//     borderWidth: 1,
// },


function str_to_date(date_str) {
    // example format of str date: 2024-08-13
    return new Date(Date.parse(date_str));
}
