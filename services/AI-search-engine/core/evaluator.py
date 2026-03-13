import timeit

def measure_execution_time(code, setup=""):
    try:
        execution_time = timeit.timeit(code, setup=setup, number=1)
        return execution_time
    except Exception as e:
        return f"Lỗi khi chạy code: {str(e)}"
