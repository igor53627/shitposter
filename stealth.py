import random

# Templates designed to sound like technical complaints/discussions.
# placeholders {} will be filled with words from our WORDLIST.
# CRITICAL: The "filler" text must NOT contain any words from WORDLIST.
# WORDLIST includes: hardware, layer, error, flag, optimize, latency, performance, function, etc.

TEMPLATES = [
    "Honestly, I think the {} is causing the lag.",
    "Did you check if the {} configures the {} correctly?",
    "The documentation for {} says it depends on {} but that seems wrong.",
    "My logs are showing a weird fault in the {} tier.",
    "Why does the {} always break when I touch the {}?",
    "It is basically a {} issue, not an equipment problem.",
    "I rewrote the {} to improve the {} usage.",
    "The new update deprecated the {} logic.",
    "Can we talk about how bad the {} support is?",
    "Just use a {} wrapper around the {} and it should work.",
    "The {} velocity is bottlenecked by the {}.",
    "I suspect the {} is conflicting with the {}.",
    "Is there a reason the {} is not compatible with {}?",
    "The {} implementation in this project is terrible.",
    "Make sure to set the {} toggle before running the {}.",
]

def generate_stealth_text(payload_words):
    """
    Wraps payload words (list of strings) into sentences.
    """
    result = []
    i = 0
    while i < len(payload_words):
        tmpl = random.choice(TEMPLATES)
        slots = tmpl.count("{}")
        
        # If we don't have enough words left for this template, find a smaller one or just append
        if i + slots > len(payload_words):
            # Try to find a 1-slot template
            single_slot_templates = [t for t in TEMPLATES if t.count("{}") == 1]
            tmpl = random.choice(single_slot_templates)
            slots = 1
        
        chunk = payload_words[i : i+slots]
        i += slots
        
        sentence = tmpl.format(*chunk)
        result.append(sentence)
        
    return " ".join(result)