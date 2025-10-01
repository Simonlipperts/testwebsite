//////////////////////////////////////////////
// Password check on sign up page
function checkPassword(){
    const pwd = document.getElementById('password').value;
    const repeat = document.getElementById('repeat_password').value;
    const btn = document.getElementById('submit-btn');
    const msg = document.getElementById('password-message');

    if (pwd === '' && repeat == '') {
        msg.textContent = '';
        //msg.className = 'success';
        btn.disabled = false;
    } else if (pwd === repeat && pwd !== '') {
        msg.textContent = '✓ Match';
        msg.className = 'success';
        btn.disabled = false;
    } else {
        msg.textContent = '✗ No match';
        msg.className = 'error';
        btn.disabled = true;
    }
}

// header logo knop
function logoClick() {
    console.log('Logo aangklikt!')
    window.location.href = '/home'
}

// already have an account knop
function alreadyAccClick() {
    console.log('Already acc knop aangelkikt!')
    window.location.href = '/log_in'
}

// Start when page loads
document.addEventListener('DOMContentLoaded', function() {

    const pwd = document.getElementById('password');
    const repeat = document.getElementById('repeat_password');
    if (pwd && repeat) {
        pwd.addEventListener('input', checkPassword);
        repeat.addEventListener('input', checkPassword);
        checkPassword();
    }

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
////////////////////////////////////////////////////
