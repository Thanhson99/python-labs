def generate_report(algorithms):
    with open("data/report.txt", "w") as f:
        f.write("🔍 Tìm thấy {} thuật toán từ Google:\n\n".format(len(algorithms)))

        for i, algo in enumerate(algorithms[:5]):
            f.write(f"{i+1}️⃣ Thuật toán từ {algo.get('url', 'Không có URL')}\n")

            # Kiểm tra nếu 'code' tồn tại và là chuỗi
            if isinstance(algo.get('code'), str):
                code_snippet = algo['code'][:100]  # Cắt 100 ký tự đầu
            else:
                code_snippet = "Không tìm thấy code hoặc chỉ là tài liệu."

            f.write(f"    - Code:\n        {code_snippet}...\n")

            # Chuyển đổi thời gian thực thi
            try:
                time_taken = float(algo.get("time", 0))
            except (ValueError, TypeError):
                time_taken = 0.0

            f.write(f"    - Thời gian thực thi: {time_taken:.4f}s\n\n")

        # Xác định thuật toán tốt nhất
        try:
            best_time = float(algorithms[0].get("time", 0))
        except (ValueError, TypeError):
            best_time = 0.0

        f.write(f"✅ Thuật toán tốt nhất: {algorithms[0].get('url', 'Không có URL')} (Nhanh nhất: {best_time:.4f}s)\n")
