from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from prompts import SCIENTIST_PROMPT, PHILOSOPHER_PROMPT
import os

llm = ChatGroq(
    model="llama3-8b-8192",
    api_key=os.getenv("GROQ_API_KEY")
)

def agent_fn(role):
    def _agent_node(state):
        topic = state["topic"]
        context = "\n".join(state["agent_context"][role])
        prompt_template = SCIENTIST_PROMPT if role == "Scientist" else PHILOSOPHER_PROMPT
        system_msg = SystemMessage(content=prompt_template.format(topic=topic, context=context))
        user_msg = HumanMessage(content="Please respond.")

        response = llm.invoke([system_msg, user_msg]).content

        if response in state["used_arguments"]:
            raise ValueError("Duplicate argument detected!")

        new_state = dict(state)
        new_state["used_arguments"].add(response)
        new_state["transcript"].append({"speaker": role, "content": response})
        new_state["last_step"] = "AgentA" if role == "Scientist" else "AgentB"
        return new_state
    return _agent_node

AgentA = agent_fn("Scientist")
AgentB = agent_fn("Philosopher")