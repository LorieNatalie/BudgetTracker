# Project Title: Secure Local Budget Tracker Application

Description:

This project is a comprehensive desktop-based budget management tool designed to empower users to track their finances securely on their local machines. Recognizing the importance of data privacy and integrity, especially when dealing with sensitive financial information, I incorporated multiple security measures to safeguard user data against potential threats.
Key Security Features & Real-World Problem Solving:

    Data Confidentiality:
    Implemented database encryption to protect sensitive financial data stored locally, preventing unauthorized access even if physical device security is compromised.

    Secure Authentication:
    Utilized bcrypt hashing for passwords to ensure that user credentials are stored securely, reducing the risk of credential theft. Added account lockout features after multiple failed login attempts to prevent brute-force attacks.

    File System Security:
    Restricted access permissions to application files and data directories, aligning with best practices for securing local data.

    Input Validation & Data Integrity:
    Enforced thorough input validation and sanitization to prevent injection attacks and data corruption, ensuring the reliability of stored information.

    Session Management:
    Integrated inactivity timeouts and lock screens, safeguarding user data if the application is left unattended or accessed by unauthorized individuals.

    Code Security:
    Employed code obfuscation techniques to hinder reverse-engineering efforts, protecting proprietary logic and security mechanisms.

Impact:

These security measures address real-world challenges faced by desktop applications handling sensitive information, ensuring data privacy, preventing unauthorized access, and maintaining user trust. The project demonstrates my ability to develop not only functional but also secure software solutions, aligning with industry standards for data protection.