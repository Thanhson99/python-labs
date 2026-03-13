import openai

openai.api_key = "your-openai-api-key"  # Set your API key here

def explain_code(code_snippet):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Please explain the following Python code:\n\n{code_snippet}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Python code example
code_snippet = """
def add(a, b):
    return a + b

result = add(2, 3)
print(result)
"""
explanation = explain_code(code_snippet)
print(f"Explanation: {explanation}")
