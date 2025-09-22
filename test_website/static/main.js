// clock on home page
function displayTime(){
    var d = new Date();
    var hour = d.getHours();
    var min = d.getMinutes();
    var sec = d.getSeconds();
    var ms = d.getMilliseconds();
    var firstDigit = Math.floor(ms/100);

    document.getElementById("clock").innerHTML = hour + ":" + min + ":" + sec + ":" + firstDigit;
}
setInterval(displayTime, 100)
// met document. scan je de hele html pagina
// met .innerHTML pas je de inhoud van een tag aan