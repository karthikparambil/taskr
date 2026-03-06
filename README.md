<img src="assets/todo.png" width=100px> 

#  Taskr - To-Do App

**Taskr** is a beautiful, feature-packed To-Do application designed for high productivity and visual excellence. It combines a powerful Flask backend with a premium, responsive frontend experience.

## Features

- **Premium UI/UX**: Modern design with smooth transitions, dark mode compatible surfaces, and custom typography.
- **Smart Tags**: Use `#urgent`, `#high`, `#medium`, `#low` to prioritize tasks.
- **Autocomplete Suggestions**: Real-time suggestions for priority tags as you type.
- **Daily Tasks**: Tag tasks with `#daily` for automatic resets every 24 hours.
- **Drag-and-Drop**: Reorder your tasks effortlessly with an intuitive drag-and-drop interface.
- **Meta Parsing**: Automatically extracts assignees (`@name`) and priorities from task text.
- **Markdown Storage**: Your data is saved in `todos.md`, making it portable and easy to read.
- **Undo Delete**: Accidentally deleted something? No worries, use the snackbar to undo!

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Storage**: Markdown (`todos.md`)

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/karthikparambil/taskr.git
   cd taskr
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open in your browser**:
   Navigate to `http://localhost:5100`

## Linux Desktop Setup (Optional)
To launch Taskr directly from your application menu, follow these steps:

### 1. Run Auto-Setup

The launcher script can automatically create a desktop entry for you. Simply run:

```bash
chmod +x to_do.sh
./to_do.sh --setup
```

This will create a `todo.desktop` file in `~/.local/share/applications/`, allowing you to launch Taskr from your application menu.

### 2. Manual Setup (Optional)

If you prefer to do it manually, create a file at `~/.local/share/applications/todo.desktop` with the following content:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Todo App
Comment=Personal To-Do Manager
Icon=accessories-text-editor
Exec=/bin/bash /path/to/your/taskr/to_do.sh
Terminal=false
Categories=Utility;Office;
Keywords=todo;tasks;notes;markdown;
StartupNotify=true
```


## 📁 Architecture

Refer to [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed breakdown of the project structure and technical implementation.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Distributed under the MIT License. See `LICENSE` for more information.
