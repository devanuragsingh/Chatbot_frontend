import re

# 🧠 Extract info dynamically
def extract_info(text):
    text = text.lower()

    data = {}

    # Name
    name_match = re.search(r"my name is (\w+)", text)
    if name_match:
        data["name"] = name_match.group(1)

    # Age
    age_match = re.search(r"(i am|my age is) (\d+)", text)
    if age_match:
        data["age"] = age_match.group(2)

    # City
    city_match = re.search(r"(i am from|i live in) ([a-zA-Z ]+)", text)
    if city_match:
        data["city"] = city_match.group(2)

    return data


def local_response(user_input, memory):
    user_input_lower = user_input.lower()

    # Extract latest info
    extracted = extract_info(user_input)

    # =========================
    # 🧠 STORE RESPONSE
    # =========================
    if extracted:
        return "Got it! I'll remember that."

    # =========================
    # 🧠 RECALL NAME
    # =========================
    if "name" in user_input_lower:
        for msg in reversed(memory):
            info = extract_info(msg["content"])
            if "name" in info:
                return f"Your name is {info['name']}."
        return "I don't know your name yet."

    # =========================
    # 🧠 RECALL AGE
    # =========================
    if "age" in user_input_lower:
        for msg in reversed(memory):
            info = extract_info(msg["content"])
            if "age" in info:
                return f"You are {info['age']} years old."
        return "I don't know your age yet."

    # =========================
    # 🧠 RECALL CITY
    # =========================
    if "from" in user_input_lower or "city" in user_input_lower:
        for msg in reversed(memory):
            info = extract_info(msg["content"])
            if "city" in info:
                return f"You are from {info['city']}."
        return "I don't know your city yet."

    # =========================
    # 👋 GREETING
    # =========================
    if "hello" in user_input_lower or "hi" in user_input_lower:
        return "Hey! How can I help you?"

    return "I'm still learning, but I remember what you say!"