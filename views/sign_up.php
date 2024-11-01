<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <link rel="stylesheet" href="../styles/sign_up.css">
</head>
<body>
    <div class="container">
        <div class="top_img">
            <img src="../styles/images/popcorn.png" alt="Popcorn and drink">
        </div>

        <form action="#" method="POST" class="form_container" id="signUpForm">
            <h1>Sign up</h1>
            
            <div class="field_wrapper">
                <input type="text" name="nickname" class="input_field" placeholder=" " id="nickname" required>
                <label for="nickname" class="label_text">Nickname</label>
            </div>
    
            <div class="field_wrapper">
                <input type="email" name="email" class="input_field" placeholder=" " id="email" required>
                <label for="email" class="label_text">Email</label>
            </div>
    
            <div class="field_wrapper">
                <input type="password" name="password" class="input_field" placeholder=" " id="password" required>
                <label for="password" class="label_text">Password</label>
            </div>

            <div class="field_wrapper">
                <input type="password" name="repeat_password" class="input_field" placeholder=" " id="repeat_password" required>
                <label for="repeat_password" class="label_text">Repeat password</label>
            </div>
    
            <button type="submit" class="sign_up_button">Sign up</button>

            <p class="footer_text">Already have an account? <a href="login.php">Login here</a></p>
        </form>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const signUpForm = document.getElementById('signUpForm');
            const nicknameField = document.getElementById('nickname');
            const emailField = document.getElementById('email');
            const passwordField = document.getElementById('password');
            const repeatPasswordField = document.getElementById('repeat_password');
            const API_URL = 'http://127.0.0.1:8000/api/v1/register/';

            function clearErrors(fieldWrapper) {
                const errorMessages = fieldWrapper.querySelectorAll('.error_message');
                errorMessages.forEach(error => error.remove());
            }

            function addError(inputField, message) {
                const errorItem = document.createElement('p');
                errorItem.classList.add('error_message');
                errorItem.innerText = message;
                inputField.parentNode.appendChild(errorItem);
            }

            signUpForm.addEventListener('submit', async function(event) {
                event.preventDefault();
                let isValid = true;

                clearErrors(nicknameField.closest('.field_wrapper'));
                if (nicknameField.value.length < 4 || nicknameField.value.length > 32) {
                    addError(nicknameField, 'Nickname must be between 4 and 32 characters.');
                    isValid = false;
                }

                clearErrors(emailField.closest('.field_wrapper'));
                const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (emailField.value.length < 4 || emailField.value.length > 32) {
                    addError(emailField, 'Email address must be between 4 and 32 characters.');
                    isValid = false;
                } else if (!emailPattern.test(emailField.value)) {
                    addError(emailField, 'Please enter a valid email address.');
                    isValid = false;
                }

                clearErrors(passwordField.closest('.field_wrapper'));
                if (passwordField.value.length < 8 || passwordField.value.length > 32) {
                    addError(passwordField, 'Password must be between 8 and 32 characters.');
                    isValid = false;
                }


                clearErrors(repeatPasswordField.closest('.field_wrapper'));
                if (repeatPasswordField.value !== passwordField.value) {
                    addError(repeatPasswordField, 'Passwords do not match.');
                    isValid = false;
                }

                if (!isValid) return;

                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            username: nicknameField.value,
                            email: emailField.value,
                            password: passwordField.value,
                        }),
                    });
                    const data = await response.json();

                    if (response.ok) {
                        alert('Registration successful!');
                        signUpForm.reset();
                    } else if (data.error_code === 1001) {
                        addError(emailField, data.error_message);
                    } else {
                        alert(`Unknown error: ${data.error_message || ''}`);
                    }
                } catch (error) {
                    alert('Error during registration process.');
                }
            });
        });
    </script>
</body>
</html>
