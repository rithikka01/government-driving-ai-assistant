/* ============================================================
   DRIVING SERVICES AI ASSISTANT
   COMPLETE JAVASCRIPT
   ============================================================ */


/* ============================================================
   ELEMENTS
   ============================================================ */

const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const clearChatButton = document.getElementById("clearChatButton");
const suggestedQuestions = document.getElementById("suggestedQuestions");


/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {

    setupButtons();

    setupInput();

    scrollToBottom();

});


/* ============================================================
   SETUP ALL BUTTONS
   ============================================================ */

function setupButtons() {

    /* -----------------------------------------
       SUGGESTION BUTTONS
       ----------------------------------------- */

    document.querySelectorAll(".suggestion-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            const message = button.getAttribute("data-message");

            if (message) {

                sendMessage(message);

            }

        });

    });


    /* -----------------------------------------
       QUICK ACTION BUTTONS
       ----------------------------------------- */

    document.querySelectorAll(".quick-btn").forEach(function (button) {

        button.addEventListener("click", function () {

            const message = button.getAttribute("data-message");

            if (message) {

                sendMessage(message);

            }

        });

    });


    /* -----------------------------------------
       SEND BUTTON
       ----------------------------------------- */

    if (sendButton) {

        sendButton.addEventListener("click", function () {

            sendMessage();

        });

    }


    /* -----------------------------------------
       CLEAR BUTTON
       ----------------------------------------- */

    if (clearChatButton) {

        clearChatButton.addEventListener("click", function () {

            clearChat();

        });

    }

}


/* ============================================================
   INPUT SETUP
   ============================================================ */

function setupInput() {

    if (!userInput) {
        return;
    }


    userInput.addEventListener("keydown", function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    });

}


/* ============================================================
   SEND MESSAGE
   ============================================================ */

async function sendMessage(message = null) {

    /* -----------------------------------------
       GET MESSAGE
       ----------------------------------------- */

    if (message === null) {

        message = userInput.value.trim();

    }


    /* -----------------------------------------
       STOP EMPTY MESSAGE
       ----------------------------------------- */

    if (!message) {

        return;

    }


    /* -----------------------------------------
       REMOVE WELCOME / SUGGESTIONS
       ----------------------------------------- */

    removeWelcomeSection();

    hideSuggestions();


    /* -----------------------------------------
       ADD USER MESSAGE
       ----------------------------------------- */

    addUserMessage(message);


    /* -----------------------------------------
       CLEAR INPUT
       ----------------------------------------- */

    userInput.value = "";


    /* -----------------------------------------
       SHOW TYPING
       ----------------------------------------- */

    const typingElement = addTypingIndicator();


    /* -----------------------------------------
       DISABLE SEND TEMPORARILY
       ----------------------------------------- */

    setSendState(true);


    try {

        /* -----------------------------------------
           CALL FLASK BACKEND
           ----------------------------------------- */

        const response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: message

            })

        });


        /* -----------------------------------------
           CHECK HTTP RESPONSE
           ----------------------------------------- */

        if (!response.ok) {

            throw new Error(
                "Server returned HTTP " + response.status
            );

        }


        /* -----------------------------------------
           READ JSON
           ----------------------------------------- */

        const data = await response.json();


        /* -----------------------------------------
           REMOVE TYPING
           ----------------------------------------- */

        removeTypingIndicator(typingElement);


        /* -----------------------------------------
           DISPLAY BOT RESPONSE
           ----------------------------------------- */

        addBotMessage(data);


    } catch (error) {

        console.error("Chat error:", error);


        removeTypingIndicator(typingElement);


        addBotMessage({

            answer:
                "Sorry, I couldn't connect to the assistant right now. Please make sure the Flask server is running.",

            intent:
                "error",

            confidence:
                0,

            source:
                "system"

        });

    }


    /* -----------------------------------------
       ENABLE SEND
       ----------------------------------------- */

    setSendState(false);

}


/* ============================================================
   ADD USER MESSAGE
   ============================================================ */

