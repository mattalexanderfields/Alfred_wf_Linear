import sys
import requests
import json
import os



# Priority mapping
PRIORITY_MAP = {
    "l": 4,
    "m": 3,
    "h": 2,
    "u": 1
}


API_KEY = os.environ.get("API_KEY")
TEAM_ID = os.environ.get("TEAM_ID")


def create_issue(title, priority):
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
                    priority
                }
            }
        }
    """
    variables = {
        "input": {
            "teamId": TEAM_ID,
            "title": title,
            "priority": priority
        }
    }
    payload = {"query": query, "variables": variables}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def main(query, priority):
    title = query
    prio = PRIORITY_MAP.get(priority.lower(), 0)
    result = create_issue(title, prio)
    issue = result["data"]["issueCreate"]["issue"]
    issue_url = f"https://linear.app/team/{TEAM_ID}/issue/{issue['id']}"
    #sys.stdout.write(f"New issue created: {issue['title']} ({issue_url})")


if __name__ == "__main__":
    string_input = sys.argv[1]
    split_string = string_input.split('-')
    query = split_string[0]
    if len(split_string) > 1:
        priority = split_string[1]
    else:
        priority = "None"


    main(query,priority)
