def test_code(code):
    try:
        exec(code)  # Chạy mã trong một môi trường Python an toàn
        return "Code executed successfully"
    except Exception as e:
        return f"Error: {str(e)}"

# Thử nghiệm mã của AI
code_to_test = """
def multiply(a, b):
    return a * b

print(multiply(3, 4))
"""
result = test_code(code_to_test)
print(f"Result: {result}")
