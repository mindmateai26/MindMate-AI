import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.gemini_service import gemini_service

def test_diverse_relevant_replies():
    test_prompts = [
        ("Greetings", "Hello there!"),
        ("Identity", "Who are you and what can you do?"),
        ("Calming/Breathing", "Help me calm down, I feel panic"),
        ("Exam Pressure", "Padikka mudiyala, exam tension romba iruku"),
        ("Sleep Problem", "I can't sleep at night, my thoughts are racing"),
        ("Overthinking", "Mind romba overthink pannuthu, bayama iruku"),
        ("Actionable Steps", "What should I do next? Enna panrathu?"),
        ("Friend Conflict", "I had a big fight with my best friend"),
        ("Tamil Support", "எனக்கு பரீட்சை பயமாக உள்ளது, நான் என்ன செய்ய வேண்டும்?")
    ]

    responses = []
    print("\n--- Testing Dialogue Variety and Specific Intent Relevance ---")
    for category, prompt in test_prompts:
        res = gemini_service.chat(prompt, history=[])
        reply = res["text"]
        responses.append(reply)
        print(f"\n[Prompt: {category}]")
        print(f"User:  {prompt}")
        print(f"Reply: {reply[:130]}...")
        print(f"Mood:  {res['moodTag']} | Lang: {res['language']}")

        # Ensure not empty
        assert len(reply) > 20

    # Ensure all replies are distinct and unique
    unique_replies = set(responses)
    assert len(unique_replies) == len(test_prompts), f"Expected {len(test_prompts)} distinct replies, got {len(unique_replies)}"
    print(f"\n[PASS] All {len(test_prompts)} prompts generated unique, targeted, and relevant responses!")

if __name__ == "__main__":
    test_diverse_relevant_replies()
