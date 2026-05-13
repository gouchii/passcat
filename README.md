
# PassCat

PassCat is a minimalist password generator and analysis tool built with Flet and Python.

It focuses on:
- secure password generation
- configurable password constraints
- real-time strength analysis using zxcvbn
- breach detection using Have I Been Pwned
- responsive desktop and web UI

## Features

- Adjustable password length
- Minimum number and symbol requirements
- Uppercase, lowercase, number, and symbol toggles
- Real-time password strength scoring
- Crack time estimation
- Pattern and vulnerability analysis
- Breach detection
- Desktop and web support

## Tech Stack

- Python
- Flet
- zxcvbn
- Have I Been Pwned API

## Run Locally

Using uv:

```bash
uv sync
uv run flet run
````

Run in browser:

```bash
uv run flet run --web
```

## Build Web Version

Local web build:

```bash
flet build web --output docs
```

Serve locally:

```bash
uv run flet serve docs
```



## Project Structure

```text
src/
├── components/
├── core/
├── views/
├── generator.py
├── validator.py
├── breach_checker.py
└── main.py
```

## License

MIT



