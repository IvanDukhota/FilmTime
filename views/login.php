<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="../styles/sign_up.css">
</head>
<body>
    <div class="container">
        <div class="top_img">
            <img src="../styles/images/popcorn.png" alt="Popcorn and drink">
        </div>

        <form action="#" method="POST" class="form_container" id="loginForm">
            <h1>Login</h1>
    
            <div class="field_wrapper">
                <input type="email" name="email" class="input_field" placeholder=" " id="email" required>
                <label for="email" class="label_text">Email</label>
            </div>
    
            <div class="field_wrapper">
                <input type="password" name="password" class="input_field" placeholder=" " id="password" required>
                <label for="password" class="label_text">Password</label>
            </div>
    
            <button type="submit" class="login_button">Login</button>

            <div class="social_buttons">
                <a href="#" class="social_button">
                    <img src="../styles/images/google.png" alt="Google"> Google
                </a>
                <a href="#" class="social_button">
                    <img src="../styles/images/facebook.png" alt="Facebook"> Facebook
                </a>
            </div>

            <p class="footer_text">Don't have an account? <a href="sign_up.php">Sign up</a></p>
        </form>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const emailField = document.getElementById('email');
            const passwordField = document.getElementById('password');
            const loginForm = document.getElementById('loginForm');
            const API_URL = 'http://127.0.0.1:8000/api/v1/login/'; 

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

            emailField.addEventListener('input', function() {
                const fieldWrapper = emailField.closest('.field_wrapper');
                clearErrors(fieldWrapper);
                const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
                if (emailField.value.length < 4 || emailField.value.length > 32) {
                    addError(emailField, 'Email address must be between 4 and 32 characters.');
                } else if (!emailPattern.test(emailField.value)) {
                    addError(emailField, 'Please enter a valid email address.');
                }
            });

            loginForm.addEventListener('submit', async function(event) {
                event.preventDefault();  

                const email = emailField.value;
                const password = passwordField.value;

                try {
                    const response = await fetch(API_URL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ email: email, password: password }),
                    });

                    const data = await response.json();

                    if (response.ok) {
                        alert('Authorization successful!');
                        window.location.href = 'welcome_page.html';  
                    } else {
                        alert(`Error: ${data.error || 'Incorrect credentials.'}`);
                    }
                } catch (error) {
                    console.error('Authorization error:', error);
                    alert('An error has occurred. Please try again later.');
                }
            });
        });
    </script>
</body>
</html>
