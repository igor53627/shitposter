# Feature Flags

This project does not use runtime feature flags.

Behavior is controlled by CLI options and API request fields (for example, the
`/encrypt` endpoint uses a `stealth` boolean to enable or disable stealth text).

Operational configuration (such as API host and port) is provided via the
runtime command line; see `docs/DEPLOYMENT.md`.
