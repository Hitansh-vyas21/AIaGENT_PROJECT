import os
import textwrap
import google.generativeai as genai

# -----------------------------
# CONFIGURATION
# -----------------------------

API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SUPPORTED_EXTENSIONS = (".py", ".java", ".js", ".c", ".cpp")

# -----------------------------
# PROMPT TEMPLATE
# -----------------------------

REVIEW_PROMPT = """
You are an expert software engineer and code reviewer.

Review the following project files and provide:
1. Bugs or errors
2. Code quality issues
3. Optimization suggestions
4. Best practices
5. Overall project feedback

Explain in simple language.

Project Code:
{code}
"""

# -----------------------------
# READ FOLDER FILES
# -----------------------------

def read_code_from_folder(folder_path: str) -> str:
    """
    Reads all supported code files from a folder.
    """
    project_code = ""

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(SUPPORTED_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        project_code += f"\n\n--- File: {file} ---\n"
                        project_code += f.read()
                except Exception as e:
                    project_code += f"\n\n--- File: {file} ---\nError reading file: {e}"

    return project_code

# -----------------------------
# AI REVIEW FUNCTION
# -----------------------------

def review_project(code_text: str) -> str:
    """
    Sends project code to Gemini for review.
    """
    prompt = REVIEW_PROMPT.format(code=code_text)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during AI review: {e}"

# -----------------------------
# DISPLAY OUTPUT
# -----------------------------

def display_review(review: str):
    print("\n" + "=" * 70)
    print("AUTOMATIC AI PROJECT CODE REVIEW")
    print("=" * 70 + "\n")

    wrapped = textwrap.fill(review, width=90)
    print(wrapped)

    print("\n" + "=" * 70)
    print("END OF REVIEW")
    print("=" * 70)

# -----------------------------
# MAIN FUNCTION
# -----------------------------

def main():
    print("=" * 70)
    print("AI AUTOMATIC CODE REVIEWER (FOLDER MODE)")
    print("=" * 70)

    folder_path = input("\nEnter project folder path: ").strip()

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    print("\nReading project files...")
    project_code = read_code_from_folder(folder_path)

    if not project_code.strip():
        print("No supported code files found.")
        return

    print("Reviewing project using Gemini 2.5 Flash...\n")
    review_result = review_project(project_code)
    display_review(review_result)

# -----------------------------
# ENTRY POINT
# -----------------------------

if __name__ == "__main__":
    main()