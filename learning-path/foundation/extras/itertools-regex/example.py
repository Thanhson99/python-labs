"""itertools + regex practical sample."""

import itertools
import re


if __name__ == "__main__":
    tokens = ["user_1", "bad-token", "event_22", "x"]
    valid = [tok for tok in tokens if re.match(r"^[a-z]+_\d+$", tok)]
    pairs = list(itertools.combinations(valid, 2))
    print({"valid": valid, "pairs": pairs})
