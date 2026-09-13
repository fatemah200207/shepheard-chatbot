
/* =========================================================
   ELEMENTS
========================================================= */

const chatBox = document.getElementById("chatBox");
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");

const typingContainer = document.getElementById("typingContainer");

const statusDot = document.getElementById("statusDot");
const statusLabel = document.getElementById("statusLabel");

const clearButton = document.getElementById("clearButton");


/* =========================================================
   STATE
========================================================= */

let isWaitingForResponse = false;


/* =========================================================
   TIME
========================================================= */

function getTimestamp() {
    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });
}


/* =========================================================
   SECURITY
   Prevent HTML entered by the user or returned by the
   chatbot from being interpreted as HTML.
========================================================= */

function escapeHTML(text) {
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* =========================================================
   MESSAGE FORMATTING
========================================================= */

function formatMessage(text) {

    const escaped = escapeHTML(text);

    return escaped.replace(/\n/g, "<br>");
}


/* =========================================================
   ADD MESSAGE
========================================================= */

function addMessage(text, role) {

    const row = document.createElement("div");

    row.className =
        role === "user"
            ? "message-row user-message"
            : "message-row bot-message";


    const avatar = document.createElement("div");

    avatar.className =
        role === "user"
            ? "avatar user-avatar"
            : "avatar bot-avatar";

    avatar.textContent =
        role === "user"
            ? "U"
            : "S";


    const content = document.createElement("div");

    content.className = "message-content";


    const bubble = document.createElement("div");

    bubble.className =
        role === "user"
            ? "message-bubble user-bubble"
            : "message-bubble bot-bubble";

    bubble.innerHTML = formatMessage(text);


    const time = document.createElement("div");

    time.className = "message-time";

    time.textContent = getTimestamp();


    content.appendChild(bubble);
    content.appendChild(time);

    row.appendChild(avatar);
    row.appendChild(content);

    chatBox.appendChild(row);

    scrollToBottom();
}


/* =========================================================
   SCROLL
========================================================= */

function scrollToBottom() {

    requestAnimationFrame(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    });

}


/* =========================================================
   STATUS
========================================================= */

function setStatus(state) {

    statusDot.className = "status-dot";


    if (state === "thinking") {

        statusDot.classList.add("thinking");

        statusLabel.textContent = "Processing";

        typingContainer.style.display = "flex";

    }


    else if (state === "error") {

        statusDot.classList.add("error");

        statusLabel.textContent = "Connection Error";

        typingContainer.style.display = "none";

    }


    else {

        statusLabel.textContent = "System Online";

        typingContainer.style.display = "none";

    }


    scrollToBottom();
}


/* =========================================================
   TEXTAREA AUTO RESIZE
========================================================= */

function autoResize() {

    questionInput.style.height = "auto";

    const height = Math.min(
        questionInput.scrollHeight,
        130
    );

    questionInput.style.height = `${height}px`;
}


/* =========================================================
   SEND QUESTION
========================================================= */

async function sendQuestion() {

    if (isWaitingForResponse) {
        return;
    }


    const question = questionInput.value.trim();


    if (!question) {
        return;
    }


    /* Show user's message */

    addMessage(question, "user");


    /* Clear input */

    questionInput.value = "";

    questionInput.style.height = "auto";


    /* Lock interface */

    isWaitingForResponse = true;

    sendButton.disabled = true;

    questionInput.disabled = true;


    setStatus("thinking");


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            /*
             * IMPORTANT:
             * FastAPI expects:
             *
             * {
             *     "message": "..."
             * }
             */

            body: JSON.stringify({
                message: question
            })

        });


        /* Check HTTP response */

        if (!response.ok) {

            let errorMessage =
                `Server error (${response.status}).`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage =
                        errorData.detail;
                }

            } catch (error) {
                /* Ignore JSON parsing error */
            }

            throw new Error(errorMessage);
        }


        const data = await response.json();


        /* Get chatbot answer */

        const answer =
            data.answer ||
            "No answer was received from the assistant.";


        setStatus("ready");


        addMessage(answer, "bot");

    }


    catch (error) {

        console.error(
            "Chat request failed:",
            error
        );


        setStatus("error");


        addMessage(
            "I couldn't connect to the project assistant. Please check that the backend is running and try again.",
            "bot"
        );

    }


    finally {

        isWaitingForResponse = false;

        sendButton.disabled = false;

        questionInput.disabled = false;

        questionInput.focus();

        setStatus("ready");

    }
}


/* =========================================================
   KEYBOARD HANDLING
========================================================= */

function handleKeyboard(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendQuestion();

    }

}


/* =========================================================
   CLEAR CHAT
========================================================= */

function clearChat() {

    if (isWaitingForResponse) {
        return;
    }


    chatBox.innerHTML = `
        <div class="session-divider">
            <span>START OF SESSION</span>
        </div>

        <div class="message-row bot-message">

            <div class="avatar bot-avatar">
                S
            </div>

            <div class="message-content">

                <div class="message-bubble bot-bubble">

                    <p>
                        Welcome to the Shepheard Hotel Annex
                        Project Assistant.
                    </p>

                    <p>
                        I can help you find and understand
                        information contained in the project
                        documents.
                    </p>

                </div>

                <div class="message-time">
                    ${getTimestamp()}
                </div>

            </div>

        </div>
    `;


    setStatus("ready");

    questionInput.focus();

    scrollToBottom();
}


/* =========================================================
   EVENT LISTENERS
========================================================= */

sendButton.addEventListener(
    "click",
    sendQuestion
);


clearButton.addEventListener(
    "click",
    clearChat
);


questionInput.addEventListener(
    "keydown",
    handleKeyboard
);


questionInput.addEventListener(
    "input",
    autoResize
);


/* =========================================================
   INITIALIZATION
========================================================= */

setStatus("ready");

questionInput.focus();
