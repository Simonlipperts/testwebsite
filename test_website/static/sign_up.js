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

// Start when page loads
document.addEventListener('DOMContentLoaded', function() {
    const pwd = document.getElementById('password');
    const repeat = document.getElementById('repeat_password');
    if (pwd && repeat) {
        pwd.addEventListener('input', checkPassword);
        repeat.addEventListener('input', checkPassword);
        checkPassword();
    }
});