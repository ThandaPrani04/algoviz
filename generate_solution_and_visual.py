import os
import sys
import requests
import json
import time
import subprocess
from bs4 import BeautifulSoup

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"


def clean_code_block(code: str) -> str:
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

For the Manim visualization:
- Detect the main data structure involved (array, linked list, tree, graph, etc.) and use the most appropriate Manim objects and layouts for each.
- Ensure all elements are clearly visible, well-aligned, and do not overlap. Use spacing, grouping, and layout strategies (e.g., VGroup, HGroup, arrange, shift, etc.) to avoid overlap and improve clarity.
- Use labels, colors, and arrows to make the visualization easy to understand.
- For graphs, use a layout that avoids edge and node overlap. For linked lists, arrange nodes horizontally or vertically with clear links. For arrays, use rectangles or squares in a row or grid.
- Always use a single class named SolutionVisualization for the Manim code.
- Do not include any explanation or comments, just code.

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


def fetch_top_discussions(slug, num_posts=3):
    """
    Scrapes the top N discussion posts for the given problem slug.
    """
    discussions_url = f"https://leetcode.com/problems/{slug}/discuss/?sort=most_votes"
    print(f"🔍 Fetching discussions from: {discussions_url}")
    resp = requests.get(discussions_url, headers={
        "User-Agent": "Mozilla/5.0"
    })
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch discussions: HTTP {resp.status_code}")
    soup = BeautifulSoup(resp.text, "html.parser")

    posts = []
    for link in soup.select("a.h-5.hover\\:text-blue-s.dark\\:hover\\:text-dark-blue-s")[:num_posts]:
        title = link.text.strip()
        href = link.get("href")
        posts.append(f"- {title}: https://leetcode.com{href}")
    if not posts:
        print("⚠️ No discussion posts found.")
    return "\n".join(posts)


def check_solution_with_discussions(slug, cpp_code):
    """
    Fetches top discussions and asks the LLM to assess correctness of cpp_code.
    """
    discussion_summary = fetch_top_discussions(slug)

    prompt = f"""
You are an expert competitive programmer.

Here is a C++ solution to the following LeetCode problem: {slug}
Please check if it is correct, by comparing it against the ideas and approaches found in the most upvoted discussion posts.

C++ Solution:
{cpp_code}

Most upvoted discussions:
{discussion_summary}

Output only:
- YES if the solution is correct
- NO if incorrect, and a one-line reason why
"""

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        raise Exception("Please set OPENROUTER_API_KEY in your environment variables.")

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

    print("🤖 Asking LLM to validate solution against discussions...")
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
    if resp.status_code == 200:
        response_data = resp.json()
        result = response_data["choices"][0]["message"]["content"]
        print(f"✅ Validation result: {result}")
        return result
    else:
        raise Exception(f"LLM validation failed: {resp.status_code} - {resp.text}")


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

    with open(cpp_file, "r", encoding="utf-8") as f:
        cpp_code = f.read()

    check_solution_with_discussions(slug, cpp_code)
    render_manim(manim_file)


if __name__ == "__main__":
    main()
