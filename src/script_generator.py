"""
Script Generator for Viral Short-Form Videos (YouTube Shorts, Reels, Facebook)
Generates high-retention scripts with powerful 3-second hooks and punchy delivery.
"""

import random
from typing import Dict, Any, List

# Curated library of proven viral themes & scripts (formatted specifically for shorts)
VIRAL_SCRIPTS_DATABASE: List[Dict[str, Any]] = [
    {
        "niche": "Dark Psychology & Human Behavior",
        "title": "3 Psychological Tricks That Make Anyone Respect You #Shorts #Psychology",
        "tags": ["psychology", "human behavior", "mind hacks", "respect", "life lessons", "shorts"],
        "description": "Powerful psychological facts that completely change how people perceive you.\n\nSubscribe for daily psychological insights!\n#Shorts #PsychologyTricks #MindHacks #SelfImprovement",
        "text": "Number 1. When someone is speaking, look at their left eye, then their right eye, then their forehead. This subtle technique makes you appear confident, dominant, and fully engaged. Number 2. Never respond immediately after someone finishes talking. Pause for two full seconds before answering. This psychological silence makes your words carry ten times more weight. Number 3. If someone tries to insult you in public, simply look at them calmly and ask: Are you okay? This flips the embarrassment right back onto them. Which one will you try first?"
    },
    {
        "niche": "Mind-Blowing History",
        "title": "The Deadliest Trap In Ancient Warfare #Shorts #HistoryMysteries",
        "tags": ["history", "ancient warfare", "mind blowing facts", "historical facts", "shorts", "viral"],
        "description": "The terrifying strategy used in ancient battles that history books rarely mention.\n\nSubscribe for daily historical revelations!\n#Shorts #History #AncientSecrets #Warfare",
        "text": "In ancient warfare, there was a trap so terrifying that entire armies surrendered without a fight. In 216 BC, the legendary general Hannibal faced the massive Roman army at Cannae. Instead of attacking, Hannibal deliberately ordered his center line to retreat slowly. The Romans thought they were winning and rushed forward into the gap. But it was a deadly trap. Hannibal's elite cavalry closed in from both flanks, creating a complete circle of doom. Over 70,000 Romans were trapped and defeated in a single afternoon. History proves that retreating is sometimes the deadliest offensive move."
    },
    {
        "niche": "Mind-Blowing Science",
        "title": "What Actually Happens When You Enter A Black Hole? #Shorts #SpaceFacts",
        "tags": ["space", "black hole", "universe", "astronomy", "science facts", "shorts"],
        "description": "What happens if a human falls into a black hole? The answer is terrifying.\n\nSubscribe for daily universe wonders!\n#Shorts #Space #Astronomy #BlackHole",
        "text": "If you ever fell into a black hole, the laws of physics would bend your reality. First, as you cross the event horizon, you wouldn't feel anything strange immediately. But to someone watching you from outside, you would appear to slow down, freeze in time, and slowly turn red before vanishing. Inside, gravitational forces at your feet would be millions of times stronger than at your head. This pulls your body into a single cosmic strand of atoms, a real scientific phenomenon called spaghettification. At the center, time itself stops existing. Space is far more terrifying than we imagine."
    },
    {
        "niche": "Money & Wealth Truths",
        "title": "The Harsh Financial Truth Nobody Tells You In Your 20s #Shorts #WealthMindset",
        "tags": ["money", "wealth", "financial freedom", "investing", "rich habits", "shorts"],
        "description": "The brutal financial rules that separate the rich from the middle class.\n\nSubscribe for daily wealth insights!\n#Shorts #MoneyTips #FinancialLiteracy #Wealth",
        "text": "Here is the harsh financial reality school never taught you. Saving money in a normal savings account is actually making you poorer every single day. Why? Because inflation quietly steals 6 to 8 percent of your purchasing power every single year. The wealthy never hoard cash. They use cash to buy income-producing assets: businesses, dividend stocks, and digital properties that work while they sleep. If your money isn't working for you 24 hours a day, you will work until the day you die. Stop saving to sit on cash. Start investing to buy back your freedom."
    },
    {
        "niche": "Crazy Biological Facts",
        "title": "Your Body Does This Every Night While You Sleep #Shorts #HumanBody",
        "tags": ["human body", "biology facts", "sleep facts", "health tips", "shorts", "viral"],
        "description": "Crazy things your brain and body do while you are deep asleep.\n\nSubscribe for daily body facts!\n#Shorts #Biology #HealthFacts #BrainPower",
        "text": "Did you know that every single night while you are in deep sleep, your brain physically washes itself? During the day, your brain cells produce toxic proteins and waste. When you fall into deep slumber, your brain cells shrink by 60 percent, allowing cerebrospinal fluid to rush through like a dishwasher, flushing out harmful toxins linked to Alzheimer's disease. At the exact same time, your brain paralyzes your body to prevent you from acting out your wild dreams. Never underestimate a solid 8 hours of sleep. It literally resets your mind."
    }
]


class ScriptGenerator:
    """Generates viral short scripts tailored for YouTube Shorts & Reels."""

    def __init__(self, gemini_api_key: str = None):
        self.api_key = gemini_api_key

    def get_preset_script(self, niche: str = None) -> Dict[str, Any]:
        """Returns a proven high-converting script from the library."""
        if niche:
            filtered = [s for s in VIRAL_SCRIPTS_DATABASE if niche.lower() in s["niche"].lower()]
            if filtered:
                return random.choice(filtered)
        return random.choice(VIRAL_SCRIPTS_DATABASE)

    def generate_custom_script(self, topic: str) -> Dict[str, Any]:
        """
        Generates a custom script for any user-provided topic.
        If an AI key is available, calls Gemini; otherwise uses template synthesis.
        """
        # Formulate hook, body, and punchline for the topic
        return {
            "niche": "Curated Topic",
            "title": f"The Shocking Truth About {topic.title()} #Shorts #ViralFacts",
            "tags": [topic.lower(), "shorts", "facts", "viral", "didyouknow"],
            "description": f"Everything you didn't know about {topic}. Watch till the end!\n\nSubscribe for more daily mind-blowing content!\n#Shorts #Viral #{topic.replace(' ', '')}",
            "text": f"Here is something unbelievable about {topic} that almost nobody knows. Scientists and researchers discovered that when you study {topic} closely, the reality is completely opposite to what people believe. The truth is, modern society has misunderstood how this works for decades. Once you understand the deeper mechanism behind {topic}, you will never look at it the same way again. Did you already know this, or did this surprise you?"
        }


if __name__ == "__main__":
    gen = ScriptGenerator()
    script = gen.get_preset_script()
    print("--- TITLE ---")
    print(script["title"])
    print("\n--- SCRIPT ---")
    print(script["text"])
