def generate_report(algorithms):
    with open("data/report.txt", "w") as f:
        f.write("🔍 Found {} algorithms from Google:\n\n".format(len(algorithms)))

        for i, algo in enumerate(algorithms[:5]):
            f.write(f"{i+1}️⃣ Algorithm from {algo.get('url', 'No URL')}\n")

            # Ensure "code" exists and is a string
            if isinstance(algo.get('code'), str):
                code_snippet = algo['code'][:100]  # Keep the first 100 characters
            else:
                code_snippet = "Code not found or page is documentation only."

            f.write(f"    - Code:\n        {code_snippet}...\n")

            # Convert execution time to float safely
            try:
                time_taken = float(algo.get("time", 0))
            except (ValueError, TypeError):
                time_taken = 0.0

            f.write(f"    - Execution time: {time_taken:.4f}s\n\n")

        # Determine the best algorithm by execution time
        try:
            best_time = float(algorithms[0].get("time", 0))
        except (ValueError, TypeError):
            best_time = 0.0

        f.write(f"✅ Best algorithm: {algorithms[0].get('url', 'No URL')} (Fastest: {best_time:.4f}s)\n")
