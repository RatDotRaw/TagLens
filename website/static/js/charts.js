console.log("app.js loaded");

document.addEventListener("DOMContentLoaded", fetchdata);

// Define the month labels
const labels_months = [
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
            if (page.journal_entry == 1) {
                page.journal_entry = true;
            } else {
                page.journal_entry = false;
            }
        });

        // fetch files
        response = await fetch("/data/files");
        files = await response.json();

        console.log("files:", files);
    } catch (e) {
        console.error("Error fetching the data:", e);
    }

    show_basic_hashtags_stats(hashtags);
    draw_hashtag_longegevity(hashtags);
    draw_hash_usage(hashtags);
    draw_hash_note_journal(hashtags);

    show_basic_page_stats(pages);
    draw_pages_dates(pages);
    draw_page_sentiment(pages);
    // draw_page_common_words(pages);

    draw_longevity_difference(hashtags, pages)
    sentiment_evolution(pages);
}

// convert a string date to a date object
function str_to_date(date_str) {
    // example format of str date: 2024-08-13
    return new Date(Date.parse(date_str));
}

function format_date(date) {
    let year = date.getFullYear();
    let month = String(date.getMonth() + 1).padStart(2, "0");
    let day = String(date.getDate()).padStart(2, "0");

    return `${day}-${month}-${year}`;
}

////////////////
/// hashtags ///
////////////////

function show_basic_hashtags_stats(hashtags) {
    let ctx_hashtag_count = document.getElementById("hashtag-count");
    let ctx_first_hashtag_date = document.getElementById("first-hashtag-date");
    let ctx_last_hashtag_date = document.getElementById("last-hashtag-date");

    // get first/last appearance date
    let first_date = null;
    let last_date = null;

    hashtags.forEach((hashtag) => {
        let first_appearance_date = hashtag.first_appearance_date;
        let last_appearance_date = hashtag.last_appearance_date;

        if (
            first_appearance_date &&
            !isNaN(first_appearance_date.getTime()) &&
            (!first_date || first_appearance_date < first_date)
        ) {
            first_date = first_appearance_date;
            // console.log("new first date: ", first_date);
        }
        if (
            last_appearance_date &&
            !isNaN(last_appearance_date.getTime()) &&
            (!last_date || last_appearance_date > last_date)
        ) {
            last_date = last_appearance_date;
            // console.log("new last date: ", last_date);
        }
    });

    // Update DOM elements
    ctx_hashtag_count.innerText = "total hashtags: " + hashtags.length;
    ctx_first_hashtag_date.innerText = "first appearance: " + format_date(first_date);
    ctx_last_hashtag_date.innerText = "last appearance: " + format_date(last_date);
}

// draw a chart showing the first and last appearance of an hashtag per month.
function draw_hashtag_longegevity(hashtags) {
    // Get the canvas context
    const ctx = document.getElementById("HashDateLine").getContext("2d");


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
            labels: labels_months, // Month labels
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
                    mode: "index",
                    intersect: false,
                },
            },
        },
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
                    mode: "index",
                    intersect: false,
                },
            },
        },
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

    // console.log(page_hashtag.length);
    // console.log(journal_hashtag.length);

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
                    label: "# of Mentions in note entries",
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
                    mode: "index",
                    intersect: false,
                },
            },
        },
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
                    mode: "index",
                    intersect: false,
                },
            },
        },
    });
}

/////////////
/// Pages ///
/////////////

