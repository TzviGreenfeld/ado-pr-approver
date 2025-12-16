import os
from typing import Optional
import typer
from pr_utils import approve_pr, reset_pr_approval
from dotenv import load_dotenv

load_dotenv()

def main(
    approve: bool = typer.Option(
        False,
        "--approve",
        help="Approve the Pull Request",
    ),
    reset: bool = typer.Option(
        False,
        "--reset",
        help="Reset your vote on the Pull Request",
    ),
    pr_url: str = typer.Argument(
        ...,
        help="Azure DevOps Pull Request URL (e.g., https://dev.azure.com/org/project/_git/repo/pullrequest/123)",
    ),
    pat: Optional[str] = typer.Argument(
        None,
        help="Personal Access Token (optional, can use ADO_PAT env var)",
    ),
):
    """
    Azure DevOps Pull Request CLI tool.
    
    Approve or reset your vote on a Pull Request.
    
    Examples:
        prhandler --approve <url>
        prhandler --reset <url>
        prhandler --approve <url> <pat>
    """
    # Validate that exactly one action is specified
    if approve == reset:
        typer.echo("Error: You must specify either --approve or --reset (but not both)", err=True)
        raise typer.Exit(code=1)
    
    # Get PAT from argument or environment
    token = pat or os.getenv("ADO_PAT")
    if not token:
        typer.echo("Error: PAT is required. Set ADO_PAT environment variable or provide it as argument.", err=True)
        typer.echo("Get yours from https://msazure.visualstudio.com/_usersSettings/tokens", err=True)
        raise typer.Exit(code=1)
    
    try:
        if approve:
            result = approve_pr(pr_url, token)
            typer.echo(f"✓ PR #{result['pull_request_id']} approved successfully!")
        else:
            result = reset_pr_approval(pr_url, token)
            typer.echo(f"✓ PR #{result['pull_request_id']} vote reset successfully!")
        
        typer.echo(f"  Repository: {result['repository']}")
        typer.echo(f"  Project: {result['project']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

def app():
    typer.run(main)

if __name__ == "__main__":
    app()
