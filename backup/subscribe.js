// https://www.geeksforgeeks.org/search-bar-using-html-css-and-javascript/
// But also another more complete
// https://www.codewithfaraz.com/content/193/create-a-search-filter-with-html-css-and-javascript-source-code

var checkboxTrue = "CheckBox is checked";
var checkboxFalse = "Please click on the checkbox";

function subscribe() { 

    if(document.getElementById('checkBox').checked) {
        alert(checkboxTrue);
    } else {
        alert(checkboxFalse);
    }
}