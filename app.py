from flask import Flask, render_template, request, jsonify
import json
import os
import re
from difflib import SequenceMatcher


app = Flask(__name__)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# ============================================================
# LOAD JSON DATA
# ============================================================

def load_json(filename):

    path = os.path.join(DATA_DIR, filename)

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        print(f"ERROR: File not found: {path}")

        return {}

    except json.JSONDecodeError:

        print(f"ERROR: Invalid JSON: {path}")

        return {}


# Load intent data
intents_data = load_json(
    "intents.json"
)


# Load knowledge base
knowledge_data = load_json(
    "driving_knowledge.json"
)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if not text:

        return ""

    text = text.lower().strip()


    # Licence / license
    text = text.replace(
        "licence",
        "license"
    )

    text = text.replace(
        "licences",
        "licenses"
    )


    # Common abbreviations / variations
    replacements = {

        "dl":
            "driving license",

        "llr":
            "learner license",

        "idp":
            "international driving permit",

        "papers":
            "documents",

        "paper":
            "documents",

        "docs":
            "documents",

        "doc":
            "documents",

        "fee":
            "fees",

        "charge":
            "fees",

        "charges":
            "fees",

        "expired":
            "expiry",

        "renewal":
            "renew",

        "renewing":
            "renew",

        "replace":
            "replacement",

        "replacing":
            "replacement",

        "track":
            "tracking",

        "tracked":
            "tracking"
    }


    for old, new in replacements.items():

        text = re.sub(
            r"\b" + re.escape(old) + r"\b",
            new,
            text
        )


    # Remove punctuation
    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )


    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()


    return text


# ============================================================
# GENERIC WORDS
# ============================================================

GENERIC_WORDS = {

    "i",
    "my",
    "me",
    "mine",

    "you",
    "your",

    "the",
    "a",
    "an",

    "for",
    "to",
    "do",
    "does",
    "did",

    "how",
    "can",
    "could",
    "would",

    "what",
    "which",
    "where",
    "when",
    "why",

    "is",
    "are",
    "am",

    "of",
    "on",
    "in",
    "at",

    "with",

    "please",
    "tell",
    "want",
    "need",
    "get",

    "have",
    "has",
    "had",

    "be",

    "about",
    "there",
    "this",
    "that",

    "should",
    "from",
    "and"
}


# ============================================================
# IMPORTANT SERVICE WORDS
# ============================================================

SERVICE_WORDS = {

    "license",
    "driving",
    "learner",
    "test",
    "renew",
    "renewal",
    "expiry",
    "replacement",
    "lost",
    "documents",
    "fees",
    "cost",
    "application",
    "tracking",
    "status",
    "address",
    "international",
    "permit",
    "age",
    "eligibility"
}


# ============================================================
# INTENT → KNOWLEDGE TOPIC
# ============================================================

INTENT_TO_TOPIC = {

    "apply_license":
        "driving_licence_application",

    "learner_license":
        "learner_licence",

    "driving_test":
        "driving_test",

    "loss_license":
        "lost_licence",

    "renew_license":
        "licence_renewal",

    "documents":
        "required_documents",

    "fees":
        "licence_fees",

    "application_status":
        "application_status",

    "eligibility":
        "minimum_age",

    "address_change":
        "address_change",

    "international_driving":
        "international_driving_permit"
}


# ============================================================
# EXTRA INTENT SYNONYMS
# ============================================================

