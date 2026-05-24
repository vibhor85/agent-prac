Built a lightweight AI Finance Agent to explore how modern AI agents work behind the scenes — from LLM reasoning and function/tool calling to conversation memory and orchestration loops. This project helped me understand the core architecture of agentic systems, prompt engineering, structured tool execution, and real-world AI workflow design using Python and Groq APIs.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_api_key_here
   MODEL_NAME=llama-3.3-70b-versatile
   ```

## Running

### User Mode (Chat Only)

```bash
python main.py
```

Shows only the chat conversation between you and the AI assistant.

### Debug Mode (With Logs)

```bash
python main.py --debug
```

Shows all debug logs and internal operations (tool calls, message history, etc.) along with the chat.

## Features

- **Chat Interface:** Interactive CLI chat with an AI assistant
- **Tool Calling:** The assistant can call tools to:
  - Get monthly expense reports
  - Check account balance
  - Add new expenses
  - Update account balance (add/remove money)
- **Debug Mode:** Toggle verbose logging with `--debug` flag
- **Message History:** Maintains conversation context for multi-turn interactions
