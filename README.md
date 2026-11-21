# Temporary Ollama endpoint for Skales AI

This repository can start a temporary Ollama server on a GitHub Actions hosted runner. Skales connects to it through a temporary Cloudflare Tunnel. The endpoint exists only while the workflow is running.

## One-time setup

1. Open **Settings → Secrets and variables → Actions** in this repository.
2. Select **New repository secret**.
3. Set the name to `OLLAMA_API_KEY`.
4. Set the value to a randomly generated secret with at least 32 characters. Keep it private. Do not put it in source files, issues, or workflow logs.

## Start the AI

1. Open the **Actions** tab.
2. Select **Temporary Ollama Brain for Skales**.
3. Select **Run workflow** on the `main` branch.
4. Wait for the job to install Ollama, download `llama3.2:1b`, start the authenticated gateway, and establish the temporary tunnel.
5. Open the completed setup step's **Summary** to get the Base URL.

## Skales provider settings

- API key: the exact value saved as the `OLLAMA_API_KEY` repository secret
- Base URL: the Base URL shown in the workflow summary (ends with `/v1`)
- Protocol: OpenAI Chat Completions
- Model: `llama3.2:1b`
- Remove any unrelated custom request header, such as `x-litellm-team`

## Important limits and security

- The workflow is manual; it does not run on a schedule.
- GitHub-hosted runners are temporary. This session is configured to stop after about 5 hours 40 minutes. Cancel the workflow to stop it sooner.
- Skales cannot reach Ollama when the workflow is stopped or the runner is recycled. Start a new run and update the Base URL each time because the temporary tunnel address changes.
- The repository is public. Never commit the API key. The gateway checks a Bearer token before forwarding supported OpenAI-compatible requests to Ollama.
- Treat the temporary endpoint as private even though it has an authentication gate. Do not share its URL or API key publicly.
