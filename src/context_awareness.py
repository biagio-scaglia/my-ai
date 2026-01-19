import os


class ContextAwareness:
    """
    Mini LSP locale.
    Scansiona il progetto per capire stack, framework e pattern.
    """

    def __init__(self, root_path="."):
        self.root_path = root_path
        self.stack_summary = ""

    def scan_project(self):
        """
        Analizza i file chiave per determinare lo stack.
        """
        tech_stack = []
        frameworks = []

        # Check files
        files = os.listdir(self.root_path)

        if "package.json" in files:
            tech_stack.append("Node.js/JS")
            # TODO: Leggere contenuto per framework precisi (Next, React, Vue)
            frameworks.append("NPM Ecosystem")

        if "requirements.txt" in files or "pyproject.toml" in files:
            tech_stack.append("Python")

        if "Cargo.toml" in files:
            tech_stack.append("Rust")

        if "composer.json" in files:
            tech_stack.append("PHP")

        if "go.mod" in files:
            tech_stack.append("Go")

        # Euristica Framework
        if (
            "app.py" in files
            and "streamlit"
            in open("app.py", "r", encoding="utf-8", errors="ignore").read()
        ):
            frameworks.append("Streamlit")

        if "manage.py" in files:
            frameworks.append("Django")

        self.stack_summary = f"Detected Stack: {', '.join(tech_stack)} | Frameworks: {', '.join(frameworks)}"
        return self.stack_summary

    def get_system_prompt_injection(self):
        """
        Ritorna una stringa da iniettare nel system prompt.
        """
        if not self.stack_summary:
            self.scan_project()

        return f"\n[CONTEXT AWARENESS]\nProject Context: {self.stack_summary}\n(You see the code structure. Don't ask what language is used.)\n"


if __name__ == "__main__":
    c = ContextAwareness()
    print(c.scan_project())
