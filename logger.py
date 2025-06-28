# logger.py

import logging

logging.basicConfig(
    filename="log.txt",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_state(step, state):
    logging.info(f"--- {step} ---")
    logging.info(f"Round: {state.get('round')}")
    logging.info(f"Last Transcript Entry: {state['transcript'][-1] if state['transcript'] else 'N/A'}")
    logging.info(f"Memory Contexts: {state['agent_context']}")
    if state.get("final_judgment"):
        logging.info(f"Final Verdict: {state['final_judgment']}")
