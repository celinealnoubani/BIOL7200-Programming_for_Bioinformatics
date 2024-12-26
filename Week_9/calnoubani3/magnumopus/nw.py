#!/usr/bin/env python3

def needleman_wunsch(seq_a: str, seq_b: str, match: int, mismatch: int, gap: int) -> tuple[tuple[str, str], int]:
    # Initialize the scoring matrix
    n = len(seq_a) + 1
    m = len(seq_b) + 1
    score_matrix = [[0] * m for _ in range(n)]
    
    # Initialize gap penalties for first row & column
    for i in range(n):
        score_matrix[i][0] = i * gap
    for j in range(m):
        score_matrix[0][j] = j * gap

    # Fill in the scoring matrix
    for i in range(1, n):
        for j in range(1, m):
            if seq_a[i - 1] == seq_b[j - 1]:
                diag_score = score_matrix[i - 1][j - 1] + match
            else:
                diag_score = score_matrix[i - 1][j - 1] + mismatch
            up_score = score_matrix[i - 1][j] + gap
            left_score = score_matrix[i][j - 1] + gap
            score_matrix[i][j] = max(diag_score, up_score, left_score)

    # Traceback to get the aligned sequences
    aligned_a, aligned_b = "", ""
    i, j = len(seq_a), len(seq_b)
    while i > 0 or j > 0:
        current_score = score_matrix[i][j]
        if i > 0 and j > 0 and (
            (seq_a[i - 1] == seq_b[j - 1] and current_score == score_matrix[i - 1][j - 1] + match) or
            (seq_a[i - 1] != seq_b[j - 1] and current_score == score_matrix[i - 1][j - 1] + mismatch)
        ):
            aligned_a = seq_a[i - 1] + aligned_a
            aligned_b = seq_b[j - 1] + aligned_b
            i -= 1
            j -= 1
        elif i > 0 and current_score == score_matrix[i - 1][j] + gap:
            aligned_a = seq_a[i - 1] + aligned_a
            aligned_b = "-" + aligned_b
            i -= 1
        else:
            aligned_a = "-" + aligned_a
            aligned_b = seq_b[j - 1] + aligned_b
            j -= 1

    # Alignment score is the bottom-right cell in the scoring matrix
    score = score_matrix[-1][-1]
    return (aligned_a, aligned_b), score
