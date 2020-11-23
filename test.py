a = list(input().split())
b = list(input().split())
c = list(input().split())
ans = ''
for j in set([int(a[i]) for i in range(len(a))] + [int(b[i]) for i in range(len(b))] + [int(c[i]) for i in range(len(c))]):
    ans+= str(j) + ' '
print(ans)
