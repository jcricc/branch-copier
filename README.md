# Project to AI Helper

**Branch Copier** is a fast and simple desktop tool that helps developers explore their codebase and easily copy file contents or project structure into AI tools like ChatGPT, GitHub Copilot, or Claude.

Whether you're debugging, explaining code, or prompting AI to generate new features, this app provides a developer-friendly interface to prepare and copy the exact context you need.

---

## Features

- ✅ Browse any local project folder
- ✅ Auto-list files with extension and folder filters
- ✅ One-click preview of file contents
- ✅ Copy file contents with filename included for AI context
- ✅ Copy entire folder structure to clipboard
- ✅ Cross-platform (works on macOS and Windows)
- ✅ Lightweight and dependency-free beyond PyQt6

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jcricc/branch-copier.git
cd branchcopier
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install PyQt6 pyperclip
```

---

## How to Run

```bash
python main.py
```

---

## 🛠 How It Works

### Choose Project Folder

Click the "Choose Project Folder" button to open a local project. The app automatically lists files inside, recursively.

### Filter Files (Optional)

- Use the **Include extensions** field to limit by type (e.g., `.py, .js`).
- Use the **Exclude folders** field to skip directories like `.git`, `__pycache__`.

### Preview & Copy

- Click any file to preview its contents.
- Click **Copy File Contents** to copy its content with the filename as a header:

```python
# src/utils/helpers.py

def example():
    ...
```

### Copy Folder Structure

Use the **Copy Folder Structure** button to copy an indented layout like:

```plaintext
project/
  main.py
  utils/
    helpers.py
    data.py
```

---

## Use Cases

| Scenario                        | How the App Helps                              |
|---------------------------------|-----------------------------------------------|
| 📌 Asking AI to debug a file    | Preview and copy with filename included       |
| 📁 Giving AI context on structure | Copy your folder tree as Markdown or plaintext |
| 🧹 Sharing minimal project outline | Filter out irrelevant files or folders easily |
| ⚙️ Working across any language  | Extension-agnostic filtering makes it language neutral |

---

https://github.com/user-attachments/assets/f752fd76-4f98-42f3-8776-322b21a9d665

## Why This Tool?

Most AI tools respond best with:

- Clear file names
- Clean source content
- Compact structure previews

This app is designed to make gathering and formatting that context effortless.

---

## Roadmap Ideas

- Add extension auto-detection with quick toggle chips
- Right-click context menu for file actions
- File search bar
- Zip export or multi-file copy
- Save/share a full AI prompt pack

---

## 🤝 Contributing

Feel free to open issues, request features, or fork the repo! This is my first released software, so I am very excited for any engagement or requests.

---

## 📜 License

MIT License © 2024 jcricc
