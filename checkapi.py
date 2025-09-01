# import requests

# player_names = ["Rishabh pant","Bumrah", "Hardik pandya","shardul thakur","deepak chahar","marco jansen"]  # Replace or loop over more names if needed

# search_headers = {
#     'x-apihub-key': '9HN92wz6l7bberNNuKkhDCXeb4YH4lXo2fIKuVdgCpB82jpHlM',
#     'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
#     'x-apihub-endpoint': 'b0242771-45ea-4c07-be42-a6da38cdec41'
# }

# for name in player_names:
#     id_url = f"https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/browse/player?search={name.replace(' ', '+')}"
#     response = requests.get(id_url, headers=search_headers)
#     print(f"Search response for '{name}':\n")
#     # print(response.json())
#     data = response.json()
#     print(data.get("player", []))  # Print the list of players found


import requests

player_id = "10744"  # Example: Virat Kohli

details_headers = {
    'x-apihub-key': '9HN92wz6l7bberNNuKkhDCXeb4YH4lXo2fIKuVdgCpB82jpHlM',
    'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
    'x-apihub-endpoint': 'a055bf38-0796-4fab-8fe3-6f042f04cdba'
}

details_url = f"https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/browse/player/{player_id}"
response = requests.get(details_url, headers=details_headers)

print(f"Details response for player ID {player_id}:\n")
# print(response.json())
info = response.json()
print(info.get("role", "Unknown").lower())
print(info.get("bat","Unknown"))
print(info.get("bowl", "Unknown"))

if "wk" in info.get("role", "Unknown").lower():
    print("Wicketkeeper")
else:    print("Not a wicketkeeper")
