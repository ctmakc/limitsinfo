# Windows Terminal Safety

Use PowerShell for all terminal and background commands in this workspace.

Rules:
- Run one command per step. Do not chain commands with `;`, `&&`, `||`, or unrelated pipes.
- For Python, use `.\venv\Scripts\python.exe` from the workspace root.
- For Git, run separate commands in this order when needed: `git status`, `git add ...`, `git commit -m "..."`, `git push`.
- Prefer non-interactive commands. Avoid commands that wait for hidden prompts.
- If a terminal command shows no output for about 20 seconds, stop, report the exact command, and retry the simplest single-command version in a fresh terminal.
- Use PowerShell quoting rules for Windows paths and commands.
