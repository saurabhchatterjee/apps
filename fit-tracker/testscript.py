def maxGold(G):
    n = len(G)

    if n == 0:
        return 0

    # Initialize dp such that all entries are set to True.
    dp = [True] * n

    # Iterate through the list of chests G.
    for i in range(n):
        if G[i] == 0:
            # Modify dp based on the values of G[i-1] and G[i+1].
            if 0 < i < n - 1:
                if G[i - 1] < G[i + 1]:
                    dp[i - 1] = False
                else:
                    dp[i + 1] = False
            elif i == 0:
                dp[i + 1] = False
            elif i == n - 1:
                dp[i - 1] = False

    # Iterate over dp and add up the elements from G when dp[i] is True.
    max_gold = sum(G[i] for i in range(n) if dp[i])

    return max_gold


if __name__ == '__main__':
    # Example usage:
    G = [1, 0, 2, 0, 3, 0, 4, 0]
    result = maxGold(G)
    print(result)  # Output: 10

# {% for idx, target in enumerate(form.targets) %}
#             {{ form_macro.form_field(target.calorie_target, with_label=True) }}
#             <h4>Macros</h4>
#             {{ form_macro.form_field(target.fat_target, with_label=True) }}
#             {{ form_macro.form_field(target.protein_target, with_label=True) }}
#             {{ form_macro.form_field(target.carbs_target, with_label=True) }}
#         {% endfor %}
