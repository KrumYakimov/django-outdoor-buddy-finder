class EmailTemplates:
    SUBJECT_WELCOME_EMAIL = "Welcome to Outdoor Buddy Finder!"
    SUBJECT_REST_PASSWORD_EMAIL = "Password Reset Request for Outdoor Buddy Finder"

    PLAIN_TEXT_CONTENT_WELCOME = """
    Hi {email},
    Welcome to Outdoor Buddy Finder!
    We're thrilled to have you on board. To help you connect with your next adventure partner, 
    please take a moment to complete your profile:
    https://ourplatform.com/account-setup
    If you have any questions, feel free to reach out to our support team 
    at https://ourplatform.com/support.
    Thank you for joining us!
    The Outdoor Buddy Finder Team
    """

    PLAIN_TEXT_CONTENT_REST_PASSWORD_EMAIL = """
    Password Reset Request
    We received a request to reset your password. Click the link below to reset it:
    https://ourplatform.com/reset-password
    """

    HTML_TEXT_CONTENT_WELCOME = """
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h3 style="color: #4CAF50;">Hi {email}, welcome to Outdoor Buddy Finder!</h3>
                <p>We're thrilled to have you on board.</p>
                <p>To help you connect with your next adventure partner, please take a moment to complete your profile:</p>
                <p>
                    <a 
                    href="https://ourplatform.com/account-setup" 
                    style="color: #4CAF50; text-decoration: none; font-weight: bold;">Fill in Your Profile Now
                    </a>
                </p>
                <p>
                    If you have any questions or need assistance, feel free to <a href="https://ourplatform.com/support" 
                    style="color: #4CAF50; text-decoration: none;">contact us</a>.
                </p>
                <p>Thank you for joining us!</p>
                <p style="font-size: 0.9em; color: #666;">- The Outdoor Buddy Finder Team</p>
            </body>
        </html>
        """

    HTML_TEXT_CONTENT_REST_PASSWORD_EMAIL = """
    <html lang="en">
        <body>
            <h2>Password Reset Request</h2>
            <p>We received a request to reset your password. Click the link below to reset it:</p>
            <a href=" https://ourplatform.com/reset-password">Reset Password</a>
        </body>
    </html>
    """