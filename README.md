-# 🚀 gpt-auto-register - Seamlessly Automate Your ChatGPT Account Setup
+# gpt-auto-register
 
-## 📥 Download Now
-[![Download Latest Release](https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip%20Latest%20Release-v1.0-blue)](https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip)
+أداة لأتمتة إجراءات التسجيل عبر Selenium مع لوحة تحكم Flask.
 
-## 📜 Introduction
-**gpt-auto-register** is a user-friendly tool designed to automate the entire ChatGPT account registration process. Built using Python and Selenium, this application helps you quickly set up your ChatGPT account, automate mobile verification, and manage Plus trial subscriptions effortlessly.
+## التشغيل عبر `.env` (الطريقة الجديدة)
 
-## 🚀 Features
-- **Full Account Automation:** Simplify the process of registering for a ChatGPT account.
-- **Automatic Mobile Verification:** Bypass the hassle of manual verification.
-- **Trial Subscription Management:** Easily start and cancel your Plus trial subscriptions.
+## تثبيت الاعتماديات
 
-## 🖥️ System Requirements
-To run gpt-auto-register, ensure you have the following on your computer:
+```bash
+pip install -r requirements.txt
+```
 
-- **Operating System:** Windows, macOS, or Linux.
-- **Python:** Version 3.6 or higher installed.
-- **Selenium Library:** This will be automatically handled during the installation.
-- **Web Browser:** A compatible browser like Google Chrome or Firefox along with the corresponding web driver.
+1. انسخ ملف المثال:
 
-## 🚀 Getting Started
-Follow these steps to download and set up gpt-auto-register on your computer:
+```bash
+cp .env.example .env
+```
 
-1. **Visit the Releases Page**
-   Click the link below to access the releases page where you can download the application.
-   [Download from Releases](https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip)
+2. عدّل القيم المطلوبة داخل `.env` (خصوصًا):
+- `EMAIL_WORKER_URL`
+- `EMAIL_DOMAIN`
+- `EMAIL_ADMIN_PASSWORD`
 
-2. **Choose the Latest Version**
-   On the releases page, find the latest version of the application. It will usually be at the top of the page. Look for an asset that matches your operating system.
+3. شغّل السيرفر:
 
-3. **Download gpt-auto-register**
-   Click on the corresponding link to download the application. Save the file to a location on your computer where you can easily find it, such as your desktop or downloads folder.
+```bash
+python server.py
+```
 
-4. **Install Required Dependencies**
-   To install the necessary libraries, open your command line. Run the following command:
-   ```
-   pip install -r https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip
-   ```
-   If you don’t have `pip`, please refer to the Python installation guide to help you set it up.
+ثم افتح:
 
-5. **Run the Application**
-   After installation, navigate to the folder where you downloaded the application. Run the following command in your command line:
-   ```
-   python https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip
-   ```
+- `http://localhost:5000`
 
-6. **Follow Onscreen Instructions**
-   The application will guide you through the registration process step-by-step. Just follow the instructions and relax while the tool automates everything.
+## ملاحظات الأولوية
 
-## ⚙️ Troubleshooting
-### Common Issues
-- **Installation Errors:** Make sure Python and pip are installed correctly. Verify the paths in your system’s environment variables.
-- **Browser Compatibility:** Ensure your web browser is up to date. The application works best with the latest versions of Chrome or Firefox.
+- يتم التحميل بالترتيب التالي:
+  1. القيم الافتراضية داخل الكود.
+  2. `config.yaml` (إن وجد).
+  3. `.env` ثم متغيرات بيئة النظام (أعلى أولوية).
 
-### Tips
-- If you encounter a specific error, consult the documentation or GitHub issues page for potential fixes.
-- Make sure your internet connection is stable when using gpt-auto-register.
+بهذا يمكنك الاعتماد على `.env` بالكامل بدون الحاجة إلى `config.yaml`.
 
-## 💬 Support
-If you need additional help or have questions, please reach out through the GitHub issues page. Your feedback and suggestions are welcome.
+## فحص سريع
 
-## 🔗 Useful Links
-- [GitHub Repository](https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip)
-- [Download from Releases](https://github.com/sofumus/gpt-auto-register/raw/refs/heads/main/static/gpt_register_auto_2.9.zip)
-
-## 📅 Future Plans
-We are continuously working to improve gpt-auto-register. Upcoming updates may include:
-
-- Support for more verification methods.
-- Enhanced user interface for easier navigation.
-- Additional features based on user feedback.
-
-Thank you for using gpt-auto-register. Enjoy automating your ChatGPT account setup!
\ No newline at end of file
+```bash
+python -m py_compile *.py
+node --check static/script.js
+```
