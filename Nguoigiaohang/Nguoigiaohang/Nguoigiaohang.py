import matplotlib.pyplot as plt
import math

INF = 10**9

# ======================
# NHẬP DỮ LIỆU
# ======================
n = int(input("Nhập số thành phố: "))
print("Nhập ma trận chi phí:")

c = []
for i in range(n):
    row = list(map(int, input(f"Dòng {i+1}: ").split()))
    c.append(row)

visited = [False]*n
best_cost = INF
best_path = []

# tìm cạnh nhỏ nhất
c_min = min(c[i][j] for i in range(n) for j in range(n) if i != j)

# ======================
# TẠO TỌA ĐỘ CÁC THÀNH PHỐ
# ======================
coords = {}
radius = 5

for i in range(n):
    angle = 2*math.pi*i/n
    coords[i] = (
        radius*math.cos(angle),
        radius*math.sin(angle)
    )

plt.ion()
fig, ax = plt.subplots(figsize=(7,7))

# ======================
# HÀM VẼ ĐỒ THỊ
# ======================
def ve_do_thi(current_path=None):

    ax.clear()

    ax.set_title("MÔ PHỎNG BÀI TOÁN TSP - NHÁNH CẬN",
                 fontsize=14, fontweight="bold")

    # vẽ tất cả cạnh
    for i in range(n):
        for j in range(i+1,n):
            ax.plot(
                [coords[i][0],coords[j][0]],
                [coords[i][1],coords[j][1]],
                color="lightgray"
            )

    # vẽ đường đang xét
    if current_path and len(current_path)>1:
        for i in range(len(current_path)-1):
            u=current_path[i]
            v=current_path[i+1]

            ax.plot(
                [coords[u][0],coords[v][0]],
                [coords[u][1],coords[v][1]],
                color="orange",
                linewidth=3
            )

    # vẽ nghiệm tốt nhất
    if best_path:
        route = best_path+[best_path[0]]

        for i in range(len(route)-1):
            u=route[i]
            v=route[i+1]

            ax.plot(
                [coords[u][0],coords[v][0]],
                [coords[u][1],coords[v][1]],
                color="red",
                linewidth=4
            )

    # vẽ thành phố
    for i,(x,y) in coords.items():

        if i==0:
            ax.scatter(x,y,s=350,color="blue")
            ax.text(x,y+0.5,"Kho",ha="center",fontsize=12)

        else:
            ax.scatter(x,y,s=250,color="green")
            ax.text(x,y+0.5,chr(ord('A')+i-1),ha="center")

    # hiển thị thông tin
    if best_path:
        ten=lambda x:"Kho" if x==0 else chr(ord('A')+x-1)
        duong=" → ".join(ten(i) for i in best_path+[best_path[0]])
    else:
        duong="Chưa có"

    ax.text(-6,-6,
        f"Chi phí tốt nhất: {best_cost if best_cost!=INF else '∞'}\n"
        f"Đường đi: {duong}",
        bbox=dict(facecolor="white",alpha=0.9)
    )

    ax.set_xlim(-7,7)
    ax.set_ylim(-7,7)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.pause(0.1)

# ======================
# THUẬT TOÁN NHÁNH CẬN
# ======================
def branch_and_bound(path,cost):

    global best_cost,best_path

    k=len(path)

    bound=cost+(n-k+1)*c_min

    if bound>=best_cost:
        return

    if k==n:

        total=cost+c[path[-1]][path[0]]

        if total<best_cost:

            best_cost=total
            best_path=path[:]

            ve_do_thi(best_path)

        return

    for i in range(n):

        if not visited[i]:

            visited[i]=True
            path.append(i)

            branch_and_bound(
                path,
                cost+c[path[-2]][i]
            )

            path.pop()
            visited[i]=False

# ======================
# CHẠY THUẬT TOÁN
# ======================
visited[0]=True

ve_do_thi([0])

branch_and_bound([0],0)

plt.ioff()
ve_do_thi(best_path)

print("\n===== KẾT QUẢ =====")
print("Đường đi tối ưu:",best_path+[0])
print("Tổng chi phí:",best_cost)

plt.show()