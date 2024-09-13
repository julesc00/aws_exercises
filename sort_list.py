from typing import List


sample = [4, 6, 8, 20, 21, 1]

def sort_dataset(dataset: List[int]) -> List[int]:
    return sorted(dataset)


if __name__ == "__main__":
    print(sort_dataset(sample))
