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
    "Essentially,", "Basically,", "Actually,", "Honestly speaking,",
    "Regarding the issue,", "Concerning the spec,", "With respect to the logs,",
    "Even if we ignore that,", "Unless the setup is wrong,"
]

def generate_stealth_text(payload_words):
    """
    Wraps payload words into a rambling pseudo-technical stream.
    """
    result = []
    i = 0
    
    # We use a mix of templates and connectors to build a "paragraph"
    while i < len(payload_words):
        sentence_parts = []
        
        # 30% chance of using a connector prefix
        if random.random() < 0.3:
            connector = random.choice(CONNECTORS)
            sentence_parts.append(connector)
            
        tmpl = random.choice(TEMPLATES)
        slots = tmpl.count("{}")
        
        if i + slots > len(payload_words):
            single_slot_templates = [t for t in TEMPLATES if t.count("{}") == 1]
            tmpl = random.choice(single_slot_templates)
            slots = 1
        
        chunk = payload_words[i : i+slots]
        i += slots
        
        filled_template = tmpl.format(*chunk)
        
        # Grammar fix: If we have a connector, lowercase the template (unless it starts with 'I' or proper noun)
        if sentence_parts:
            first_word = filled_template.split()[0]
            if first_word not in ["I", "My", "Did", "Is", "Why"]: # Keep these capped usually
                # Lowercase the first letter
                filled_template = filled_template[0].lower() + filled_template[1:]
        
        sentence_parts.append(filled_template)
        
        result.append(" ".join(sentence_parts))
        
    return " ".join(result)