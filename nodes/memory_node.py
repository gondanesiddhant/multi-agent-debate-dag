def memory_node(state):
    new_state = dict(state)
    transcript = new_state["transcript"]
    recent = transcript[-3:]

    scientist_view = [f'{x["speaker"]}: {x["content"]}' for x in recent if x["speaker"] != "Philosopher"]
    philosopher_view = [f'{x["speaker"]}: {x["content"]}' for x in recent if x["speaker"] != "Scientist"]

    new_state["agent_context"]["Scientist"] = scientist_view
    new_state["agent_context"]["Philosopher"] = philosopher_view

    new_state["round"] += 1
    new_state["last_step"] = "MemoryNode"
    return new_state