# PR Handler

A simple CLI tool to approve or reset your vote on Azure DevOps Pull Requests.

## Installation

Run the setup script from the project directory:

```powershell
.\setup.ps1
```

This will install all dependencies and set up the `prhandler` command.

## Setup

You need an Azure DevOps Personal Access Token (PAT) with PR approval permissions.

1. Get your PAT from: https://msazure.visualstudio.com/_usersSettings/tokens
2. Either:
   - Set the `ADO_PAT` environment variable, or
   - Pass it as an argument to the command

## Usage

```bash
# Approve a PR
prhandler --approve <pr-url>

# Reset your vote on a PR
prhandler --reset <pr-url>

# Pass PAT as argument (if not using env var)
prhandler --approve <pr-url> <pat>
```

### Examples

```bash
# Approve (using ADO_PAT env var)
prhandler --approve https://dev.azure.com/org/project/_git/repo/pullrequest/123

# Reset vote (using ADO_PAT env var)
prhandler --reset https://dev.azure.com/org/project/_git/repo/pullrequest/123

# Approve with PAT as argument
prhandler --approve https://dev.azure.com/org/project/_git/repo/pullrequest/123 your-pat-token

# Reset vote with PAT as argument
prhandler --reset https://dev.azure.com/org/project/_git/repo/pullrequest/123 your-pat-token
```

## Supported URL Formats

- `https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{pr_id}`
- `https://{org}.visualstudio.com/{project}/_git/{repo}/pullrequest/{pr_id}`
