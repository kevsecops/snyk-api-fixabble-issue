# Snyk Fixable Issue Reporter

This Python script connects to the Snyk REST API (v3), processes the raw issue data, and filters the results to report only the vulnerabilities that Snyk has identified as fixable (i.e., issues that can be resolved via upgrade, patch, or an automated Snyk fix).

The script automatically handles pagination, ensuring all issues across your organization/project are retrieved and analyzed.

# Features

API Integration: Fetches issue data from a Snyk REST API endpoint.

Pagination Support: Automatically iterates through links.next to retrieve all pages of issues.

Fixability Filtering: Analyzes the attributes.coordinates to check for flags like is_upgradeable, is_patchable, is_fixable_snyk, and is_fixable_upstream.

Clean Report: Outputs a terminal report summarizing the issue ID, title, severity, type, and the detected fix method(s).

# Prerequisites

You need Python 3.x and the requests library.

pip install requests


# Setup and Configuration

Save the Script: Save the provided Python code as snyk_fixable_issues.py.

Get Your Snyk API Token: You can find your API token in your Snyk account settings.

Configure API Endpoint: You must specify the full URL for the Snyk Issues endpoint, which requires your Organization ID (ORG_ID) and the API version.

Open snyk_fixable_issues.py and update the following variables:

# Replace with your actual API Token
API_TOKEN = "YOUR_SNYK_API_TOKEN"

# Replace with your specific Issues endpoint
# Example structure:
# "[https://api.snyk.io/rest/orgs/](https://api.snyk.io/rest/orgs/){ORG_ID}/issues?version=2024-01-23&limit=50"
BASE_URL = "YOUR_FULL_API_ENDPOINT_URL"


Note: The limit=50 parameter is highly recommended for faster fetching, as the API may default to a lower page size.

# Usage

Run the script from your terminal:

python snyk_fixable_issues.py


# Example Output

The script will first print the URL it is fetching from, and then present a categorized list of fixable issues.

Fetching issues from: [https://api.snyk.io/rest/orgs/a1b2c3d4-..../issues](https://api.snyk.io/rest/orgs/a1b2c3d4-..../issues)?...
----------------------------------------------------------------------------------------------------
Found 12 fixable issues:

SEVERITY   | TYPE       | TITLE                                              | FIX METHODS
-----------|------------|----------------------------------------------------|------------------------
high       | package_vulnerability | Denial of Service in xyz-parser version 1.2.3... | Upgradeable
medium     | code       | Insecure use of temp directory detected...         | Snyk Fix, Manual Fix
low        | package_vulnerability | Weak random number generation in module-a v4.0.0... | Patchable, Pinnable
critical   | package_vulnerability | Remote Code Execution in logger-utils 0.1.0... | Upgradeable
