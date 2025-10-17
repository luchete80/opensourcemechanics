// https://www.geeksforgeeks.org/search-bar-using-html-css-and-javascript/
// But also another more complete
// https://www.codewithfaraz.com/content/193/create-a-search-filter-with-html-css-and-javascript-source-code

function search_entry() { 
    let input = document.getElementById('searchbar').value 
    input=input.toLowerCase(); 
    let x = document.getElementsByClassName('entry'); 
      
    for (i = 0; i < x.length; i++) {  
        if (!x[i].innerHTML.toLowerCase().includes(input)) { 
            x[i].style.display="none"; 
        } 
        else { 
            x[i].style.display="list-item";                  
        } 
    } 
} 

function search_by_string(input) { 
    //let input = '#FEM'
    // let input = document.getElementById('searchbar').value 
    // input=input.toLowerCase(); 
    let x = document.getElementsByClassName('entry'); 
      
    for (i = 0; i < x.length; i++) {  
        if (!x[i].innerHTML.includes(input)) { 
            x[i].style.display="none"; 
        } 
        else { 
            x[i].style.display="list-item";                  
        } 
    } 
    document.getElementById("demo").innerHTML = input;
} 

function search_HTML(){
  search_entry('#CUDA');
  
}
