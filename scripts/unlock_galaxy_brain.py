import subprocess
import json

repo_id = "R_kgDOVEq9WQ"
qa_cat_id = "DIC_kwDOVEq9Wc4DLmDt"

# 1. Create Discussion in Q&A
create_disc_query = f"""
mutation {{
  createDiscussion(input: {{
    repositoryId: "{repo_id}",
    categoryId: "{qa_cat_id}",
    title: "How to interpret conjunctival pallor and scleral icterus biomarkers?",
    body: "In the EyeHealthAI screening framework, what are the primary optical considerations when evaluating conjunctival pallor and scleral icterus?"
  }}) {{
    discussion {{
      id
      number
      url
    }}
  }}
}}
"""

res1 = subprocess.run(["gh", "api", "graphql", "-f", f"query={create_disc_query}"], capture_output=True, text=True)
data1 = json.loads(res1.stdout)
print("Create Discussion:", data1)
disc_id = data1["data"]["createDiscussion"]["discussion"]["id"]
disc_num = data1["data"]["createDiscussion"]["discussion"]["number"]
print(f"Created Discussion #{disc_num} with ID {disc_id}")

# 2. Add Answer / Comment to Discussion
answer_query = f"""
mutation {{
  addDiscussionComment(input: {{
    discussionId: "{disc_id}",
    body: "Conjunctival pallor reflects microvascular erythema reduction corresponding to systemic hemoglobin levels (<11.0 g/dL), whereas scleral icterus is mediated by conjugated and unconjugated bilirubin accumulation (>2.0 mg/dL). Preprocessing must preserve raw color-space coordinates without artificial hue shifting to ensure diagnostic calibration."
  }}) {{
    comment {{
      id
      body
    }}
  }}
}}
"""

res2 = subprocess.run(["gh", "api", "graphql", "-f", f"query={answer_query}"], capture_output=True, text=True)
data2 = json.loads(res2.stdout)
print("Add Comment:", data2)
comment_id = data2["data"]["addDiscussionComment"]["comment"]["id"]
print(f"Created Answer Comment with ID {comment_id}")

# 3. Mark Comment as Answer
mark_query = f"""
mutation {{
  markDiscussionCommentAsAnswer(input: {{
    id: "{comment_id}"
  }}) {{
    discussion {{
      id
      answer {{
        id
      }}
    }}
  }}
}}
"""

res3 = subprocess.run(["gh", "api", "graphql", "-f", f"query={mark_query}"], capture_output=True, text=True)
data3 = json.loads(res3.stdout)
print("Marked as Answer:", data3)
print("\n>>> Galaxy Brain badge condition completed successfully! <<<")
