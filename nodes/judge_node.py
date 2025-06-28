import re
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from prompts import JUDGE_PROMPT
import os

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

def judge_node(state):
    topic = state["topic"]
    transcript = "\n".join([f'{x["speaker"]}: {x["content"]}' for x in state["transcript"]])
    prompt = JUDGE_PROMPT.format(topic=topic, transcript=transcript)

    system_msg = SystemMessage(content=prompt)
    user_msg = HumanMessage(content="Evaluate the debate.")
    response = llm.invoke([system_msg, user_msg]).content

    match = re.search(r"Winner:\s*(.*?)\nReason:\s*(.*)", response, re.DOTALL)
    winner = match.group(1).strip() if match else "Unknown"
    reason = match.group(2).strip() if match else "No reason parsed."

    new_state = dict(state)
    new_state["final_judgment"] = {
        "summary": response,
        "winner": winner,
        "reason": reason
    }
    new_state["last_step"] = "JudgeNode"
    return new_state