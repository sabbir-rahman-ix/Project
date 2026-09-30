import re
import random
from datetime import datetime

class AgentState:

    def __init__(self): 
        self.user_name = None          
        self.turn_count = 0            
        self.last_topic = None         
        self.history = []              

    def remember_name(self, name):
        """Store the user's name in agent memory."""
        self.user_name = name.strip().title()

    def record_turn(self, user_input, bot_response):
        """Log a completed turn (percept + action) into conversation history."""
        self.turn_count += 1
        self.history.append((user_input, bot_response))


def normalize_input(raw_text):
    if not isinstance(raw_text, str):
        return ""
    text = raw_text.strip()
    text = re.sub(r"\s+", " ", text)
    return text.lower()

NON_NAME_WORDS = {
    "sad", "happy", "fine", "good","bad"
}


def extract_name(text):
    patterns = [
        r"my name is ([a-zA-Z]+)",
        r"i am ([a-zA-Z]+)",
        r"i'm ([a-zA-Z]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            candidate = match.group(1)
            if candidate.lower() in NON_NAME_WORDS:
                continue
            return candidate
    return None


def rule_greeting(text):
    return bool(re.search(r"\b(hi|hello|hey|good morning|good evening)\b", text))


def response_greeting(text, state):
    greetings = ["Hello!", "Hi there!", "Hey, good to see you!"]
    if state.user_name:
        return f"{random.choice(greetings)} Welcome back, {state.user_name}."
    return random.choice(greetings) + " What's your name?"


def rule_name(text):
    return extract_name(text) is not None


def response_name(text, state):
    name = extract_name(text)
    state.remember_name(name)
    return f"Nice to meet you, {state.user_name}! How can I help you today?"


def rule_ask_bot_name(text):
    return bool(re.search(r"(your name|who are you)", text))


def response_ask_bot_name(text, state):
    return "I'm RuleBot, a simple rule-based chatbot built for an AI lab assignment."


def rule_how_are_you(text):
    return bool(re.search(r"how are you", text))


def response_how_are_you(text, state):
    return "I'm just a program, so I don't have feelings, but I'm running smoothly! How about you?"


def rule_feeling_good(text):
    return bool(re.search(r"\b(i am|i'm) (good|great|fine|okay|happy)\b", text))


def response_feeling_good(text, state):
    state.last_topic = "mood_positive"
    return "That's wonderful to hear! What's making your day good?"


def rule_feeling_bad(text):
    return bool(re.search(r"\b(i am|i'm) (sad|tired|bad|not okay|upset|angry)\b", text))


def response_feeling_bad(text, state):
    state.last_topic = "mood_negative"
    return "I'm sorry to hear that. Do you want to talk about what's bothering you?"


def rule_ask_time(text):
    return bool(re.search(r"\b(time|clock)\b", text))


def response_ask_time(text, state):
    now = datetime.now().strftime("%H:%M:%S")
    return f"The current system time is {now}."


def rule_ask_capabilities(text):
    return bool(re.search(r"what can you do|help me with", text))


def response_ask_capabilities(text, state):
    return ("I can chat about simple topics, remember your name, tell you the time, "
            "and respond to greetings and feelings. Try saying hello or telling me "
            "your name!")


def rule_thanks(text):
    return bool(re.search(r"\b(thanks|thank you)\b", text))


def response_thanks(text, state):
    return "You're welcome!"


def rule_farewell(text):
    return bool(re.search(r"\b(bye|goodbye|see you|exit|quit)\b", text))


def response_farewell(text, state):
    if state.user_name:
        return f"Goodbye, {state.user_name}! It was nice talking with you."
    return "Goodbye! Have a great day."


def rule_topic_followup(text):
    return bool(re.search(r"\b(nothing much|not sure|just tired|work|school)\b", text))


def response_topic_followup(text, state):
    if state.last_topic == "mood_negative":
        return "That sounds tough. Remember to take breaks and be kind to yourself."
    elif state.last_topic == "mood_positive":
        return "Sounds good! Keep that positive energy going."
    return "I see. Tell me more if you'd like."


RULES = [
    (rule_farewell, response_farewell),
    (rule_thanks, response_thanks),
    (rule_how_are_you, response_how_are_you),
    (rule_feeling_bad, response_feeling_bad),
    (rule_feeling_good, response_feeling_good),
    (rule_name, response_name),
    (rule_ask_bot_name, response_ask_bot_name),
    (rule_ask_time, response_ask_time),
    (rule_ask_capabilities, response_ask_capabilities),
    (rule_greeting, response_greeting),
    (rule_topic_followup, response_topic_followup),
]

DEFAULT_RESPONSES = [
    "That is interesting",
    "I'm not sure I understand fully.",
    "I see",
]

def generate_response(user_text, state):
    try:
        for condition, respond in RULES:
            if condition(user_text):
                return respond(user_text, state)
        return random.choice(DEFAULT_RESPONSES)
    except Exception as error:
        return f"(Internal error while processing that, but let's continue) " \
               f"Sorry, could you say that differently?"


def is_exit_command(user_text):
    return bool(re.search(r"\b(bye|goodbye|exit|quit|see you)\b", user_text))


def main():
    state = AgentState()

    print("=" * 60)
    print(" RuleBot -- A Rule-Based Chatbot (AI Lab Demo)")
    print(" Type 'bye', 'exit', or 'quit' to end the conversation.")
    print("=" * 60)

    while True:
        try:
            raw_input_text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nRuleBot: Conversation interrupted. Goodbye!")
            break

        user_text = normalize_input(raw_input_text)

        if user_text == "":
            print("RuleBot: I didn't catch that -- could you type something?")
            continue

        bot_response = generate_response(user_text, state)
        print(f"RuleBot: {bot_response}")

        state.record_turn(raw_input_text, bot_response)

        if is_exit_command(user_text):
            break

    print(f"\n[Conversation ended after {state.turn_count} turn(s).]")


if __name__ == "__main__":
    main()