const header = document.querySelector("header");

if (header) {
    console.log("Header found:", header); // Logs the <header> element
    header.style.backgroundColor = "lightblue"; // Changes the background color of the header
    document.write('dada')
} else {
    console.log("No <header> element found in the DOM.");
}
