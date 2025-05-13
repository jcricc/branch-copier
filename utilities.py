import pyperclip

def set_clipboard():
    try:
        pyperclip.set_clipboard("pbcopy")
    except:
        pass