INTENT_SYNONYMS = {

    "learner_license": [

        "learner license",
        "learner",
        "llr",
        "learning license",
        "learners license",
        "learner licence",
        "apply learner license",
        "get learner license",
        "need learner license",
        "want learner license"
    ],


    "apply_license": [

        "apply driving license",
        "new driving license",
        "get driving license",
        "driving license application",
        "apply for license",
        "new license",
        "obtain driving license",
        "how to apply license",
        "how can i apply",
        "apply for driving license"
    ],


    "driving_test": [

        "driving test",
        "book driving test",
        "schedule driving test",
        "test appointment",
        "driving exam",
        "take driving test",
        "book test",
        "driving test appointment"
    ],


    "loss_license": [

        "lost license",
        "lost driving license",
        "lost dl",
        "replace lost license",
        "replacement license",
        "duplicate license",
        "duplicate driving license",
        "license replacement",
        "replace my license"
    ],


    "renew_license": [

        "renew license",
        "license renewal",
        "expiry license",
        "license expired",
        "renew expired license",
        "renew driving license",
        "license expiry",
        "my license is expired",
        "expired driving license"
    ],


    "documents": [

        "documents",
        "required documents",
        "documents needed",
        "documents required",
        "papers",
        "proof",
        "what papers",
        "what documents",
        "documents for license",
        "papers needed"
    ],


    "fees": [

        "fees",
        "license fee",
        "driving license fee",
        "cost",
        "price",
        "charges",
        "how much",
        "renewal fee",
        "license cost"
    ],


    "application_status": [

        "application status",
        "track application",
        "tracking application",
        "check status",
        "application tracking",
        "where is my application",
        "status of application",
        "track my license"
    ],


    "eligibility": [

        "minimum age",
        "driving age",
        "eligible age",
        "age requirement",
        "how old",
        "age to apply",
        "eligibility",
        "eligible for license"
    ],


    "address_change": [

        "change address",
        "update address",
        "address on license",
        "wrong address",
        "new address",
        "change my address",
        "update my address"
    ],


    "international_driving": [

        "international driving",
        "international driving permit",
        "international license",
        "drive abroad",
        "driving abroad",
        "driving in another country",
        "idp"
    ]
}


# ============================================================
# SIMILARITY
# ============================================================

def similarity(text1, text2):

    return SequenceMatcher(
        None,
        text1,
        text2
    ).ratio()


# ============================================================
# SCORE PHRASE
# ============================================================

def score_phrase(
    user_text,
    user_words,
    phrase
):

    phrase_text = normalize_text(
        phrase
    )


    if not phrase_text:

        return 0


    phrase_words = set(
        phrase_text.split()
    )


    meaningful_phrase_words = (
        phrase_words -
        GENERIC_WORDS
    )


    # Exact complete match
    if user_text == phrase_text:

        return 100


    # Exact phrase inside question
    if phrase_text in user_text:

        word_count = len(
            meaningful_phrase_words
        )


        if word_count >= 3:

            return 90


        if word_count == 2:

            return 85


        return 75


    # Word overlap
    common_words = (
        user_words &
        phrase_words
    )


    meaningful_common_words = (
        common_words -
        GENERIC_WORDS
    )


    if not meaningful_common_words:

        return 0


    if not meaningful_phrase_words:

        return 0


    overlap = len(
        meaningful_common_words
    )


    phrase_count = len(
        meaningful_phrase_words
    )


    coverage = (
        overlap /
        phrase_count
    )


    score = (
        overlap *
        18
    )


    # Coverage bonus
    if coverage >= 1:

        score += 35

    elif coverage >= 0.66:

        score += 25

    elif coverage >= 0.5:

        score += 15


    # Similarity bonus
    sim = similarity(
        user_text,
        phrase_text
    )


    if sim >= 0.85:

        score += 20

    elif sim >= 0.70:

        score += 10


    return min(
        score,
        95
    )


# ============================================================
# FIND INTENT
# ============================================================

