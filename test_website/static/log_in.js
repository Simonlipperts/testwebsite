// Show error if login failed
// voor de login zou je niet checken of dat de first name en de last name of het password gelijk aan elkaar zijn
// en enkel bij het opnieuw laden van de pagina zou het moeten verschijnen

// header logo knop
function logoClick() {
    console.log('Logo aangklikt!')
    window.location.href = '/home'
}

// already have an account knop
function alreadyAccClick() {
    console.log('Already acc knop aangelkikt!')
    window.location.href = '/sign_up'
}

// Start when page loads
document.addEventListener('DOMContentLoaded', function() {
    const headerLogo = document.getElementById('header_logo');
        if (headerLogo) {
            headerLogo.addEventListener('click', logoClick);
        } else {
            console.warn('Header logo element niet gevonden');
        }

    const alreadyAcc = document.getElementById('already_acc');
    if (alreadyAcc) {
        alreadyAcc.addEventListener('click', alreadyAccClick)
    } else {
        console.warn('Already account knop niet gevonden')
    }
});


function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) 
           || window.innerWidth <= 768;
}

if (isMobileDevice()) {
    document.body.innerHTML = '<h1>Sorry, deze website is niet toegankelijk op mobiele apparaten</h1>';
}