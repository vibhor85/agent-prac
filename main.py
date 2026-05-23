from env import load_environment
from prompt import read_system_prompt
from client import ChatClient
from tools import execute_tool
import json


def main() -> None:
    print("[log] Starting main()")
    load_environment()
    system_prompt = read_system_prompt()

    chat_client = ChatClient(system_prompt)
    print("[log] ChatClient initialized")

    # Add initial user message
    initial_message = "Hey I forgot where i spent the 95$, can u tell me ?"
    chat_client.add_user_message(initial_message)
    print(f"[log] Added initial user message: {initial_message}")

    while True:

        chat_completion = chat_client.create_chat_completion()
        print("[log] Received chat completion response")

        # Check for tool calls
        if hasattr(chat_completion.choices[0].message, "tool_calls") and chat_completion.choices[0].message.tool_calls:
            tool_calls = chat_completion.choices[0].message.tool_calls
            print(f"[log] Model requested {len(tool_calls)} tool call(s)")

            message = chat_completion.choices[0].message

            assistant_message = {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            }

            chat_client.append_message(assistant_message)
            print("[log] Appended assistant tool-call message to history")

            # Execute each tool call
            for idx, tool in enumerate(tool_calls):
                name = tool.function.name
                arguments = json.loads(tool.function.arguments)
                tool_call_id = tool.id
                print(
                    f"[log] Executing tool {idx+1}: {name} with arguments: {arguments}, tool_call_id: {tool_call_id}")

                result = execute_tool(name, arguments)
                print(f"[log] Tool result: {result}")

                # Add tool result as tool message with name and tool_call_id
                chat_client.push_message(
                    "tool",
                    json.dumps(result),
                    tool_call_id=tool_call_id,
                    name=name,
                )
                print(
                    f"[log] Added tool result to message history with tool_call_id={tool_call_id} and name={name}")

            # Loop continues to next iteration to get final response
            print("[log] Loop continues to get model's response to tool result")

        else:
            # No tool calls - assistant provided final response
            final_response = chat_completion.choices[0].message.content
            print(final_response)
            return


if __name__ == "__main__":
    main()