function addUserMessage(message) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message user-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content";

    content.textContent =
        message;


    const timestamp =
        document.createElement("span");

    timestamp.className =
        "timestamp";

    timestamp.textContent =
        getCurrentTime();


    messageElement.appendChild(content);

    messageElement.appendChild(timestamp);


    chatBox.appendChild(messageElement);


    scrollToBottom();

}


/* ============================================================
   ADD BOT MESSAGE
   ============================================================ */

function addBotMessage(data) {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message bot-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    /* -----------------------------------------
       GET ANSWER
       ----------------------------------------- */

    let answer =
        data.answer ||
        data.response ||
        data.message ||
        "I couldn't find an answer to that question.";


    /*
       Convert new lines into HTML safely
    */

    content.innerHTML =
        formatAnswer(answer);


    /* -----------------------------------------
       SARATHI PORTAL BUTTON
       ----------------------------------------- */

    const portalUrl =
        data.portal_url ||
        data.official_portal ||
        data.url;


    if (portalUrl) {

        const portalButton =
            document.createElement("a");

        portalButton.className =
            "official-portal-button";

        portalButton.href =
            portalUrl;

        portalButton.target =
            "_blank";

        portalButton.rel =
            "noopener noreferrer";

        portalButton.textContent =
            "🔗 Open Official Sarathi Portal";


        content.appendChild(
            portalButton
        );

    }


    /* -----------------------------------------
       TIMESTAMP
       ----------------------------------------- */

    const timestamp =
        document.createElement("span");

    timestamp.className =
        "timestamp";

    timestamp.textContent =
        getCurrentTime();


    messageElement.appendChild(content);

    messageElement.appendChild(timestamp);


    /* -----------------------------------------
       METADATA
       ----------------------------------------- */

    const intent =
        data.intent;

    const confidence =
        data.confidence;

    const source =
        data.source;


    if (
        intent !== undefined ||
        confidence !== undefined ||
        source !== undefined
    ) {

        const metadata =
            document.createElement("div");

        metadata.className =
            "message-metadata";


        let metadataText = "";


        if (intent !== undefined) {

            metadataText +=
                "Intent: " + intent;

        }


        if (confidence !== undefined) {

            if (metadataText) {

                metadataText +=
                    "  •  ";

            }


            let confidenceValue =
                Number(confidence);


            /*
               If backend sends 0.91,
               display 91%.
            */

            if (
                confidenceValue >= 0 &&
                confidenceValue <= 1
            ) {

                confidenceValue *= 100;

            }


            metadataText +=
                "Confidence: " +
                Math.round(confidenceValue) +
                "%";

        }


        if (source !== undefined) {

            if (metadataText) {

                metadataText +=
                    "  •  ";

            }


            metadataText +=
                "Source: " + source;

        }


        metadata.textContent =
            metadataText;


        messageElement.appendChild(
            metadata
        );

    }


    chatBox.appendChild(
        messageElement
    );


    scrollToBottom();

}


/* ============================================================
   FORMAT ANSWER
   ============================================================ */

function formatAnswer(text) {

    /*
       Escape HTML first for safety
    */

    const div =
        document.createElement("div");

    div.textContent =
        String(text);


    let safeText =
        div.innerHTML;


    /*
       Convert line breaks
    */

    safeText =
        safeText.replace(
            /\n/g,
            "<br>"
        );


    /*
       Convert simple bullet points
    */

    safeText =
        safeText.replace(
            /•/g,
            "•"
        );


    return safeText;

}


/* ============================================================
   TYPING INDICATOR
   ============================================================ */

function addTypingIndicator() {

    const messageElement =
        document.createElement("div");

    messageElement.className =
        "message bot-message";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const typing =
        document.createElement("div");

    typing.className =
        "typing";


    const dot1 =
        document.createElement("span");

    const dot2 =
        document.createElement("span");

    const dot3 =
        document.createElement("span");


    typing.appendChild(dot1);

    typing.appendChild(dot2);

    typing.appendChild(dot3);


    content.appendChild(
        typing
    );


    messageElement.appendChild(
        content
    );


    chatBox.appendChild(
        messageElement
    );


    scrollToBottom();


    return messageElement;

}


