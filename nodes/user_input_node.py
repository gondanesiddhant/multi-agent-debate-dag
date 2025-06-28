def user_input_node(state):
    topic = input("Enter topic for debate: ").strip()
    return {
        "topic": topic,
        "round": 1,
        "transcript": [],
        "agent_context": {"Scientist": [], "Philosopher": []},
        "used_arguments": set(),
        "final_judgment": {},
        "last_step": "UserInputNode"
    }