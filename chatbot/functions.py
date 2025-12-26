from langchain_core.messages import AIMessage
import sqlite3
def token_usage (ai_message):
     # AIMessage terakhir

    token_usage = ai_message.response_metadata["token_usage"]

    input_tokens = token_usage["prompt_tokens"]
    output_tokens = token_usage["completion_tokens"]
    total_tokens = token_usage["total_tokens"]

    # total_output_tokens = output_tokens

    token_info = {
        "Input Tokens": input_tokens,
        "Output Tokens": output_tokens,
        "Total Tokens": total_tokens,
    }

    return token_info

def extract_tool_calls(result):
    tool_calls = []

    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            tool_calls.extend(msg.tool_calls)

    return tool_calls

def get_db_connection_claim():
    return sqlite3.connect("claimdata.db")

def claim(claim_id):
    conn = get_db_connection_claim()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM claims WHERE claim_id = ?",
        (claim_id,)
    )
    row = cursor.fetchone()

    conn.close()
    return row

def get_db_connection_policy():
    return sqlite3.connect("policydata.db")

def policy(policy_number):
    conn = get_db_connection_policy()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM policies WHERE policy_number = ?",
        (policy_number,)
    )
    row = cursor.fetchone()

    conn.close()
    return row