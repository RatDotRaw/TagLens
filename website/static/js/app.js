console.log("app.js loaded");

document.addEventListener("DOMContentLoaded", fetchdata);

async function fetchdata() {
    let files = [];
    let hashtags = [];
    let pages = [];

    try {
        // fetch hashtags
        let response = await fetch("/data/hashtags");
        hashtags = await response.json();

        // convert string date to date object
        hashtags.forEach((hashtag) => {
            hashtag.first_appearance_date = str_to_date(
                hashtag.first_appearance_date
            );
            hashtag.last_appearance_date = str_to_date(
                hashtag.last_appearance_date
            );
        });

        console.log("hashtags:", hashtags);

        // fetch Pages
        response = await fetch("/data/pages");
        pages = await response.json();

        console.log("pages:", pages);

        // convert string date to date object
        pages.forEach((page) => {
            page.date = str_to_date(page.date);
        });

        // convert pages.journal_entry to boolean
        pages.forEach((page) => {
            if (page.journal_entry == 1 ) {
                page.journal_entry = true;
            } else {
                page.journal_entry = false;
            }
        })


        // fetch files
        response = await fetch("/data/files");
        files = await response.json();

        console.log("files:", files);
    } catch (e) {
        console.error("Error fetching the data:", e);
    }

    draw_first_last_date_hashtag(hashtags);
    draw_hash_usage(hashtags);
    draw_hash_note_journal(hashtags);

    draw_pages_dates(pages)
}

// convert a string date to a date object
function str_to_date(date_str) {
    // example format of str date: 2024-08-13
    return new Date(Date.parse(date_str));
}

////////////////
/// hashtags ///
////////////////

// draw a chart showing the first and last appearance of an hashtag per month.
function draw_first_last_date_hashtag(hashtags) {
    // Get the canvas context
    const ctx = document.getElementById("HashDateLine").getContext("2d");
    // Define the month labels
    const labels = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

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

    // Calculate difference between first and last appearance dates for each month
    let monthly_difference = [];
    for (let i = 0; i < 12; i++) {
        monthly_difference.push(
            first_appearance_date_counts[i] - last_appearance_date_counts[i]
        );
    }

    // Create the radar chart
    new Chart(ctx, {
        type: "line",
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
                {
                    label: "Difference",
                    data: monthly_difference, // Data for each month
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                    borderWidth: 1,
                    fill: true,
                },
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}

function draw_hash_usage(hashtags) {
    var ctx = document.getElementById("HashUse").getContext("2d");

    // get 20 most used hashtags
    hashtags.sort((a, b) => b.total_count - a.total_count);
    hashtags = hashtags.slice(0, 25);

    // create chart data
    const labels = hashtags.map((hashtag) => hashtag.name);
    var data = hashtags.map((hashtag) => hashtag.total_count);

    // draw chart
    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "# of Uses",
                    data: data,
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}

function draw_hash_note_journal(hashtags) {
    var ctx_page = document.getElementById("HashPage").getContext("2d");
    var ctx_journal = document.getElementById("HashJournal").getContext("2d");

    // check if a hashtag has any journal entries
    // this is done by checking the file's name associated with the page, a journal entry will have a date as a file name ex. 2021-05-01.md
    // yes this is lazy but it works.
    // TODO: refactor to use relationships instead of file names.
    const page_hashtag = [];
    const journal_hashtag = [];
    const dateRegex = /^\d{4}_\d{2}_\d{2}\.md$/;

    for (const hashtag of hashtags) {
        const isJournalHashtag = hashtag.files.some((file) =>
            dateRegex.test(file.filename)
        );

        if (isJournalHashtag) {
            if (!journal_hashtag.some((h) => h.name === hashtag.name)) {
                journal_hashtag.push(hashtag);
            }
        } else {
            if (!page_hashtag.some((h) => h.name === hashtag.name)) {
                page_hashtag.push(hashtag);
            }
        }
    }

    // slice the hashtags to only show the top 10 for each
    page_hashtag.sort((a, b) => b.total_count - a.total_count);
    journal_hashtag.sort((a, b) => b.total_count - a.total_count);
    page_hashtag.splice(25);
    journal_hashtag.splice(25);

    console.log(page_hashtag.length);
    console.log(journal_hashtag.length);
    

    const labels_page = Array.from(page_hashtag).map((hashtag) => hashtag.name);
    const labels_journal = Array.from(journal_hashtag).map(
        (hashtag) => hashtag.name
    );

    const page_data = Array.from(page_hashtag).map(
        (hashtag) => hashtag.total_count
    );
    const journal_data = Array.from(journal_hashtag).map(
        (hashtag) => hashtag.total_count
    );

    new Chart(ctx_page, {
        type: "bar",
        data: {
            labels: labels_page,
            datasets: [
                {
                    label: "# of Mentions in page entries",
                    data: page_data,
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
    new Chart(ctx_journal, {
        type: "bar",
        data: {
            labels: labels_journal,
            datasets: [
                {
                    label: "# of Mentions in journal entries",
                    data: journal_data,
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}

/////////////
/// Pages ///
/////////////
function draw_pages_dates(pages) {
    const ctx = document.getElementById("PageDates").getContext('2d');
    
    const labels = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

    // Sort pages by month
    let pages_dates = Array(12).fill(0); // Initialize counts for each month
    pages.forEach((pages) => {
        let month = pages.date.getMonth(); // 0-based index for months
        pages_dates[month]++;
    });

    // console.log(pages_dates); // Debugging output

    // Create the radar chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels, // Month labels
            datasets: [
                {
                    label: "Page creation date",
                    data: pages_dates, // Data for each month
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                }
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}