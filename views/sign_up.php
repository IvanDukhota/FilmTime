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

                <div class="social_buttons">
                    <a href="#" class="social_button">
                        <img src="../styles/images/google.png" alt="Google"> Google
                    </a>
                    <a href="#" class="social_button">
                        <img src="../styles/images/facebook.png" alt="Facebook"> Facebook
                    </a>
                </div>

                <p class="footer_text">Already have an account? <a href="login.php">Login here</a></p>
            </form>
        </div>

        <script>
            document.addEventListener("DOMContentLoaded", function() {
                const nicknameField = document.getElementById('nickname');
                const emailField = document.getElementById('email');
                const passwordField = document.getElementById('password');
                const repeatPasswordField = document.getElementById('repeat_password');

                function clearErrors(fieldWrapper) {
                    const errorMessages = fieldWrapper.querySelectorAll('.error_message');
                    errorMessages.forEach(error => error.remove());
                }

                function addError(fieldWrapper, message) {
                    const errorItem = document.createElement('p');
                    errorItem.classList.add('error_message');
                    errorItem.innerText = message;
                    fieldWrapper.appendChild(errorItem);
                }

                nicknameField.addEventListener('input', function() {
                    const fieldWrapper = nicknameField.closest('.field_wrapper');
                    clearErrors(fieldWrapper);
                    if (nicknameField.value.length < 4 || nicknameField.value.length > 32) {
                        addError(fieldWrapper, 'Nickname must be between 4 and 32 characters.')
                    }
                });

                emailField.addEventListener('input', function() {
                    const fieldWrapper = emailField.closest('.field_wrapper');
                    clearErrors(fieldWrapper);
                    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                    if (emailField.value.length < 4 || emailField.value.length > 32) {
                        addError(fieldWrapper, 'Email address must be between 4 and 32 characters.')
                    }
                    else if (!emailPattern.test(emailField.value)) {
                        addError(fieldWrapper, 'Please enter a valid email address.')
                    }
                });

                passwordField.addEventListener('input', function() {
                    const fieldWrapper = passwordField.closest('.field_wrapper');
                    clearErrors(fieldWrapper);
                    if(passwordField.value.length < 8 || passwordField.value.length > 32) {
                        addError(fieldWrapper, 'Password must be between 8 and 32 characters.');
                    }
                });

                repeatPasswordField.addEventListener('input', function() {
                    const fieldWrapper = repeatPasswordField.closest('.field_wrapper');
                    clearErrors(fieldWrapper);
                    if (repeatPasswordField.value !== passwordField.value) {
                        addError(fieldWrapper, 'Passwords do not match.');
                    }
                });
            });
        </script>
    </body>
</html>