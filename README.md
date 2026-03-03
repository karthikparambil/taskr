#  Taskr - To-Do App

**Taskr** is a beautiful, feature-packed To-Do application designed for high productivity and visual excellence. It combines a powerful Flask backend with a premium, responsive frontend experience.

![Taskr UI](assets/todo.png)

## ✨ Features

- **Premium UI/UX**: Modern design with smooth transitions, dark mode compatible surfaces, and custom typography.
- **Smart Tags**: Use `#urgent`, `#high`, `#medium`, `#low` to prioritize tasks.
- **Autocomplete Suggestions**: Real-time suggestions for priority tags as you type.
- **Daily Tasks**: Tag tasks with `#daily` for automatic resets every 24 hours.
- **Drag-and-Drop**: Reorder your tasks effortlessly with an intuitive drag-and-drop interface.
- **Meta Parsing**: Automatically extracts assignees (`@name`) and priorities from task text.
- **Markdown Storage**: Your data is saved in `todos.md`, making it portable and easy to read.
- **Undo Delete**: Accidentally deleted something? No worries, use the snackbar to undo!

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Frontend**: Vanilla JavaScript, CSS3, HTML5
- **Storage**: Markdown (`todos.md`)
- **Icons**: SVG-based custom icons

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/taskr.git
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

## 🐧 Linux Desktop Setup (Optional)

To launch Taskr directly from your application menu, follow these steps:

### 1. Configure the Launcher Script

Open `script/to_do.sh` and update the `APP_DIR` variable to point to your project directory:

```bash
APP_DIR="/home/YOUR_USERNAME/path/to/taskr"
```

### 2. Create a Desktop Entry

Create a new file at `/usr/share/applications/todo.desktop` (requires sudo) or `~/.local/share/applications/todo.desktop` (for current user only) with the following content:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Todo App
Comment=Personal To-Do Manager
Icon=accessories-text-editor
Exec=/bin/bash /home/YOUR_USERNAME/path/to/taskr/script/to_do.sh
Terminal=false
Categories=Utility;Office;
Keywords=todo;tasks;notes;markdown;
StartupNotify=true
```

> [!IMPORTANT]
> Make sure to replace `/home/YOUR_USERNAME/path/to/taskr` with the actual absolute path to your project.

### 3. Make the Script Executable

```bash
chmod +x script/to_do.sh
```

## 📁 Architecture

Refer to [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed breakdown of the project structure and technical implementation.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
