# 📚 Publishing to GitHub - Step by Step Guide

This guide will help you publish your LangGraph Chatbot to GitHub while keeping it synced with Hugging Face Spaces.

## 🎯 Goal

You currently have:
- ✅ App published on Hugging Face Spaces: `https://huggingface.co/spaces/sshibinthomass/Gradio-Chat`

You want to add:
- 🎯 GitHub repository for source code hosting and collaboration

## 📋 Prerequisites

- ✅ Git installed on your machine
- ✅ GitHub account created
- ✅ Git configured with your credentials

## 🚀 Step-by-Step Instructions

### Step 1: Create a New GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `Gradio-Chat` (or your preferred name)
   - **Description**: "Multi-Provider LLM Chatbot powered by LangGraph"
   - **Visibility**: Choose Public or Private
   - **⚠️ DO NOT** initialize with README, .gitignore, or license (you already have these)
4. Click **"Create repository"**
5. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/Gradio-Chat.git`)

### Step 2: Add GitHub as a Remote

Your repository is currently only connected to Hugging Face. Let's add GitHub as well:

```bash
# Navigate to your project directory
cd /Users/qtf4195/Github_Projects/HF-MCP-Hack-Nov/Gradio-Chat

# Add GitHub as a second remote named 'github'
git remote add github https://github.com/YOUR_USERNAME/Gradio-Chat.git

# Verify both remotes
git remote -v
```

You should now see:
```
origin  https://huggingface.co/spaces/sshibinthomass/Gradio-Chat (fetch)
origin  https://huggingface.co/spaces/sshibinthomass/Gradio-Chat (push)
github  https://github.com/YOUR_USERNAME/Gradio-Chat.git (fetch)
github  https://github.com/YOUR_USERNAME/Gradio-Chat.git (push)
```

### Step 3: Stage and Commit Changes

```bash
# Check current status
git status

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Multi-provider LangGraph chatbot with Gradio UI"
```

### Step 4: Push to GitHub

```bash
# Push to GitHub
git push github main
```

If you encounter authentication issues, you may need to:
- Use a Personal Access Token (PAT) instead of password
- Configure SSH keys

### Step 5: Verify on GitHub

1. Go to your GitHub repository URL
2. You should see all your files uploaded
3. The README.md will be displayed on the homepage

## 🔄 Keeping Both Repositories in Sync

### Push to Both Remotes

After making changes, you can push to both Hugging Face and GitHub:

```bash
# Add and commit changes
git add .
git commit -m "Your commit message"

# Push to Hugging Face
git push origin main

# Push to GitHub
git push github main
```

### Or Push to Both at Once

```bash
# Add and commit changes
git add .
git commit -m "Your commit message"

# Push to both remotes
git push origin main && git push github main
```

### Create an Alias (Optional)

To make it easier, create a git alias that pushes to both:

```bash
git config alias.pushall '!git push origin main && git push github main'
```

Now you can just use:
```bash
git pushall
```

## 📝 Important Files to Review Before Publishing

### ✅ Files Already Configured

- ✅ `.gitignore` - Python cache files and .env are ignored
- ✅ `README.md` - Comprehensive documentation
- ✅ `requirements.txt` - All dependencies listed
- ✅ `app.py` - Main application

### ⚠️ Ensure These Are NOT in Git

Check that these sensitive files are ignored:
```bash
# These should NOT appear in git status
.env
__pycache__/
*.pyc
.venv/
```

## 🎨 GitHub Repository Settings

After publishing, customize your GitHub repository:

1. **About Section**:
   - Add description
   - Add topics: `gradio`, `langgraph`, `langchain`, `chatbot`, `llm`
   - Add website URL to your Hugging Face Space

2. **Create Tags/Releases** (optional):
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push github v1.0.0
   ```

3. **Add GitHub Topics**:
   - Go to repository → Settings → Topics
   - Add: `python`, `gradio`, `langgraph`, `ai`, `chatbot`, `groq`, `gemini`, `openai`

## 🔗 Update README Links

Don't forget to update the GitHub link in your README.md:

Replace:
```markdown
- **GitHub Repository**: [Source Code](https://github.com/YOUR_USERNAME/Gradio-Chat)
```

With your actual GitHub username!

## 🎉 You're Done!

Your project is now available on:
- 🤗 **Hugging Face**: For live demo and Space deployment
- 🐙 **GitHub**: For source code, version control, and collaboration

## 💡 Pro Tips

1. **Use Branches**: Create feature branches for new development
   ```bash
   git checkout -b feature/new-provider
   # Make changes
   git commit -m "Add new provider"
   git push github feature/new-provider
   ```

2. **Write Good Commit Messages**: 
   - Use present tense: "Add feature" not "Added feature"
   - Be descriptive: "Add Ollama provider support" instead of "Update code"

3. **Regular Commits**: Commit often, push regularly

4. **Use GitHub Issues**: Track bugs and feature requests

5. **Add GitHub Actions** (advanced): Automate testing or deployment

## 🆘 Troubleshooting

### Authentication Failed?

Use a Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Already Have a GitHub Repo?

If you already created a repository on GitHub, just replace the URL in Step 2.

### Want to Switch Origin?

If you want GitHub to be your primary remote:
```bash
# Rename existing origin to 'huggingface'
git remote rename origin huggingface

# Add GitHub as new origin
git remote add origin https://github.com/YOUR_USERNAME/Gradio-Chat.git

# Push to GitHub
git push -u origin main
```

---

Need help? Open an issue on GitHub or check the [Git documentation](https://git-scm.com/doc).
