"""Utility functions for Azure DevOps Pull Request operations"""

from typing import Dict
from urllib.parse import urlparse
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication


def _parse_pr_url(pr_url: str) -> Dict:
    """
    Parse an Azure DevOps PR URL to extract organization, project, repo, and PR ID.
    
    Supports URL formats:
    - https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{pr_id}
    - https://{org}.visualstudio.com/{project}/_git/{repo}/pullrequest/{pr_id}
    
    Args:
        pr_url: Full URL to the pull request
        
    Returns:
        Dict with organization_url, project, repository, and pull_request_id
    """
    parsed = urlparse(pr_url)
    path_parts = parsed.path.strip("/").split("/")
    
    # Find indices for _git and pullrequest
    git_index = path_parts.index("_git")
    pr_index = path_parts.index("pullrequest")
    
    return {
        "organization_url": f"{parsed.scheme}://{parsed.netloc}",
        "project": path_parts[0],
        "repository": path_parts[git_index + 1],
        "pull_request_id": int(path_parts[pr_index + 1])
    }


def _get_current_user_id(connection: Connection) -> str:
    """
    Get the current authenticated user's ID.
    
    Args:
        connection: Azure DevOps connection
        
    Returns:
        User ID string
    """
    location_client = connection.clients.get_location_client()
    connection_data = location_client.get_connection_data()
    return connection_data.authenticated_user.id


def approve_pr(pr_url: str, pat: str) -> Dict:
    """
    Approve a Pull Request in Azure DevOps.
    
    Args:
        pr_url: URL of the PR (e.g., https://dev.azure.com/org/project/_git/repo/pullrequest/123)
        pat: Personal Access Token with PR approval permissions
    
    Returns:
        Dict with approval status information
    """
    pr_info = _parse_pr_url(pr_url)
    
    credentials = BasicAuthentication("", pat)
    connection = Connection(base_url=pr_info["organization_url"], creds=credentials)
    
    git_client = connection.clients.get_git_client()
    user_id = _get_current_user_id(connection)
    
    # Vote values: 10 = approved, 5 = approved with suggestions, 0 = no vote, -5 = waiting for author, -10 = rejected
    reviewer = {"vote": 10}  # Approved
    
    result = git_client.create_pull_request_reviewer(
        reviewer=reviewer,
        repository_id=pr_info["repository"],
        pull_request_id=pr_info["pull_request_id"],
        reviewer_id=user_id,
        project=pr_info["project"]
    )
    
    return {
        "pull_request_id": pr_info["pull_request_id"],
        "repository": pr_info["repository"],
        "project": pr_info["project"],
        "reviewer_id": user_id,
        "vote": result.vote,
        "status": "approved"
    }


def reset_pr_approval(pr_url: str, pat: str) -> Dict:
    """
    Reset (undo) a Pull Request approval in Azure DevOps.
    Sets the vote back to "no vote" (0).
    
    Args:
        pr_url: URL of the PR (e.g., https://dev.azure.com/org/project/_git/repo/pullrequest/123)
        pat: Personal Access Token with PR approval permissions
    
    Returns:
        Dict with reset status information
    """
    pr_info = _parse_pr_url(pr_url)
    
    credentials = BasicAuthentication("", pat)
    connection = Connection(base_url=pr_info["organization_url"], creds=credentials)
    
    git_client = connection.clients.get_git_client()
    user_id = _get_current_user_id(connection)
    
    # Vote values: 10 = approved, 5 = approved with suggestions, 0 = no vote, -5 = waiting for author, -10 = rejected
    reviewer = {"vote": 0}  # No vote (reset)
    
    result = git_client.create_pull_request_reviewer(
        reviewer=reviewer,
        repository_id=pr_info["repository"],
        pull_request_id=pr_info["pull_request_id"],
        reviewer_id=user_id,
        project=pr_info["project"]
    )
    
    return {
        "pull_request_id": pr_info["pull_request_id"],
        "repository": pr_info["repository"],
        "project": pr_info["project"],
        "reviewer_id": user_id,
        "vote": result.vote,
        "status": "reset"
    }


if __name__ == "__main__":
    # import os
    # from dotenv import load_dotenv
    
    # load_dotenv()
    
    # Example usage
    pr_url = ""
    pat = ""
    
    if pat:
        # Approve PR
        result = approve_pr(pr_url, pat)
        print(f"PR approved: {result}")
        
        # Reset approval
        # result = reset_pr_approval(pr_url, pat)
        # print(f"PR approval reset: {result}")
    else:
        print("Please set ADO_PAT environment variable")
