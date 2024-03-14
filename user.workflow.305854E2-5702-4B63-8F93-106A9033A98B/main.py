import sys
import requests
import json
import os

api = os.environ.get("API_KEY")
team = os.environ.get("TEAM_ID")



# Replace with your Linear API key
API_KEY = api

# Replace with your Linear team ID
TEAM_ID = team

def create_issue(title):
    url = f"https://api.linear.app/graphql"
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }
    query = """
        mutation CreateIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                issue {
                    id
                    title
                }
            }
        }
    """
    variables = {
        "input": {
            "teamId": TEAM_ID,
            "title": title
        }
    }
    payload = {"query": query, "variables": variables}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def main(query):
    title = query
    result = create_issue(title)
    issue = result["data"]["issueCreate"]["issue"]
    issue_url = f"https://linear.app/team/{TEAM_ID}/issue/{issue['id']}"
    sys.stderr.write(f"New issue created: {issue['title']} ({issue_url})")

query = sys.argv[1]
main(query)