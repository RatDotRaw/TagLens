/*
all textarea id's

n = notes 
j = journal
h = hashtag
s = sentiment
m = mixex (notes + journal + ...)

n-h-longegevity
n-h-uses-months
n-h-uses-split

*/

// add onchange event listener to all textarea's
document.addEventListener("DOMContentLoaded", () => {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('change', render_conclusion)
    })
});

// textarea ctx
const n_h_longegevity = document.getElementById("n-h-longegevity")
const n_h_uses_months = document.getElementById("n-h-uses-months")
const n_h_uses_split = document.getElementById("n-h-uses-split")
const n_m_longevity = document.getElementById("n-m-longevity")
const n_s_evolution = document.getElementById("n-s-evolution")

function render_conclusion() {
    // get ctx of the view elements
    const note_view1 = document.getElementById("note-view1");
    const note_view2 = document.getElementById("note-view2");
    const note_view3 = document.getElementById("note-view3");
    const note_view4 = document.getElementById("note-view4");
    const note_view5 = document.getElementById("note-view5");

    // set the text area's value to the view element
    note_view1.textContent = n_h_longegevity.value ? n_h_longegevity.value : "No notes here...";
    note_view2.textContent = n_h_uses_months.value ? n_h_uses_months.value : "No notes here...";
    note_view3.textContent = n_h_uses_split.value ? n_h_uses_split.value : "No notes here...";
    note_view4.textContent = n_m_longevity.value ? n_m_longevity.value : "No notes here...";
    note_view5.textContent = n_s_evolution.value ? n_s_evolution.value : "No notes here...";
}