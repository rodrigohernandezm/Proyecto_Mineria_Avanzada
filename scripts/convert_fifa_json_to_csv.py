import json
import csv
from pathlib import Path

input_path = Path("fifa_ranking_men_2026_07_08.json")
output_csv = Path("fifa_ranking_men_2026_07_08.csv")

with input_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for item in data.get("Results", []):
    team_name = ""
    team_names = item.get("TeamName", [])
    if team_names and isinstance(team_names, list):
        team_name = team_names[0].get("Description", "")

    rows.append(
        {
            "rank": item.get("Rank"),
            "prev_rank": item.get("PrevRank"),
            "ranking_movement": item.get("RankingMovement"),
            "team": team_name,
            "country_code": item.get("IdCountry"),
            "confederation": item.get("ConfederationName"),
            "total_points": (
                round(float(item.get("TotalPoints", 0)), 3)
                if item.get("TotalPoints") is not None
                else ""
            ),
            "prev_points": (
                round(float(item.get("PrevPoints", 0)), 3)
                if item.get("PrevPoints") is not None
                else ""
            ),
            "rated_matches": item.get("RatedMatches"),
            "id_team": item.get("IdTeam"),
            "id_confederation": item.get("IdConfederation"),
            "gender": item.get("Gender"),
            "ranking_status": item.get("RankingStatus"),
        }
    )

headers = [
    "rank",
    "prev_rank",
    "ranking_movement",
    "team",
    "country_code",
    "confederation",
    "total_points",
    "prev_points",
    "rated_matches",
    "id_team",
    "id_confederation",
    "gender",
    "ranking_status",
]

with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV creado correctamente: {output_csv}")
print(f"Filas exportadas: {len(rows)}")
