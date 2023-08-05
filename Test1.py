

def solution(numbers, target):
    n = len(numbers)
    answer = 0

    def dfs(idx, result):
        if idx == n:
            if result == target:
                nonlocal answer
                answer += 1
            return
        else:
            dfs(idx+1, result+numbers[idx])
            dfs(idx+1, result-numbers[idx])

    dfs(0, 0)

    return answer


print(solution([4, 1, 2, 1], 4))

pla_dic = {key: i for key, i in enumerate([5, 2, 3, 4, 5])}

print(pla_dic)

visited = [False for i in range(5)]
print(visited)