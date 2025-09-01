import requests
from bs4 import BeautifulSoup
from typing import Dict, Any , Optional, List 
import time

# def get_opp_venue_stats(player_id: int, role_type: str, opposition_id: Optional[int] = None, venue_id: Optional[int] = None) -> Dict[str, Dict[str, Any]]:
#     """
#     Fetches filtered career stats for a given player,
#     optionally restricted to a specific opposition or venue.

#     Args:
#         player_id (int): ESPNcricinfo player ID.
#         role_type (str): One of 'batting', 'bowling', or 'allround'.
#         opposition_id (Optional[int]): If provided, filter stats vs the given opposition.
#         venue_id (Optional[int]): If provided, filter stats at the given ground.
#                                   (Cannot use both together; opposition takes precedence if set.)

#     Returns:
#         Dict[str, Dict[str, Any]]:
#           - If role_type == 'batsman', returns:
#                 {
#                 "Batting": {
#                     "Matches": int,
#                     "Innings": int,
#                     "Runs": int,
#                     "Balls": int,
#                     "Outs": int,
#                     "4s": int,
#                     "6s": int,
#                     "50s": int,
#                     "100s": int,
#                     "SR": float,
#                     "Avg": float
#                     }
#                 }
#           - If role_type == 'bowling', returns:
#                 {
#                 "Bowling": {
#                     "Matches": int,
#                     "innings": int,
#                     "Overs": float,
#                     "Maidens": int,
#                     "Runs": int,
#                     "Wkts": int,
#                     "Eco": float,
#                     "Avg": float,
#                     "SR": float
#                     }
#                 }
#           - If role_type == 'allround', returns:
#                 {
#                   "Batting": {…batting fields…},
#                   "Bowling": {…bowling fields…}
#                 }

#     Raises:
#         ValueError: If role_type is invalid or filtered row not found.
#         RuntimeError: If the “Career averages” table cannot be located.
#     """
#     role_type = role_type.lower()
#     if role_type not in ("batting", "bowling", "allround"):
#         raise ValueError("role_type must be 'batting', 'bowling' or 'allround'")

#     def fetch_filtered_row(role_type: str) -> list:
#         """Fetches the 'filtered' stats row for a player and role."""
#         url = f"https://stats.espncricinfo.com/ci/engine/player/{player_id}.html"
#         params = {"class": 6, "template": "results", "type": role_type}
#         # Apply opposition or venue filter
#         if opposition_id is not None:
#             params["opposition"] = opposition_id
#         elif venue_id is not None:
#             params["ground"] = venue_id

#         headers={"User-Agent": "Mozilla/5.0"}
#         resp = requests.get(url, params = params, headers = headers)
#         resp.raise_for_status()
#         soup = BeautifulSoup(resp.text, "html.parser")

#         # Locate the <table> with caption containing "Career averages"
#         target_table = None
#         for tbl in soup.find_all("table", class_="engineTable"):
#             cap = tbl.find("caption")
#             if cap and "Career averages" in cap.text:
#                 target_table = tbl
#                 break

#         if not target_table:
#             raise RuntimeError("Career averages table not found")

#         # Within that table, find the <tr> whose first cell is "filtered"
#         for row in target_table.find_all("tr"):
#             cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
#             if cells and cells[0].lower() == "filtered":
#                 return cells

#         raise ValueError(f"Filtered row not found for {role_type} (opposition={opposition_id}, venue={venue_id})")

#     def parse_batting(cells: list) -> Dict[str, Dict[str, Any]]:
#         """Parses batting stats from the filtered row."""
#         return {
#             "Batting": {
#                 "Matches": int(cells[2]),
#                 "Innings": int(cells[3]),
#                 "Runs": int(cells[5]),
#                 "Balls": int(cells[8]),
#                 "Outs": int(cells[3]) - int(cells[4]),  # Inns - NO
#                 "4s": int(cells[13]),
#                 "6s": int(cells[14]),
#                 "50s": int(cells[11]),
#                 "100s": int(cells[10]),
#                 "SR": float(cells[9]),
#                 "Avg": float(cells[7])
#                 }
#             }

#     def parse_bowling(cells: list) -> Dict[str, Any]:
#         """Parses bowling stats from the filtered row."""
#         overs_txt = cells[4]
#         overs = float(overs_txt) if overs_txt != "-" else 0.0
#         whole_overs = int(overs)
#         fraction = overs - whole_overs
#         balls = whole_overs * 6 + round(fraction * 10)
#         wickets = int(cells[7])

#         avg_val = float(cells[9]) if cells[9] != "-" else None
#         econ_val = float(cells[10]) if cells[10] != "-" else None
#         sr_val = round(balls / wickets, 2) if wickets else None

#         return {
#             "Bowling": {
#                 "Matches": int(cells[2]),
#                 "innings": int(cells[3]),
#                 "Overs": overs,
#                 "Maidens": int(cells[5]),
#                 "Runs": int(cells[6]),
#                 "Wkts": wickets,
#                 "Eco": econ_val,
#                 "Avg": avg_val,
#                 "SR": sr_val
#                 }
#             }

