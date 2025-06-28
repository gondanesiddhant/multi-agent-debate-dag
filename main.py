# main.py

from langgraph.graph import StateGraph, END
from nodes.user_input_node import user_input_node
from nodes.agent_node import AgentA, AgentB
from nodes.memory_node import memory_node
from nodes.judge_node import judge_node
from logger import log_state
from rich import print
from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict, List, Dict, Set

class DebateState(TypedDict):
    topic: str
    round: int
    transcript: List[Dict[str, str]]
    agent_context: Dict[str, List[str]]
    used_arguments: Set[str]
    final_judgment: Dict[str, str]
    last_step: str


def build_graph():
    sg = StateGraph(DebateState)
    
    sg.add_node("UserInputNode", user_input_node)
    sg.add_node("AgentA", AgentA)
    sg.add_node("AgentB", AgentB)
    sg.add_node("MemoryNode", memory_node)
    sg.add_node("JudgeNode", judge_node)

    sg.set_entry_point("UserInputNode")

    def next_node_selector(state):
        if state["round"] > 8:
            return "JudgeNode"
        return "AgentA" if state["round"] % 2 == 1 else "AgentB"

    sg.add_conditional_edges(
    "MemoryNode",
    next_node_selector,
    {"AgentA": "AgentA", "AgentB": "AgentB", "JudgeNode": "JudgeNode"}
    )



    sg.add_edge("UserInputNode", "AgentA")
    sg.add_edge("AgentA", "MemoryNode")
    sg.add_edge("AgentB", "MemoryNode")
    sg.add_edge("JudgeNode", END)

    return sg.compile()

if __name__ == "__main__":
    graph = build_graph()
    state = {}
    for state in graph.stream({}, stream_mode="values"):
        
        step = state.get("last_step", "UNKNOWN")


        log_state(step, state)

        if step in ("AgentA", "AgentB") and state.get("transcript"):
            last_entry = state["transcript"][-1]
            print(f"\n[bold white]Round {state['round'] - 1}[/bold white]")
            print(f"[bold cyan]{last_entry['speaker']}:[/bold cyan] {last_entry['content']}\n")

        elif step == "JudgeNode":
            verdict = state["final_judgment"]
            print("\n[bold green][Judge] Debate Summary[/bold green]")
            print(verdict["summary"])
            print(f"\n[bold yellow]Winner:[/bold yellow] {verdict['winner']}")
            print(f"[bold cyan]Reason:[/bold cyan] {verdict['reason']}")






