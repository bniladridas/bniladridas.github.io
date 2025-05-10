# Git Secret Removal Guide

This guide provides step-by-step instructions for removing sensitive information (like API keys, passwords, or credentials) from a Git repository's history.

## Prerequisites

Before you begin, ensure you have:

- Git installed and configured
- Java Runtime Environment (JRE) installed (if using BFG Repo-Cleaner)
- A backup of your repository

## Method 1: Using Git Filter-Branch (What We Used)

This is the method we used to successfully remove the API key from our repository history.

### Step 1: Create a Clean Clone of Your Repository

```bash
# Clone your repository
git clone https://github.com/yourusername/your-repository.git clean-repo
cd clean-repo
```

### Step 2: Create a Script to Replace Sensitive Information

Create a file named `replace-key.sh` with the following content:

```bash
#!/bin/bash

# Set the API key and replacement
API_KEY="YOUR_SENSITIVE_KEY_HERE"
REPLACEMENT="REMOVED_API_KEY"

# Use git filter-branch to replace the API key in all files
git filter-branch --force --tree-filter "find . -type f -exec sed -i '' 's/$API_KEY/$REPLACEMENT/g' {} \;" --prune-empty HEAD

# Clean up the repository
git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "API key has been removed from the repository history."
```

### Step 3: Make the Script Executable and Run It

```bash
chmod +x replace-key.sh
./replace-key.sh
```

### Step 4: Verify the Removal

```bash
# Check if the sensitive information still exists in the history
git log -p | grep "YOUR_SENSITIVE_KEY_HERE"
```

### Step 5: Force Push the Changes

```bash
git push origin --force
```

## Method 2: Using BFG Repo-Cleaner (Alternative Method)

BFG is a faster, simpler alternative to git-filter-branch for cleansing bad data from your Git repository history.

### Step 1: Download BFG Repo-Cleaner

```bash
curl -L -o bfg.jar https://repo1.maven.org/maven2/com/github/rtyley/bfg/1.14.0/bfg-1.14.0.jar
```

### Step 2: Create a Mirror Clone of Your Repository

```bash
git clone --mirror https://github.com/yourusername/your-repository.git repo.git
```

### Step 3: Create a Text File with Patterns to Replace

Create a file named `api-keys.txt` containing the sensitive information:

```
YOUR_SENSITIVE_KEY_HERE
```

### Step 4: Run BFG to Remove Sensitive Information

```bash
java -jar bfg.jar --replace-text api-keys.txt repo.git
```

### Step 5: Clean Up the Repository

```bash
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Step 6: Push the Changes

```bash
git push --force
```

## Best Practices for Preventing Secret Leaks

1. **Use Environment Variables**: Store sensitive information in environment variables instead of hardcoding them.

2. **Add Sensitive Files to .gitignore**: Make sure `.env` files and other files containing secrets are in your `.gitignore`.

3. **Use Secret Management Tools**: Consider using tools like:
   - GitHub Secrets for GitHub Actions
   - Vercel Environment Variables for Vercel deployments
   - AWS Secrets Manager for AWS resources

4. **Implement Pre-commit Hooks**: Use tools like `git-secrets` or `pre-commit` to prevent accidental commits of sensitive information.

5. **Regularly Rotate Credentials**: Even after removing secrets from Git history, consider them compromised and rotate them.

6. **Use Secret Scanning**: GitHub offers secret scanning for private repositories to detect accidentally committed secrets.

## Important Notes

- Even after removing secrets from your Git history, consider them compromised and rotate them.
- Force pushing rewrites history and can cause issues for collaborators. Make sure everyone is aware of the change.
- Always back up your repository before performing history rewriting operations.

## References

- [Git Documentation on filter-branch](https://git-scm.com/docs/git-filter-branch)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
- [GitHub Help: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
