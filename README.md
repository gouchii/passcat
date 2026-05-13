
# PassCat

PassCat is a minimalist password generator and security analysis tool built with Python and Flet.

It focuses on generating strong passwords while providing real-time feedback on:
- strength
- crack resistance
- structural weaknesses
- breach exposure
- password patterns

Live Demo: https://passcat.onrender.com/

## Features

- Secure password generation
- Adjustable password length
- Minimum number and symbol requirements
- Uppercase, lowercase, number, and symbol toggles
- Real-time password strength analysis using zxcvbn
- Crack time estimation
- Pattern and vulnerability detection
- Breach checking with Have I Been Pwned
- Responsive desktop and web interface

## Tech Stack

- Python
- Flet
- zxcvbn
- Have I Been Pwned API
- uv

## Run Locally

Install dependencies:

```bash
uv sync
````

Run desktop app:

```bash
uv run flet run src/main.py
```

Run web version locally:

```bash
uv run flet run --web src/main.py
```

## Deployment

PassCat is deployed using Render.

Start command:

```bash
uv run flet run src/main.py --web --port $PORT
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

