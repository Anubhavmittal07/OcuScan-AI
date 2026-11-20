import subprocess
import json

query = """
query {
  repository(owner: "Sarthak752008", name: "Eye-Diseases-healthai-research") {
    id
    discussionCategories(first: 10) {
      nodes {
        id
        name
        isAnswerable
      }
    }
  }
}
"""

res = subprocess.run(["gh", "api", "graphql", "-f", f"query={query}"], capture_output=True, text=True)
print("OUT:", res.stdout)
if res.stderr:
    print("ERR:", res.stderr)
