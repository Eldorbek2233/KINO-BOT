# Copilot Instructions for Kino Bot

## Overview
Kino Bot is a Telegram bot designed to manage and share movie files. It includes features for user management, file handling, and admin-specific functionalities. The bot is built using Python and the `python-telegram-bot` library.

## Architecture
- **Main Components**:
  - `bot.py`: Entry point of the application. Sets up the bot, handlers, and commands.
  - `handlers.py`: Contains all the bot's command and message handlers.
  - `config.py`: Stores configuration variables like `TOKEN` and `ADMIN_ID`.
  - `file_ids.json`: JSON database for storing movie file IDs.
- **Data Flow**:
  - User interactions are processed by handlers in `handlers.py`.
  - Admin-specific commands and menus are managed using `ADMIN_ID`.
  - File IDs are stored and retrieved from `file_ids.json`.

## Developer Workflows
### Running the Bot
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the bot:
   ```bash
   python bot.py
   ```

### Debugging
- Use `print` statements in handlers to log user interactions and debug issues.
- Check the `file_ids.json` file for stored movie codes and IDs.

### Testing
- Manually test commands like `/start`, `/stat`, and `/admin_menu`.
- Verify admin-specific functionalities using the `ADMIN_ID`.

## Project-Specific Conventions
- **Command Handlers**:
  - All commands are defined in `handlers.py`.
  - Use `CommandHandler` for slash commands and `MessageHandler` for text-based interactions.
- **Admin-Specific Features**:
  - Admin functionalities are restricted using `ADMIN_ID`.
  - Admin menus use `InlineKeyboardMarkup` for navigation.
- **File Management**:
  - Movie file IDs are stored in `file_ids.json`.
  - Use `save_file_id` and `load_file_ids` functions for file ID management.

## Integration Points
- **Telegram API**:
  - The bot interacts with Telegram using the `python-telegram-bot` library.
  - Commands and messages are processed using `Application`, `CommandHandler`, and `MessageHandler`.
- **JSON Database**:
  - `file_ids.json` is used to store and retrieve movie file IDs.

## Examples
### Adding a New Command
1. Define the handler in `handlers.py`:
   ```python
   async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text("This is a new command!")
   ```
2. Register the command in `bot.py`:
   ```python
   app.add_handler(CommandHandler("new_command", new_command))
   ```

### Saving a File ID
Use the `save_file_id` function in `handlers.py`:
```python
save_file_id("movie_code", "file_id")
```

## Notes
- Ensure `ADMIN_ID` is set correctly in `config.py`.
- Update `requirements.txt` if new dependencies are added.

Feel free to suggest updates or clarify any sections!