function show_basic_page_stats(pages) {
    let ctx_pages_count = document.getElementById("page-count");
    let ctx_journal_to_page_ratio = document.getElementById(
        "journal-to-page-ratio"
    );
    let ctx_total_words = document.getElementById("total-words");

    let ctx_average_words = document.getElementById("average-words");
    let ctx_average_words_journal = document.getElementById(
        "average-words-journal"
    );
    let ctx_average_words_pages = document.getElementById("average-words-page");

    let ctx_average_tags = document.getElementById("average-tags");

    // count total words for dom
    let total_words = 0;
    pages.forEach((page) => {
        total_words += page.word_count;
    });

    // count total journal/page entris
    let journal_to_page_ratio =
        pages.filter((page) => page.journal_entry).length +
        "/" +
        pages.filter((page) => !page.journal_entry).length;

    // calculate average word per page for DOM
    let average_words = total_words / pages.length;

    // calculate average words for journal/page entries only
    let average_words_journal = 0;
    let average_words_pages = 0;
    pages.forEach((page) => {
        if (page.journal_entry) {
            average_words_journal += page.word_count;
        } else {
            average_words_pages += page.word_count;
        }
    });
    // divite total by pages marked as journal/page entry
    average_words_journal =
        average_words_journal /
        pages.filter((page) => page.journal_entry).length;
    average_words_pages =
        average_words_pages /
        pages.filter((page) => !page.journal_entry).length;

    // calculate average tag per page
    let average_tags_per_page =
        pages.reduce((a, b) => a + b.tag_count, 0) / pages.length;

    // Update DOM elements
    ctx_pages_count.innerText = "total pages: " + pages.length;
    ctx_journal_to_page_ratio.innerText =
        "└─ journal/page ratio: " + journal_to_page_ratio;

    ctx_total_words.innerText = "total words: " + total_words;
    ctx_average_words.innerText = "├─ average words per page: " + average_words;
    ctx_average_words_journal.innerText =
        "├─ average words per journal entry: " +
        average_words_journal.toFixed(2);
    ctx_average_words_pages.innerText =
        "└─ average words per non-journal entry: " +
        average_words_pages.toFixed(2);

    ctx_average_tags.innerText =
        "Average tags per page: " + average_tags_per_page.toFixed(2);
}

function draw_pages_dates(pages) {
    const ctx = document.getElementById("PageDates").getContext("2d");

    // Sort pages by month
    let total_dates = Array(12).fill(0); // Initialize counts for each month
    let journal_dates = Array(12).fill(0);
    let pages_dates = Array(12).fill(0); 
    pages.forEach((page) => {
        let month = page.date.getMonth(); // 0-based index for months
        total_dates[month]++;

        // add to journal dates if it is a journal entry
        if (page.journal_entry) {
            journal_dates[month]++;
        } else {
            pages_dates[month]++;
        }
    });

    // console.log(total_dates); // Debugging output
    // console.log(journal_dates); // Debugging output
    // console.log(pages_dates); // Debugging output

    // Create the radar chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels_months, // Month labels
            datasets: [
                {
                    label: "Journal entries",
                    data: journal_dates, // Data for each month
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                },
                {
                    label: "Pages entries",
                    data: pages_dates, // Data for each month
                    backgroundColor: "rgba(75, 192, 192, 0.2)",
                    borderColor: "rgba(75, 192, 192, 1)",
                },
                {
                    label: "total creation date",
                    data: total_dates, // Data for each month
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    mode: "index",
                    intersect: false,
                },
            },
        },
    });
}
 
function draw_page_sentiment(pages) {
    let ctx = document.getElementById("PageSentiment")

    // get all sentiment labels and count occurances per page
    let sentiment_labels = {};
    pages.forEach(page => {
        const sentiment = page.sentiment_tags
        if (!sentiment) return // skip empty ones
        sentiment.forEach(sentiment => {
            let label = sentiment.label;
            if (sentiment_labels[label]) {
                sentiment_labels[label]++;
            } else {
                sentiment_labels[label] = 1;
            }
        })
    })

    // split into smaller dictionaries
    sentiment_labels = Object.entries(sentiment_labels).flatMap(([key, count]) => ({ [key]: count }));
    // sort by descending
    sentiment_labels.sort((a, b) => b - a);

    // hide less frequent labels to reduce clutter
    // count total entries
    let total_value = sentiment_labels.reduce((sum, entry) => sum + Object.values(entry)[0], 0);
    // Combine entries with less than 10% of the total into "other"
    let threshold = total_value * 0.025;
    let combined_labels = [];
    let other_value = 0;

    sentiment_labels.forEach(entry => {
        let value = Object.values(entry)[0];
        if (value < threshold) {
            other_value += value;
        } else {
            combined_labels.push(entry);
        }
    });

    if (other_value > 0) {
        combined_labels.push({ "other": other_value });
    }

    // get labels and values for chart
    let labels = combined_labels.map(item => Object.keys(item)[0]);
    let values = combined_labels.map(item => Object.values(item)[0]);
    
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels, 
            datasets: [
                {
                    label: "Journal sentiment",
                    data: values,
                },
            ],
        },
        // options: {
        //     plugins: {
        //         tooltip: {
        //             mode: "index",
        //             intersect: false,
        //         },
        //     },
        // },
    });
}

