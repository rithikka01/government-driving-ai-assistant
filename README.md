# Government Driving Services AI Assistant 🚗

A web-based conversational AI-style assistant that helps users find information about government driving licence services through a simple and interactive chat interface.

## 🚀 Live Demo

👉 **[Try the Government Driving Services AI Assistant](https://government-driving-ai-assistant.vercel.app/)**

The application is deployed and accessible online using Vercel.

---

## 📌 Overview

The **Government Driving Services AI Assistant** is a web-based conversational assistant designed to help users quickly find information related to driving licence services.

The assistant processes common driving licence-related questions, identifies the user's intent, retrieves relevant information from a structured knowledge base, and provides appropriate responses through a chat-based interface.

It also provides users with access to the official **Sarathi Parivahan Portal** for relevant driving licence services.

---

## ✨ Features

- 🚗 Driving licence application guidance
- 🪪 Learner licence information
- 📝 Driving test information
- 🔄 Licence renewal guidance
- 📄 Lost or duplicate licence guidance
- 📑 Required documents information
- 💰 Licence fee information
- 🔎 Application status information
- 📍 Address change information
- 🎂 Minimum age and eligibility information
- 🌍 International Driving Permit information
- 🧠 Natural-language intent detection
- 📚 Knowledge-base retrieval
- 📊 Intent and confidence information
- 🛡️ Fallback handling for unsupported questions
- 🔗 Official Sarathi Parivahan Portal link
- ⚡ Quick-action buttons
- 🧹 Chat history clearing
- 🌐 Live web deployment using Vercel

---

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **HTML5**
- **CSS3**
- **JavaScript**
- **JSON**
- **Natural-language intent matching**
- **Vercel**

---

## 🏗️ Project Architecture

The application follows a simple Flask-based architecture:

```text
User
  │
  ▼
Web Interface
  │
  ▼
JavaScript Chat Handler
  │
  ▼
Flask Backend
  │
  ├── Intent Detection
  │
  ├── Knowledge Base Retrieval
  │
  └── Response Generation
  │
  ▼
Chat Response


🧠 How It Works

1. The user enters a driving licence-related question through the web interface.
2. JavaScript sends the user's message to the Flask backend.
3. The backend processes the input and identifies the most relevant intent.
4. Relevant information is retrieved from the structured knowledge base.
5. The system generates and returns an appropriate response.
6. The response is displayed in the chat interface.

📊 Intent Testing and Evaluation

The project includes an intent accuracy testing notebook to evaluate the intent detection functionality.

Test Results
Metric	Result
Total Test Samples	55
Correct Predictions	50
Incorrect Predictions	5
Intent Detection Accuracy	90.91%

The testing notebook is available in:

intent_accuracy_testing.ipynb
🚀 Deployment

The application is deployed using Vercel.

🌐 Live Application

👉 https://government-driving-ai-assistant.vercel.app/

▶️ Running the Project Locally
1. Clone the Repository
git clone https://github.com/rithikka01/government-driving-ai-assistant.git
2. Navigate to the Project Directory
cd government-driving-ai-assistant
3. Install Dependencies
pip install -r requirements.txt
4. Run the Application
python app.py

Then open the application in your browser.

📚 Knowledge Base

The assistant uses structured JSON files to store:

Driving licence service intents
User question patterns
Relevant responses
Driving service information

This allows the application to provide responses based on the user's detected intent.

🛡️ Fallback Handling

If the user's question does not match a supported intent, the assistant provides a fallback response instead of returning an incorrect or unrelated answer.



👩‍💻 Author
Rithikka

⭐ If you found this project useful, feel free to star the repository!


### After pasting this into `README.md`

Run:

```bash
git add README.md
git commit -m "Update README with project details and testing results"
git push origin main