#     # Branch based on role_type
#     if role_type == "batting":
#         batting_cells = fetch_filtered_row("batting")
#         return parse_batting(batting_cells)

#     elif role_type == "bowling":
#         bowling_cells = fetch_filtered_row("bowling")
#         return parse_bowling(bowling_cells)

#     else:  # role_type == "allround"
#         batting_cells = fetch_filtered_row("batting")
#         bowling_cells = fetch_filtered_row("bowling")
#         result_batting = parse_batting(batting_cells)
#         result_bowling = parse_bowling(bowling_cells)
#         return {
#             "Batting": result_batting["Batting"],
#             "Bowling": result_bowling["Bowling"]
#         }

# print(get_opp_venue_stats(player_id = 625371, role_type= "allround", venue_id= 713))
def fetch_stats(url: str, headers: dict) -> dict:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
       return {}
    return response.json()

def fetch_response(url: str) -> dict:
    headers={"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
       return {}
    return response

def get_espn_player_id(player_name: str) -> Optional[int]:
    """
    Given a player's name (partial or full), performs a Bing search
    specifically targeting ESPNcricinfo’s “cricketers” pages. Parses the
    search results to find the first matching URL of the form
    "espncricinfo.com/cricketers/<name>-<id>" and returns that numeric ID.

    Returns:
        int: The extracted ESPNcricinfo player ID if found.
        None: If the HTTP response is not 200 or if no matching player URL
              appears in the search results.
    """
    query = f"{player_name} site:espncricinfo.com/cricketers"
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    response = fetch_response(url)
    
    # Looking for ESPNcricinfo player URL
    match = re.search(r"espncricinfo\.com/cricketers/[^/]+-(\d+)", response.text)
    if match:
        player_id = match.group(1)
        return player_id
    return None 

def player_stats(player_details: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Computes a player's form profile by aggregating T20 stats in 3 scopes:
    (1) overall last 8 innings, (2) vs a specific opposition, and (3) at a specific venue.

    Args:
        player_details (List[Dict[str, str]]): List of player metadata dicts.
            Each dict contain:
              - name (str): Full player name (e.g., "virat kohli")
              - role (str): Player's primary role (e.g., "batsman", "bowler", etc.)
              - is_wicketkeeper (str): "True"/"False"
              - is_overseas (str): "True"/"False"
              - batting_style (str): e.g., "Right-hand-Batsman"
              - bowling_style (str): e.g., "Right-arm-Medium"
              - opposition (str): Opponent team name (e.g., "kolkata")
        venue_name (str): Venue name (e.g., "eden")

    Returns:
        List[Dict[str, Any]]: One summary dict per player in the format:
            {
              "player name": <str>,
              "role": <str>,
              "is_wicketkeeper": <str>,
              "is_overseas": <str>,
              "batting_style": <str>,
              "bowling_style": <str>,
              "opposition": <str>,
              "recent_stats": [
                {
                  "title": "last_8_innings_stats",
                  "data": { ... }
                },
                {
                  "title": "career_stats_vs_<Opposition>",
                  "data": { ... }
                },
                {
                  "title": "career_stats_at_<Venue>",
                  "data": { ... }
                }
              ]
            }
    """
    
    results = []

    for detail in player_details:
        name = detail.get("name", "").strip()
        opposition = detail.get("opposition", "").strip()
        venue_name = detail.get("venue","").strip()
        role = detail.get("role", "").strip().lower()
        is_wk = detail.get("is_wicketkeeper", "")
        is_overseas = detail.get("is_overseas", "")
        batting_style = detail.get("batting_style", "")
        bowling_style = detail.get("bowling_style", "")

        # Retry logic for resolving player ID
        player_id = None
        err = "Unknown error"
        for attempt in range(10):
            try:
                player_id = get_espn_player_id(name)
                if player_id is not None:
                    break  # Success
            except Exception as e:
                err = str(e)
            time.sleep(0.25)

        if player_id is None:
            results.append({"name": name, "error": f"Could not resolve ID after 10 attempts. Last error: {err}"})
            continue

        # Resolve opposition and venue IDs using the given dict of opposition and venue names with their ids
        if opposition:
            opposition_id = resolve_to_id(opposition, opposition_ids)
        if venue_name:
            venue_id = resolve_to_id(venue_name, venue_ids)

        if "batsman" in role: # wk-batsman, batsman
            role_type = "batting" # It is a parameter in the url
        elif "wk-batsman" in role: # wk-batsman
            role_type = "batting"
        elif "bowler" in role: # bowler
            role_type = "bowling"
        else:
            role_type = "allround" # batting allrounder, bowling allrounder

        overall_stats_dict = get_recent_stats(player_id = player_id, role_type = role_type)
        opp_stats_dict = get_opp_venue_stats(player_id = player_id, opposition_id = opposition_id, venue_id = None, role_type = role_type)
        venue_stats_dict = get_opp_venue_stats(player_id = player_id, opposition_id = None, venue_id = venue_id, role_type = role_type)

        player_summary = combine_recent_stats(
            name, role, overall_stats_dict, opp_stats_dict, venue_stats_dict,
            opposition, venue_name, is_wk, is_overseas, batting_style, bowling_style
        )
        results.append(player_summary)

    return results