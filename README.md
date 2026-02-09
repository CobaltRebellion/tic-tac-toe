# Multiplayer Tic-Tac-Toe with Live Chat

A real-time, terminal-based multiplayer Tic-Tac-Toe game in Python featuring live chat for players and spectators.  
The project uses a client–server architecture with concurrent networking and a dynamic terminal UI using [Rich](https://github.com/Textualize/rich).

---

## Features

- **Real-time multiplayer:** Two players can play Tic-Tac-Toe simultaneously while spectators can join and chat.
- **Authoritative server:** The server enforces turns, validates moves, and detects wins to prevent cheating.
- **Concurrent networking:** Handles multiple clients using Python’s `select()` for non-blocking I/O.
- **Live terminal UI:** Split-screen display with the board on the left and chat on the right, powered by the Rich library.
- **JSON-based messaging protocol:** Clean communication for game moves, chat messages, and player events.

---

## Technologies Used

- **Python 3**
- **Sockets & Select module** for TCP networking
- **Threading** for simultaneous input and network listening on the client
- **Rich** for terminal UI rendering
- **JSON** for message serialization

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/CobaltRebellion/your-repo-name.git
cd your-repo-name
```
2. Install dependencies:
```bash
pip install rich
```
---
## Usage
#### Start the Server
```bash
python server.py <port>
```

Example:

```
python server.py 12345
```
#### Connect a Client
```bash
python client.py <nickname> <host> <port>
```

Example:

```bash
python client.py Alice localhost 12345
python client.py Bob localhost 12345
```

#### How to move and chat:
Players take turns using the command:
```bash
/move <x> <y>
```
Chat by typing messages normally.

Quit using:
```
/q
```