def find_intent(user_message):

    user_text = normalize_text(
        user_message
    )


    if not user_text:

        return None, None, 0


    user_words = set(
        user_text.split()
    )


    best_intent = None
    best_score = 0


    # --------------------------------------------------------
    # Check every intent
    # --------------------------------------------------------

    for intent in intents_data.get(
        "intents",
        []
    ):

        tag = intent.get(
            "tag",
            "unknown"
        )


        intent_score = 0


        # ----------------------------------------------------
        # Original intent patterns
        # ----------------------------------------------------

        for pattern in intent.get(
            "patterns",
            []
        ):

            score = score_phrase(
                user_text,
                user_words,
                pattern
            )


            intent_score = max(
                intent_score,
                score
            )


        # ----------------------------------------------------
        # Additional synonyms
        # ----------------------------------------------------

        for synonym in INTENT_SYNONYMS.get(
            tag,
            []
        ):

            score = score_phrase(
                user_text,
                user_words,
                synonym
            )


            if score > 0:

                score += 5


            intent_score = max(
                intent_score,
                min(score, 100)
            )


        # ----------------------------------------------------
        # Keep strongest intent
        # ----------------------------------------------------

        if intent_score > best_score:

            best_score = intent_score

            best_intent = intent


    # --------------------------------------------------------
    # Return detected intent
    # --------------------------------------------------------

    if (
        best_intent
        and
        best_score >= 15
    ):

        tag = best_intent.get(
            "tag",
            "unknown"
        )


        responses = best_intent.get(
            "responses",
            []
        )


        if responses:

            intent_response = (
                responses[0]
            )

        else:

            intent_response = (
                "Sorry, I don't have an answer "
                "available for that."
            )


        return (

            tag,

            intent_response,

            min(
                round(best_score),
                100
            )
        )


    return (
        None,
        None,
        0
    )


# ============================================================
# KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_knowledge(
    user_message,
    intent=None
):

    user_text = normalize_text(
        user_message
    )


    # ========================================================
    # CASE 1
    # Intent exists
    # ========================================================

    if intent in INTENT_TO_TOPIC:

        target_topic = (
            INTENT_TO_TOPIC[intent]
        )


        for item in knowledge_data:

            if (
                item.get("topic")
                ==
                target_topic
            ):

                return (
                    item.get("answer"),
                    100
                )


    # ========================================================
    # CASE 2
    # NO intent
    #
    # IMPORTANT:
    # Do NOT allow weak single-word matches.
    # This fixes:
    #
    # "Tell me about driving"
    #
    # from accidentally becoming "documents".
    # ========================================================

    if not intent:

        return (
            None,
            0
        )


    # ========================================================
    # Keyword retrieval
    # ========================================================

    user_words = set(
        user_text.split()
    )


    best_item = None
    best_score = 0


    for item in knowledge_data:

        score = 0


        keywords = item.get(
            "keywords",
            []
        )


        for keyword in keywords:

            keyword_text = normalize_text(
                keyword
            )


            keyword_words = set(
                keyword_text.split()
            )


            # Exact keyword phrase
            if keyword_text in user_text:

                # Strong match
                score += 35


            else:

                common_words = (
                    user_words &
                    keyword_words
                )


                meaningful_common_words = (
                    common_words -
                    GENERIC_WORDS
                )


                # ------------------------------------------------
                # Prevent weak generic matches
                # ------------------------------------------------

                if len(
                    meaningful_common_words
                ) >= 2:

                    score += (
                        len(
                            meaningful_common_words
                        )
                        * 12
                    )


        # --------------------------------------------------------
        # Intent/topic bonus
        # --------------------------------------------------------

        topic = item.get(
            "topic"
        )


        if (
            intent in INTENT_TO_TOPIC
            and
            topic ==
            INTENT_TO_TOPIC[intent]
        ):

            score += 50


        if score > best_score:

            best_score = score

            best_item = item


    # --------------------------------------------------------
    # Return knowledge result
    # --------------------------------------------------------

    if (
        best_item
        and
        best_score >= 35
    ):

        return (
            best_item.get("answer"),
            min(
                best_score,
                100
            )
        )


    return (
        None,
        0
    )


# ============================================================
# OFFICIAL SARATHI PORTAL
# ============================================================

SARATHI_LINK = (
    "https://sarathi.parivahan.gov.in/"
)


