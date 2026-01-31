
# 256 words for 1-byte mapping.
# Theme: AI, Tech, Startups, Crypto, Reddit
WORDLIST = [
    "agent", "alignment", "algorithm", "api", "architecture", "array", "artifact", "asset",
    "autonomous", "backend", "bandwidth", "baseline", "batch", "benchmark", "bias", "binary",
    "bitcoin", "block", "bot", "buffer", "bug", "build", "byte", "cache",
    "canvas", "cap", "chain", "channel", "chat", "checkpoint", "chip", "cipher",
    "circuit", "cloud", "cluster", "code", "cognitive", "commit", "compile", "compute",
    "config", "connect", "console", "constant", "context", "contract", "control", "core",
    "crypto", "cuda", "cycle", "daemon", "data", "database", "debug", "decimal",
    "decode", "deep", "default", "define", "deploy", "depth", "design", "device",
    "digital", "dimension", "disk", "distributed", "dns", "docker", "domain", "drive",
    "driver", "dump", "dynamic", "edge", "editor", "effect", "element", "embedding",
    "encode", "engine", "entropy", "epoch", "error", "ether", "event", "execution",
    "expert", "exploit", "export", "extension", "feature", "field", "file", "filter",
    "firewall", "firmware", "flag", "flash", "float", "flow", "flux", "folder",
    "fork", "form", "frame", "framework", "function", "future", "game", "gateway",
    "generate", "generator", "git", "glitch", "global", "goal", "gpu", "gradient",
    "graph", "grid", "hack", "hardware", "hash", "head", "heap", "host",
    "hugging", "hyper", "image", "import", "index", "inference", "info", "input",
    "install", "instance", "integer", "integration", "interface", "internet", "interpreter", "interrupt",
    "ip", "iteration", "java", "job", "json", "kernel", "key", "keyboard",
    "keyword", "label", "language", "latency", "layer", "layout", "learning", "ledger",
    "library", "license", "limit", "link", "linux", "list", "load", "local",
    "lock", "log", "logic", "login", "loop", "loss", "machine", "macro",
    "main", "map", "mask", "matrix", "memory", "merge", "mesh", "meta",
    "method", "metric", "micro", "miner", "model", "mode", "module", "monitor",
    "mouse", "move", "net", "network", "neural", "node", "noise", "nonce",
    "norm", "null", "number", "object", "offset", "open", "operator", "optimize",
    "option", "oracle", "output", "overflow", "overlay", "packet", "page", "panel",
    "parameter", "parse", "patch", "path", "pattern", "peer", "performance", "perl",
    "permission", "phone", "pipeline", "pixel", "platform", "plugin", "pointer", "policy",
    "pool", "port", "post", "power", "precision", "predict", "prefix", "process",
    "profile", "program", "prompt", "protocol", "proxy", "public", "push", "python",
    "query", "queue", "ram", "random", "range", "rank", "rate", "raw",
    "react", "read", "real", "record", "recursion", "register", "release", "remote",
    "render", "repo", "request", "reset", "resolution", "resource", "response", "restore",
    "result", "return", "robot", "root", "route", "router", "routine", "row",
    "rule", "runtime", "rust", "safe", "save", "scale", "scan", "schema",
    "scope", "screen", "script", "scroll", "search", "secret", "secure", "security",
    "seed", "segment", "select", "self", "semantic", "server", "service", "session",
    "set", "shader", "shell", "shift", "signal", "signature", "silicon", "simple",
    "simulation", "site", "size", "skill", "skip", "slice", "slide", "slot",
    "smart", "socket", "soft", "software", "solid", "solution", "sort", "source",
    "space", "span", "speed", "stack", "stage", "standard", "start", "state",
    "static", "stats", "status", "store", "stream", "string", "struct", "style",
    "subnet", "submit", "switch", "symbol", "sync", "syntax", "system", "table"
]

# Trim strictly to 256 to ensure byte mapping
WORDLIST = WORDLIST[:256]

# Ensure we have exactly 256 words
assert len(WORDLIST) == 256, f"Wordlist length is {len(WORDLIST)}, expected 256"

WORD_TO_BYTE = {w: i for i, w in enumerate(WORDLIST)}

def encode_bytes(data: bytes) -> str:
    """Encodes bytes into a 'shitpost' string."""
    words = []
    for byte in data:
        words.append(WORDLIST[byte])
    return " ".join(words)

def decode_string(text: str) -> bytes:
    """Decodes a 'shitpost' string back into bytes."""
    import re
    # Replace non-alphanumeric with space to handle punctuation
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', text)
    words = cleaned.lower().split()
    
    byte_array = []
    word_set = set(WORDLIST) # Optimization
    
    for w in words:
        if w in word_set:
            byte_array.append(WORD_TO_BYTE[w])
        else:
            # Skip unknown words (filler from stealth mode)
            pass
    return bytes(byte_array)
