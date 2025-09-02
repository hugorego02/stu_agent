from agno.playground import Playground, serve_playground_app
from agent.setup import agent

app = Playground(agents=[agent]).get_app()

if __name__ == "__main__":
    # from agent.setup import clear_all_history
    # clear_all_history()  # optional
    serve_playground_app("app:app", port=7777, reload=True)