# dag_diagram.py

from graphviz import Digraph

def generate_dag_diagram():
    dot = Digraph(comment="LangGraph Debate DAG", format="png")
    dot.attr(rankdir='LR', size='8,5')

    # Define nodes
    dot.node("UserInputNode", "UserInputNode")
    dot.node("AgentA", "AgentA\n(Scientist)")
    dot.node("AgentB", "AgentB\n(Philosopher)")
    dot.node("MemoryNode", "MemoryNode")
    dot.node("JudgeNode", "JudgeNode")

    # Edges
    dot.edge("UserInputNode", "AgentA")
    dot.edge("AgentA", "MemoryNode")
    dot.edge("AgentB", "MemoryNode")

    # MemoryNode routes next agent based on round count
    dot.edge("MemoryNode", "AgentA", label="Odd Round")
    dot.edge("MemoryNode", "AgentB", label="Even Round")
    dot.edge("MemoryNode", "JudgeNode", label="After Round 8")

    # End
    dot.node("END", "END", shape="doublecircle")
    dot.edge("JudgeNode", "END")

    # Output
    dot.render("dag_diagram", cleanup=True)
    print("Generated DAG diagram as dag_diagram.png")

if __name__ == "__main__":
    generate_dag_diagram()