def get_service_link(intent):

    supported_intents = [

        "apply_license",
        "learner_license",
        "driving_test",
        "loss_license",
        "renew_license",
        "documents",
        "fees",
        "application_status",
        "eligibility",
        "address_change",
        "international_driving"
    ]


    if intent in supported_intents:

        return SARATHI_LINK


    return None


# ============================================================
# GREETING DETECTION
# ============================================================

def is_greeting(message):

    text = normalize_text(
        message
    )


    greetings = {

        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",

        "good morning",
        "good afternoon",
        "good evening"
    }


    return (
        text in greetings
    )


# ============================================================
# CHAT API
# ============================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json()


    # --------------------------------------------------------
    # Empty request
    # --------------------------------------------------------

    if not data:

        return jsonify({

            "response":
                "Please enter a question.",

            "intent":
                "empty",

            "confidence":
                0,

            "source":
                "system"
        })


    user_message = data.get(
        "message",
        ""
    ).strip()


    # --------------------------------------------------------
    # Empty message
    # --------------------------------------------------------

    if not user_message:

        return jsonify({

            "response":
                "Please enter a question.",

            "intent":
                "empty",

            "confidence":
                0,

            "source":
                "system"
        })


    # ========================================================
    # GREETING
    # ========================================================

    if is_greeting(
        user_message
    ):

        return jsonify({

            "response":

                "Hello! 👋 I'm your Government "
                "Driving Services AI Assistant. "
                "I can help you with driving "
                "licence applications, learner "
                "licences, renewal, documents, "
                "fees, tests and other licence "
                "services.",

            "intent":
                "greeting",

            "confidence":
                100,

            "source":
                "system"
        })


    # ========================================================
    # STEP 1 — INTENT DETECTION
    # ========================================================

    (
        intent,
        intent_response,
        intent_confidence
    ) = find_intent(
        user_message
    )


    # ========================================================
    # STEP 2 — KNOWLEDGE RETRIEVAL
    # ========================================================

    (
        knowledge_answer,
        knowledge_confidence
    ) = retrieve_knowledge(
        user_message,
        intent
    )


    # ========================================================
    # STEP 3 — KNOWLEDGE ANSWER
    # ========================================================

    if knowledge_answer:

        service_link = (
            get_service_link(
                intent
            )
        )


        response_text = (
            knowledge_answer
        )


        if service_link:

            response_text += (

                "\n\n🔗 Official Sarathi Portal:\n"
                + service_link
            )


        final_confidence = max(

            intent_confidence,

            knowledge_confidence
        )


        return jsonify({

            "response":
                response_text,

            "intent":
                (
                    intent
                    if intent
                    else
                    "knowledge_retrieval"
                ),

            "confidence":
                min(
                    final_confidence,
                    100
                ),

            "source":
                "knowledge_base"
        })


    # ========================================================
    # STEP 4 — INTENT RESPONSE
    # ========================================================

    if intent:

        service_link = (
            get_service_link(
                intent
            )
        )


        response_text = (
            intent_response
        )


        if service_link:

            response_text += (

                "\n\n🔗 Official Sarathi Portal:\n"
                + service_link
            )


        return jsonify({

            "response":
                response_text,

            "intent":
                intent,

            "confidence":
                intent_confidence,

            "source":
                "intent"
        })


    # ========================================================
    # STEP 5 — FINAL FALLBACK
    # ========================================================

    fallback_response = """

I'm sorry, I couldn't understand your question.

I can help you with:

• Applying for a driving licence
• Learner licence
• Licence renewal
• Lost or duplicate licence
• Required documents
• Licence fees
• Application tracking
• Driving tests
• Eligibility
• Address changes
• International driving permits

Please ask me a question about one of these services.
"""


    return jsonify({

        "response":
            fallback_response,

        "intent":
            "fallback",

        "confidence":
            0,

        "source":
            "fallback"
    })


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )