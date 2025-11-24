
import time
import numpy as np
import pandas as pd
from sklearn.datasets import (
    make_blobs,
    load_iris,
    load_wine,
    load_breast_cancer,
    load_digits,
    fetch_olivetti_faces,
)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_dists



def gonzalez_k_centers(X, k, rng_seed=None):
    n = X.shape[0]
    k = min(k, n)
    if k <= 0:
        return []

    rng = np.random.default_rng(rng_seed)
    centers_idx = []
    first = int(rng.integers(0, n))
    centers_idx.append(first)
    dists = np.linalg.norm(X - X[first], axis=1) #euclidean distance
    
    for _ in range(1, k):
        idx = int(np.argmax(dists))
        centers_idx.append(idx)
        newd = np.linalg.norm(X - X[idx], axis=1)
        dists = np.minimum(dists, newd)
        
        
        
    cost = float(np.max(dists))
    return centers_idx


def k_center_cost(X, centers_idx):
    if len(centers_idx) == 0:
        return float("inf")
    centers = X[centers_idx]
    dists = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
    nearest = np.min(dists, axis=1)
    return float(np.max(nearest))


def hochbaum_shmoys(X, k):
    dists = pairwise_dists(X)
    n = len(dists)
    all_dists = np.unique(dists)
    all_dists = all_dists[all_dists > 0] 

    low, high = 0, len(all_dists) - 1
    radius = all_dists[-1]
    final_centers = None

    while low <= high:
        mid = (low + high) // 2
        R = all_dists[mid]
        adj = []
        for i in range(n):
            neigh = np.where(dists[i] <= R)[0]
            neigh = neigh[neigh != i]  
            adj.append(set(neigh))

        uncovered = set(range(n))
        centers = []    

        while uncovered:
            v = next(iter(uncovered))
            centers.append(v)
            uncovered.discard(v)
            for u in adj[v]:
                uncovered.discard(u)

        if len(centers) <= k:
            radius = R
            final_centers = centers[:k]
            high = mid - 1 
        else:
            low = mid + 1

    return final_centers, radius


def run_experiments(datasets, k_list, rng_seed=0, save_csv="/mnt/data/kcenter_results.csv"):

    rows = []
    for name, X in datasets:
        Xs = StandardScaler().fit_transform(X)
        n_samples, n_features = Xs.shape
        for k in k_list:
            t0 = time.perf_counter()
            centers_idx = gonzalez_k_centers(Xs, k, rng_seed)
            t1 = time.perf_counter()
            selection_time = t1 - t0
            t2 = time.perf_counter()
            cost = k_center_cost(Xs, centers_idx)
            t3 = time.perf_counter()
            cost_time = t3 - t2

            rows.append({
                "dataset": name,
                "n_samples": n_samples,
                "n_features": n_features,
                "k": k,
                "num_centers": len(centers_idx),
                "cost": cost,
                "selection_time_s": selection_time,
                "cost_time_s": cost_time,
                "centers_idx_sample": ",".join(map(str, centers_idx[:10]))  # show up to 10 indices
            })


    df = pd.DataFrame(rows).sort_values(["dataset", "k"]).reset_index(drop=True)
    try:
        df.to_csv(save_csv, index=False)
        print(f"\nResults saved to: {save_csv}")
    except Exception as e:
        print(f"\nWarning: could not save CSV: {e}")

    return df


if __name__ == "__main__":
    datasets = []
    
    X_toy, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.6, random_state=42)
    datasets.append(("toy_blobs", X_toy))

    iris = load_iris(); datasets.append(("iris", iris.data))
    wine = load_wine(); datasets.append(("wine", wine.data))
    breast = load_breast_cancer(); datasets.append(("breast_cancer", breast.data))
    digits = load_digits(); datasets.append(("digits", digits.data))

    try:
        olivetti = fetch_olivetti_faces()
        datasets.append(("olivetti_faces", olivetti.data))
    except Exception:
        X_syn, _ = make_blobs(n_samples=400, centers=8, cluster_std=1.2, random_state=7)
        datasets.append(("synthetic_400", X_syn))

    k_list = [1, 3, 5, 10]

    results_df = run_experiments(datasets, k_list, rng_seed=0, save_csv="kcenter_results.csv")

    # # Print summary table
    # print("\nSummary (first 20 rows):")
    # print(results_df.head(20).to_string(index=False))

