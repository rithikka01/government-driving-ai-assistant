# Government Driving Services AI Assistant 🚗

A web-based AI-style assistant that helps users find information about government driving licence services through a simple conversational interface.

## 🚀 Live Demo

👉 **[Try the Government Driving Services AI Assistant](https://government-driving-ai-assistant.vercel.app/)**

The application is deployed and accessible online using Vercel.

---

## 📌 Overview

The **Government Driving Services AI Assistant** is a web-based conversational assistant designed to help users quickly find information related to driving licence services.

The assistant understands common driving licence-related questions, identifies the user's intent, retrieves relevant information from a structured knowledge base, and provides a simple response through a chat-based interface.

It also provides a link to the official **Sarathi Parivahan Portal** for relevant services.

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
