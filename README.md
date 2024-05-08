# taptap
Super power for multilingual humans

a simple python script that runs on background and listens to keyboard keys pressed
when the caps lock pressed twice, the last word will be removed and typed again in next language.

When this is useful?
For every blind typers. When youre typing and noticed that the wrong language is used, just double tap the CapsLock, the last typed word will be cleared, the next typing language will be picked and same keyboard buttons will be pressed

Example:
Installed lagugages: English, Russian Hebrew:

Type:
Hello my friend. Ghbdtn
Now press CapsLock twice. The last word will be deleted and typed again in next launguage (Russian)
Hello my friend. Привет

When this is useful?
For every blind typers. When youre typing and noticed that the wrong language is used, just double tap the CapsLock, the last typed word will be cleared, the next typing language will be picked and same keyboard buttons will be pressed

## Developer Instructions

This project requires Python 3.6 or higher. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).


```bash
brew install uv
uv venv  # Create a virtual environment at .venv.
source .venv/bin/activate
uv pip install keyboard colorlog
