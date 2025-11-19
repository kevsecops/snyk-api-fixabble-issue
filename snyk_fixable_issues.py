import requests
import json

# --- CONFIGURATION ---
# Replace with your actual API Token
API_TOKEN = "YOUR_SNYK_API_TOKEN"

# Replace with the specific URL for your project/org issues
# Example: "https://api.snyk.io/rest/orgs/{ORG_ID}/issues?version=2024-01-23&limit=50"
BASE_URL = "https://api.snyk.io/rest/orgs/{ORG_ID}/issues?version=2024-01-23&limit=50"

HEADERS = {
    "Authorization": f"token {API_TOKEN}",
    "Accept": "application/vnd.api+json"
}

def check_fixability(issue):
    """
    Analyzes the 'coordinates' inside the issue attributes
    to determine if any fix method is available.
    """
    attributes = issue.get("attributes", {})
    coordinates = attributes.get("coordinates", [])
    
    fix_details = {
        "is_fixable": False,
        "methods": []
    }

    for coord in coordinates:
        # We check all boolean flags provided in your schema
        if coord.get("is_fixable_snyk"):
            fix_details["methods"].append("Snyk Fix")
        if coord.get("is_upgradeable"):
            fix_details["methods"].append("Upgradeable")
        if coord.get("is_patchable"):
            fix_details["methods"].append("Patchable")
        if coord.get("is_pinnable"):
            fix_details["methods"].append("Pinnable")
        if coord.get("is_fixable_upstream"):
            fix_details["methods"].append("Upstream Fix")
            
    if fix_details["methods"]:
        fix_details["is_fixable"] = True
        # Remove duplicates from list
        fix_details["methods"] = list(set(fix_details["methods"]))
        
    return fix_details

def get_fixable_issues(url):
    fixable_issues = []
    
    print(f"Fetching issues from: {url}...")
    
    while url:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            payload = response.json()
            
            # The 'data' field contains the list of issues
            issues_list = payload.get("data", [])
            
            for issue in issues_list:
                analysis = check_fixability(issue)
                
                if analysis["is_fixable"]:
                    attributes = issue.get("attributes", {})
                    
                    # Create a simplified object for the report
                    report_item = {
                        "id": issue.get("id"),
                        "title": attributes.get("title"),
                        "severity": attributes.get("effective_severity_level"),
                        "type": attributes.get("type"),
                        "fix_methods": analysis["methods"]
                    }
                    fixable_issues.append(report_item)

            # Handle Pagination (links.next) as per schema
            links = payload.get("links", {})
            next_link = links.get("next")
            
            if next_link:
                # Usually 'next' is a full URL or a path string. 
                # If it's a dictionary with 'href', extract it (per schema "ONE OF")
                if isinstance(next_link, dict) and "href" in next_link:
                    url = "https://api.snyk.io" + next_link["href"] if next_link["href"].startswith("/") else next_link["href"]
                elif isinstance(next_link, str):
                    url = "https://api.snyk.io" + next_link if next_link.startswith("/") else next_link
                else:
                    url = None
            else:
                url = None
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

    return fixable_issues

# --- EXECUTION ---
if __name__ == "__main__":
    results = get_fixable_issues(BASE_URL)
    
    print(f"\nFound {len(results)} fixable issues:\n")
    print(f"{'SEVERITY':<10} | {'TYPE':<10} | {'TITLE':<50} | {'FIX METHODS'}")
    print("-" * 100)
    
    for item in results:
        methods_str = ", ".join(item['fix_methods'])
        print(f"{item['severity']:<10} | {item['type']:<10} | {item['title'][:47]+'...':<50} | {methods_str}")