/* ============================================================
   REMOVE TYPING INDICATOR
   ============================================================ */

function removeTypingIndicator(element) {

    if (
        element &&
        element.parentNode
    ) {

        element.parentNode.removeChild(
            element
        );

    }

}


/* ============================================================
   REMOVE WELCOME
   ============================================================ */

function removeWelcomeSection() {

    const welcome =
        document.querySelector(
            ".welcome-section"
        );


    if (welcome) {

        welcome.remove();

    }

}


/* ============================================================
   HIDE SUGGESTIONS
   ============================================================ */

function hideSuggestions() {

    if (suggestedQuestions) {

        suggestedQuestions.style.display =
            "none";

    }

}


/* ============================================================
   CLEAR CHAT
   ============================================================ */

function clearChat() {

    chatBox.innerHTML = "";


    /* -----------------------------------------
       RECREATE WELCOME SECTION
       ----------------------------------------- */

    const welcome =
        document.createElement("div");

    welcome.className =
        "welcome-section";


    welcome.innerHTML = `

        <div class="welcome-icon">
            👋
        </div>

        <h2>
            Hello! How can I help you?
        </h2>

        <p>
            Ask me anything about driving licence services,
            applications, documents, renewal, fees and more.
        </p>

    `;


    chatBox.appendChild(
        welcome
    );


    /* -----------------------------------------
       RECREATE FIRST BOT MESSAGE
       ----------------------------------------- */

    const firstMessage =
        document.createElement("div");

    firstMessage.className =
        "message bot-message";


    firstMessage.innerHTML = `

        <div class="message-content">

            Hello! I'm your Government Driving Services AI Assistant.
            Ask me anything about driving licence services.

        </div>

        <span class="timestamp">
            Now
        </span>

    `;


    chatBox.appendChild(
        firstMessage
    );


    /* -----------------------------------------
       RECREATE SUGGESTIONS
       ----------------------------------------- */

    const suggestions =
        document.createElement("div");

    suggestions.className =
        "suggested-questions";

    suggestions.id =
        "suggestedQuestions";


    suggestions.innerHTML = `

        <button
            type="button"
            class="suggestion-btn"
            data-message="How do I apply for a driving license?">

            How do I apply for a driving license?

        </button>


        <button
            type="button"
            class="suggestion-btn"
            data-message="What documents do I need?">

            What documents do I need?

        </button>


        <button
            type="button"
            class="suggestion-btn"
            data-message="How do I get a learner license?">

            How do I get a learner license?

        </button>

    `;


    chatBox.appendChild(
        suggestions
    );


    /* -----------------------------------------
       RECONNECT SUGGESTION BUTTONS
       ----------------------------------------- */

    suggestions
        .querySelectorAll(".suggestion-btn")
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    const message =
                        button.getAttribute(
                            "data-message"
                        );


                    if (message) {

                        sendMessage(
                            message
                        );

                    }

                }
            );

        });


    userInput.value = "";


    userInput.focus();


    scrollToBottom();

}


/* ============================================================
   SEND BUTTON STATE
   ============================================================ */

function setSendState(isLoading) {

    if (!sendButton) {
        return;
    }


    if (isLoading) {

        sendButton.disabled =
            true;

        sendButton.textContent =
            "...";

        sendButton.style.opacity =
            "0.7";

    } else {

        sendButton.disabled =
            false;

        sendButton.textContent =
            "Send";

        sendButton.style.opacity =
            "1";

    }

}


/* ============================================================
   CURRENT TIME
   ============================================================ */

function getCurrentTime() {

    const now =
        new Date();


    return now.toLocaleTimeString(
        [],
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );

}


/* ============================================================
   SCROLL
   ============================================================ */

function scrollToBottom() {

    if (!chatBox) {
        return;
    }


    setTimeout(function () {

        chatBox.scrollTop =
            chatBox.scrollHeight;

    }, 50);

}