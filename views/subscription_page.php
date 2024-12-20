<!DOCTYPE html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subscription Plans</title>
    <link rel="stylesheet" href="../styles/subscription_page.css">
</head>
<body>
    <?php
        include('header_logged_in.html');
    ?>

    <div class="plans-container">
        <div class="plan-card" data-name="Flexible Plan" data-price="€500/month" data-terms="Monthly, no long-term commitment. Cancel anytime without penalties. Higher cost compared to long-term plans.">
            <div class="plan-description">
                <h3>Flexible Plan</h3>
                <p>₴<strong>500</strong>/month</p>
                <ul>
                    <li>Monthly, no long-term commitment.</li>
                    <li>Cancel anytime without penalties.</li>
                    <li>Higher cost compared to long-term plans.</li>
                </ul>
            </div>
            <button class="choose-button">Choose Plan</button>
        </div>
        <div class="plan-card" data-name="Annual Plan" data-price="€400/month" data-terms="Fixed monthly payment over 12 months. A 12-month commitment with evenly distributed monthly payments. Cheaper than the flexible plan.">
            <div class="plan-description">
                <h3>Annual Plan</h3>
                <p>₴<strong>400</strong>/month</p>
                <ul>
                    <li>Fixed monthly payment over 12 months.</li>
                    <li>A 12-month commitment with evenly distributed monthly payments.</li>
                    <li>Cheaper than the flexible plan.</li>
                </ul>
            </div>
            <button class="choose-button">Choose Plan</button>
        </div>
        <div class="plan-card" data-name="Pay Ahead for a Year" data-price="€4200/year" data-terms="Only €350 per month. One-time payment for the entire year. The cheapest option with additional savings.">
            <div class="plan-description">
                <h3>Pay Ahead for a Year</h3>
                <p>₴<strong>4200</strong>/year</p>
                <ul>
                    <li>Only <strong>₴350</strong> per month.</li>
                    <li>One-time payment for the entire year.</li>
                    <li>The cheapest option with additional savings.</li>
                </ul>
            </div>
            <button class="choose-button">Choose Plan</button>
        </div>
    </div>

    <div id="overlay">
        <div class="modal">
            <div class="plan-description" id="modal-content"></div>
            <button class="confirm-button">Proceed to Payment</button>
            <button class="cancel-button">Cancel</button>
        </div>
    </div>

    <?php
        include('footer.html');
    ?>
</body>
    <script>
        const buttons = document.querySelectorAll('.choose-button');
        const overlay = document.getElementById('overlay');
        const modalContent = document.getElementById('modal-content');
        const confirmButton = document.querySelector('.confirm-button');
        const cancelButton = document.querySelector('.cancel-button');

        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                const card = e.target.closest('.plan-card');
                const description = card.querySelector('.plan-description').innerHTML;

                modalContent.innerHTML = description;
                overlay.style.display = 'flex';
            });
        });

        cancelButton.addEventListener('click', () => {
            overlay.style.display = 'none';
        });

        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.style.display = 'none';
            }
        });
    </script>
</html>