# =============================================================================
# AI DAD JOKE GENERATOR
# Phase 1 — Project 01 | ai-automation-journey
# -----------------------------------------------------------------------------
# What this project teaches:
#   - Loading API keys safely from a .env file (never hardcode secrets)
#   - Making your first OpenAI API call
#   - Structuring prompts with system + user roles
#   - Understanding the temperature parameter
#   - Parsing an API response to extract text
# =============================================================================

import os                          # Built-in: access environment variables
from dotenv import load_dotenv     # Third-party: reads .env file into os environment
from openai import OpenAI          # Third-party: official OpenAI Python client


# -----------------------------------------------------------------------------
# SETUP — Load credentials and initialize the client
# -----------------------------------------------------------------------------

# load_dotenv() reads the .env file in the same directory and loads its
# key=value pairs into the environment. Must be called before os.getenv().
load_dotenv()

# os.getenv("OPENAI_API_KEY") reads the key from the environment (not hardcoded).
# NEVER write your actual API key in code — it would be exposed on GitHub.
# The OpenAI client uses this key to authenticate every API request.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------------------------------------------------------
# CORE FUNCTION — Build the prompt and call the API
# -----------------------------------------------------------------------------

def generate_jokes(topic: str, count: int = 5) -> str:
    """
    Generate dad jokes about a given topic using the OpenAI API.

    Parameters:
        topic (str): The subject the jokes should be about (e.g. "coffee")
        count (int): How many jokes to generate. Defaults to 5.

    Returns:
        str: The AI's response as a plain text string containing the jokes.

    Pattern note:
        This function follows the standard pattern for all AI API calls:
        1. Build a prompt  →  2. Call the API  →  3. Extract and return the text
        You'll reuse this same 3-step pattern in every project going forward.
    """

    # --- Step 1: Build the prompt ---
    # f-strings let us inject Python variables into the prompt dynamically.
    # This is called "prompt templating" — a core prompt engineering technique.
    prompt = f"""Generate {count} original dad jokes about the topic: {topic}

Format each joke like this:
1. [Setup]
   [Punchline]

Make them groan-worthy but family friendly."""

    # --- Step 2: Call the API ---
    response = client.chat.completions.create(

        # The model to use. gpt-4o-mini is fast and cheap — ideal for simple tasks.
        # Other options: "gpt-4o" (smarter, pricier), "gpt-3.5-turbo" (older, cheaper)
        model="gpt-4o-mini",

        # Messages is a list of dicts that forms the conversation history.
        # Each message has a "role" and "content":
        #   "system" — sets the AI's persona/instructions for the whole session
        #   "user"   — the actual request (what you'd type in ChatGPT)
        #   "assistant" — used when building multi-turn conversations (Phase 3)
        messages=[
            {
                "role": "system",
                "content": "You are a dad joke expert. All your jokes are original, punny, and make people groan."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        # temperature controls creativity/randomness of the output.
        # 0.0 = very deterministic (almost same output every run)
        # 0.7 = balanced (good default for most tasks)
        # 1.0 = creative/varied (good for jokes, stories, brainstorming)
        # 1.5+ = chaotic (rarely useful)
        temperature=1,

        # max_tokens caps how long the response can be.
        # 1 token ≈ 0.75 words. 500 tokens ≈ ~375 words — plenty for 5 jokes.
        # This also controls your API cost: fewer tokens = cheaper call.
        max_tokens=500
    )

    # --- Step 3: Extract the text from the response ---
    # The API returns a complex object. The actual text lives at:
    # response.choices[0].message.content
    #   .choices      — list of possible responses (usually just 1)
    #   [0]           — first (and default) choice
    #   .message      — the assistant's message object
    #   .content      — the actual text string
    return response.choices[0].message.content


# -----------------------------------------------------------------------------
# MAIN — Handle user input and display output
# -----------------------------------------------------------------------------

def main():
    """
    Entry point of the script.
    Handles user input, calls generate_jokes(), and prints the result.

    Structure note:
        Keeping main() separate from generate_jokes() is good practice.
        It means generate_jokes() can be imported and reused in other scripts
        without triggering the print/input logic.
    """
    print("🤣 AI Dad Joke Generator")
    print("-" * 30)

    # input() pauses the script and waits for the user to type.
    # .strip() removes any accidental leading/trailing whitespace.
    topic = input("Enter a topic for your dad jokes: ").strip()

    # Fallback: if user presses Enter without typing, default to "programming"
    if not topic:
        topic = "programming"

    print(f"\nGenerating jokes about '{topic}'...\n")

    # Call the function — this is where the API request actually happens
    jokes = generate_jokes(topic)

    # Print the returned string (the AI's response)
    print(jokes)
    print("\n" + "-" * 30)
    print("Have a groaning day! 👋")


# -----------------------------------------------------------------------------
# ENTRY POINT GUARD
# -----------------------------------------------------------------------------
# This block ensures main() only runs when you execute this file directly.
# If another script imports this file (e.g. to reuse generate_jokes()),
# main() will NOT run automatically.
# This is a Python best practice — always include it in your scripts.
if __name__ == "__main__":
    main()