import random
import time
# benchmarking (small scale) insert than sort VS insert into sorted
def insert_then_sort(top_scores, worker_results):
    start_time = time.time()
    merged = top_scores + worker_results
    merged = sorted(merged)
    merged_trimmed = merged[:1000]
    end_time = time.time()
    print("appending and sorting took", end_time - start_time)

    return merged_trimmed

def sort_in_order(top_scores, worker_results):
    start_time = time.time()
    copy = list(top_scores)
    for result in worker_results:
        # place each dock score in its proper position in top_scores
        for i in range(len(top_scores) - 1):
            if top_scores[i] <= result:
                if top_scores[i + 1] >= result:
                    

def main():
    worker_results = [random.randint(0, 5000) for i in range(10000)]
    top_scores_a = [random.randint(0, 10000) for i in range(1000)]
    top_scores_b = [random.randint(0, 10000) for i in range(1000)]
    top_scores_a.sort()
    top_scores_b.sort()

    insert_then_sort(top_scores_a, worker_results)

if __name__ == "__main__":
    main()
