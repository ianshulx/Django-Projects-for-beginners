# LeetCode Helper Chrome Extension

LeetCode Helper is a Chrome Extension designed to supercharge your LeetCode problem-solving experience with instant, AI-powered guidance. It seamlessly detects the current LeetCode problem, sends the details to a powerful backend, and returns step-by-step solutions—all without leaving your browser.

---

## 🧩 Features

- **Auto-Detects LeetCode Problems:** Instantly grabs the title and URL of the LeetCode problem you're viewing.
- **AI-Powered Guidance:** Sends problem details to a deployed Django REST API, which uses an LLM (Gemini or OpenAI) to generate step-by-step solutions.
- **Clean UI:** Displays AI responses in Markdown, rendered beautifully in the extension popup using [marked.min.js](https://marked.js.org/).
- **No Local Setup Needed:** Backend is fully managed and deployed on [Render.com](https://render.com).

---

## 🚀 Project Overview

LeetCode Helper streamlines your LeetCode workflow. With a single click, you get expert-level guidance directly from a large language model, tailored to the problem you're working on. No more context switching or copy-pasting—just solutions when you need them.

---

## 🛠️ How to Load as an Unpacked Extension

1. Download or clone this repository.
2. Open Google Chrome and go to `chrome://extensions/`.
3. Enable **Developer mode** (top right).
4. Click **Load unpacked** and select the `extension` folder inside the project.
5. The LeetCode Helper icon should appear in your extensions bar.

---

## ⚡ How to Use the Extension

1. Navigate to any [LeetCode](https://leetcode.com/) problem page.
2. Click the **LeetCode Helper** extension icon.
3. The extension will auto-fill the problem title and URL.
4. Click **Get Guidance**.
5. See step-by-step AI-generated guidance appear instantly in the popup!

> **Note:** No need to run any local servers—everything works out of the box.

---

## 🏗️ Architecture Overview

```
+---------------------+            +------------------------------+             +-----------------------------+
|  Chrome Extension   |  <------>  |  Django REST API (Render.com)|  <------->  | Large Language Model (LLM)  |
| (popup.html/js)     |            |   Endpoint: /api/solve/      |             | (Gemini, OpenAI, etc.)      |
+---------------------+            +------------------------------+             +-----------------------------+
       |                                                                                  |
       |------------------- User initiates a request -------------------------------------|
```

- **Frontend:** Presents popup UI, grabs problem info, and renders Markdown via marked.js.
- **Backend:** 
  The backend is built with Django and Django REST Framework, deployed on [Render.com](https://render.com) for seamless scalability and reliability. It exposes a single endpoint at `/api/solve/` and handles communication with the LLM.
- **LLM:** Generates step-by-step guidance tailored to the problem context.

---

### Key Backend Features

- **Integration with LLMs:** Utilizes APIs from LLM providers (e.g., Gemini, OpenAI) to generate detailed solutions and explanations.
- **Markdown Output:** Formats responses in Markdown for easy rendering on the frontend.
- **Error Handling:** Returns user-friendly error messages and backend status codes if the AI cannot generate guidance.
- **Scalability:** Hosted on Render.com for auto-scaling and high availability.
- **Security:** Basic request validation and sanitization are performed to ensure safe API usage.
- **Production Ready:** Includes Procfile and render.yaml for cloud deployment, and `.gitignore` for environment management.
- **Extensible:** Modular structure for easy addition of endpoints or support for other coding platforms.

> The backend is fully managed—no user setup required. All requests are handled securely and efficiently in the cloud.

---
## 📂 Folder Structure

```
Leetcode-Helper/
├── extension/                  # Chrome Extension source code
│   ├── icon.png
│   ├── manifest.json
│   ├── marked.min.js
│   ├── popup.css
│   ├── popup.html
│   └── popup.js
├── leetcode backend/
│   ├── api/                    
│   ├── backend/                
│   ├── .gitignore
│   ├── Procfile
│   ├── db.sqlite3
│   ├── manage.py
│   ├── render.yaml
│   └── requirements.txt
├── screenshots/                
```

---

## 🚧 Future Improvements & Contribution Guidelines

### Future Plans
- Support for more coding platforms (HackerRank, Codeforces, etc.)
- Chrome Web Store publication
- Enhanced error handling and retry logic
- User authentication and saved guidance history

### Contributing
Contributions are welcome! Please open an issue or submit a pull request with a clear description of your changes.

---

## 👥 Contributors

- [jydv402 (Jayadev B S)](https://github.com/jydv402)
- [SHIBINSHA02 (Shibinsha)](https://github.com/SHIBINSHA02)

---
