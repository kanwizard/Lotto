import random

count = 5  # 생성할 조합 개수

for i in range(count):
    numbers = sorted(random.sample(range(1, 40), 6))
    print(f"{i+1}번:", numbers)
