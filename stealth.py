import random

# Templates designed to sound like technical complaints/discussions.
# placeholders {} will be filled with words from our WORDLIST.
# CRITICAL: The "filler" text must NOT contain any words from WORDLIST.
# WORDLIST includes: hardware, layer, error, flag, optimize, latency, performance, function, etc.

TEMPLATES = [
    "Honestly, I think the {} is causing the lag.",
    "Did you check if the {} configures the {} correctly?",
    "The documentation for {} says it depends on {} but that seems wrong.",
    "My readout is showing a weird fault in the {} tier.",
    "Why does the {} always break when I touch the {}?",
    "It is basically a {} issue, not an equipment problem.",
    "I rewrote the {} to improve the {} usage.",
    "The new update deprecated the {} behavior.",
    "Can we talk about how bad the {} support is?",
    "Just use a {} wrapper around the {} and it should work.",
    "The {} velocity is bottlenecked by the {}.",
    "I suspect the {} is conflicting with the {}.",
    "Is there a reason the {} is not compatible with {}?",
    "The {} implementation in this project is terrible.",
    "Make sure to enable the {} toggle before running the {}.",
]

# Simple Markov-like tech jargon generator
# This makes the text look like a "stream of consciousness" from a bot.
CONNECTORS = [
    "essentially", "basically", "actually", "honestly", "honestly speaking",
    "regarding the", "concerning the", "with respect to", "as for the",
    "whenever I try to", "even if we", "unless the", "until the"
]

def generate_stealth_text(payload_words):
    """
    Wraps payload words into a rambling pseudo-technical stream.
    """
    result = []
    i = 0
    
    # We use a mix of templates and connectors to build a "paragraph"
    while i < len(payload_words):
        # 30% chance of using a connector
        if random.random() < 0.3:
            result.append(random.choice(CONNECTORS))
            
        tmpl = random.choice(TEMPLATES)
        slots = tmpl.count("{}")
        
        if i + slots > len(payload_words):
            single_slot_templates = [t for t in TEMPLATES if t.count("{}") == 1]
            tmpl = random.choice(single_slot_templates)
            slots = 1
        
        chunk = payload_words[i : i+slots]
        i += slots
        
        result.append(tmpl.format(*chunk))
        
    return " ".join(result)