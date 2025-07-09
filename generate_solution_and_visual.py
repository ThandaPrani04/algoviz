import os
import sys
import requests
import json
import time
import subprocess

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

def clean_code_block(code: str) -> str:
    """
    Removes leading and trailing ``` markers and language hints from a code block.
    """
    lines = code.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def extract_sections_and_save(txt_file, cpp_file, manim_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()

    cpp_section = ""
    manim_section = ""

    if "--- C++ Solution ---" in content and "--- Manim Visualization ---" in content:
        cpp_section = content.split("--- C++ Solution ---")[1].split("--- Manim Visualization ---")[0].strip()
        manim_section = content.split("--- Manim Visualization ---")[1].strip()
    else:
        raise RuntimeError("Expected section headers not found in the file.")

    cpp_section = clean_code_block(cpp_section)
    manim_section = clean_code_block(manim_section)

    with open(cpp_file, "w", encoding="utf-8") as f:
        f.write(cpp_section)
    print(f"✅ C++ solution written to: {cpp_file}")

    with open(manim_file, "w", encoding="utf-8") as f:
        f.write(manim_section)
    print(f"✅ Manim script written to: {manim_file}")


def render_manim(manim_py_file, class_name="SolutionVisualization"):
    print("🎬 Rendering Manim animation...")
    subprocess.run([
        "manim", "-pql", manim_py_file, class_name
    ])


def fetch_problem_with_graphql(slug):
    print(f"📥 Fetching problem description for: {slug}")
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        difficulty
        content
      }
    }
    """
    variables = {"titleSlug": slug}
    resp = requests.post(
        LEETCODE_GRAPHQL,
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch problem: HTTP {resp.status_code}")
    data = resp.json()
    q = data.get("data", {}).get("question")
    if not q:
        raise Exception("Problem not found.")
    print(f"✅ Found: {q['title']} [{q['difficulty']}]")
    return q["content"]


def generate_code(problem_text, lang):
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        raise Exception("Please set OPENROUTER_API_KEY in your environment variables.")

    prompt = f"""
You are a competitive programmer and teacher.
Write an efficient solution in {lang} for the following problem.
Output only two sections:
- First section starts with this exact line: --- C++ Solution ---
- Then the full C++ code (no explanation, no comments, just code)
- Then this exact line: --- Manim Visualization ---
- Then the full Manim (Python) code (no explanation, no comments, just code)

Problem description (HTML):
{problem_text}
"""

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
            if resp.status_code == 200:
                response_data = resp.json()
                text = response_data["choices"][0]["message"]["content"]
                return text
            else:
                print(f"⚠️ Attempt {attempt} failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
        time.sleep(5)
    raise Exception("Failed to get response from OpenRouter after 3 attempts.")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <leetcode-problem-url>")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith("https://leetcode.com/problems/"):
        print("Invalid LeetCode problem URL.")
        sys.exit(1)

    slug = url.rstrip("/").split("/")[-1]

    problem_text = fetch_problem_with_graphql(slug)

    print("\n🤖 Generating C++ solution + Manim visualization...")
    result = generate_code(problem_text, lang="C++")

    raw_output = f"{slug}_solution_and_visualization.txt"
    with open(raw_output, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"✅ Raw output written to: {raw_output}")

    cpp_file = f"{slug}_solution.cpp"
    manim_file = f"{slug}_visualization.py"

    extract_sections_and_save(raw_output, cpp_file, manim_file)
    render_manim(manim_file)


if __name__ == "__main__":
    main()