function draw_page_common_words(pages) {
    // split all file names by spaces and count the occurrences of each word
    let word_counts = {};
    pages.forEach(page => {
        if (page.journal_entry) { 
            return; // Skip journal entries as they are not common words in page names.
        }
        let words = page.name.split(' ');
        
        words = words.map(word => word.replace(/\.md$/, '')) // remove .md extension
        // words = words.map(word => word.replace(/^%.*? /, '')) // remove % and the next 2 characters

        words = words.filter(word => word.length > 4); // Filter out short words
        words = words.map(word => word.toLowerCase()); // Convert to lower case

        // Count the occurrences of each word
        for (let i = 0; i < words.length; i++) {
            if (word_counts[words[i]]) {
                word_counts[words[i]]++;
            } else {
                word_counts[words[i]] = 1;
            }
        }
    })
    // sort the word counts by frequency
    console.log(word_counts)


    // get the top x words
    const top_words = Object.fromEntries(
        Object.entries(word_counts)
          .sort(([, a], [, b]) => b - a) // Sort by value descending
          .slice(0, 10) // Take the top words
      );
    console.log('top words:', top_words);   
    
    // const chart = new Chart(document.getElementById("PageWords").getContext("2d"), {
    //   type: "wordCloud",
    //   data: {
    //     labels: Object.keys(top_words),
    //     datasets: [
    //       {
    //         label: "",
    //         data: Object.values(top_words)
    //       }
    //     ]
    //   },
    //   options: {
    //     title: {
    //       display: false,
    //       text: "Chart.js Word Cloud"
    //     },
    //     plugins: {
    //       legend: {
    //         display: false
    //       }
    //     }
    //   }
    // });
}

/////////////
/// mixed ///
/////////////

function draw_longevity_difference(hashtags, pages) {
    const ctx = document.getElementById("mix_longevity")

    // Count hashtag usage by month
    let first_appearance_date = Array(12).fill(0); // Initialize counts for each month
    hashtags.forEach((hashtag) => {
        let month = hashtag.first_appearance_date.getMonth(); // 0-based index for months
        first_appearance_date[month]++;
    });
    let last_appearance_date = Array(12).fill(0);
    hashtags.forEach((hashtag) => {
        let month = hashtag.last_appearance_date.getMonth(); // 0-based index for months
        last_appearance_date[month]++;
    });

    // count new pages per month
    let total_dates = Array(12).fill(0);
    pages.forEach((page) => {
        let month = page.date.getMonth(); // 0-based index for months
        total_dates[month]++;
    });

    // remove hashtag counts per moth (hashtag - pages)
    for (let i = 0; i < 12; i++) {
        first_appearance_date[i] -= total_dates[i];
        last_appearance_date[i] -= total_dates[i];
    }

    let monthly_difference = [];
    for (let i = 0; i < 12; i++) {
        monthly_difference.push(
            first_appearance_date[i] - last_appearance_date[i]
        );
    }

    // draw chart
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels_months, // Month labels
            datasets: [
                {
                    label: "Hashtag First Appearance",
                    data: first_appearance_date, // Data for each month
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                },
                {
                    label: "Hashtag Last Appearance",
                    data: last_appearance_date, // Data for each month
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
                title: {
                    display: true,
                    text: 'Normalized hashtag count'
                },
                tooltip: {
                    mode: "index",
                    intersect: false,
                },
            },
        },
    });
}


