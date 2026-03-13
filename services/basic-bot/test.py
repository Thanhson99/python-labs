def test_code(code):
    try:
        exec(code)  # Execute code in a controlled local environment
        return "Code executed successfully"
    except Exception as e:
        return f"Error: {str(e)}"

# Test AI-generated code
code_to_test = """
def multiply(a, b):
    return a * b

print(multiply(3, 4))
"""
result = test_code(code_to_test)
print(f"Result: {result}")
