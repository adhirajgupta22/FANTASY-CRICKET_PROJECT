# app.py
from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

from researcher import *
from selector import *
from fantasy_FAQ import *
from data_collector import *
from faceoff import *
from form_accessor import *

from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

app = Flask(__name__, static_folder="client_build", static_url_path="")
CORS(app)  # allows requests from the frontend

# === Load LangGraph Supervisor ===
memory = MemorySaver()
config = {"configurable": {"thread_id": "fantasy123"}}

LLM = ChatOpenAI(model="gpt-4.1")
tavily_search = TavilySearchResults(max_results=5)
duck_search = DuckDuckGoSearchRun()

supervisor_agent = create_supervisor(
    model=LLM,
    agents=[research_agent, data_collector_agent, player_selector_agent, faceoff_agent, form_accessor_agent, FAQ_agent],
    tools=[tavily_search, duck_search],
    output_mode="full_history",
    prompt=(
    """
        You are a helpful AI assistant specialized in fantasy sports, particularly focused on the Indian Premier League (IPL).

        Your core expertise is in:
        - Fantasy league strategy
        - Player stats, form, and selection
        - Match analysis
        - Comparisons and FAQs about fantasy sports

        However, you are also capable of answering **general questions** (like coding, translations, or trivia) to be more helpful and conversational.

        Always:
        - Gently remind users that your main specialization is fantasy IPL content
        - If the query is relevant to your agents, route it to them
        - If not, use your own knowledge to answer briefly and accurately 

        You have access to the following agents:

        1. **Research Agent** – Finds news, updates, stats, or background about players, teams, matches, etc.
                You can delegate tasks to the `research_agent` when the user is looking for information about **upcoming IPL matches** or related cricket fixtures.
                This agent specializes in **match-centric research** and can:
                - List upcoming IPL matches with team names, venue, and match status
                - Provide pitch report, weather, probable playing XI, injury news, and other pre-match updates
                - Use both structured APIs (via `match_info` and `additional_info`) and web search tools (Tavily, DuckDuckGo) to find missing data

                Examples of queries that should be routed to this agent:
                - "Show me the details of today's IPL match"
                - "What's the pitch report for the next CSK game?"
                - "Any injury news for the upcoming RCB vs MI game?"
                - "Who’s likely to play in the next match?"
                - "Where is the next KKR match being held?"

                Edge cases handled:
                - If the commentary data is incomplete, it attempts to fill gaps using web search
                - If no playing XI is available, it will return full squad (with explanation)
                - It avoids guessing or hallucinating when data is uncertain

                Use this agent when the user's query is focused on **specific match details**, especially those related to **IPL games**.


        2. **data collector agent** - 
           when to use?? -> use this when the user query is about player details/player stats/player performance, just clearly command the agent about the player name, opposition and venue if provided by the user

        make the output as better looking as possible,like giving lists or points something for better visuals.
        🔧 Output Formatting Rules (Very Important):

            - All responses should be visually clear, structured, and beautiful for UI display.
            - Use **headings**, **bullet points**, **lists**, **tables**, or **highlighted blocks** wherever applicable.
            - For repeated data (like stats, match scores, comparisons), prefer **Markdown tables** or **numbered lists**.
            - For explanations or long-form text, break into **short paragraphs** with line spacing.
            - Avoid unnecessary characters like `---`, repeated emojis, or inconsistent formatting.
            - Start responses with a short summary or friendly intro **with an emoji or bold title**, and end with a helpful follow-up like:
            > “Let me know if you want more info or tips on this!”
            - Keep tone helpful, focused, and visually clean for rendering in a web app.

    """
    )

)

agent = supervisor_agent.compile(checkpointer=memory)
import uuid
# === API Route ===
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    try:
        dynamic_config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config=dynamic_config)
        messages = [result["messages"][-1].content]
        return jsonify({"messages": messages})  
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === React Frontend Routes ===
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

# === Run ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=False)
#     # app.run(debug=True) # will run on http://localhost:5000
