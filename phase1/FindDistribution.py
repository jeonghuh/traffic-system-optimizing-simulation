import pandas as pd
import scipy
import scipy.stats
from scipy.stats import expon


file_path = 'C:/Users/송재민/Desktop/최종데이터.xlsx'


Data_list = []


i = input("Inter-arrival time - 해당하는 개찰구 번호(1~6), Service-time - 7 입력 ")
print()

sheet_name='Sheet'+str(i)

df = pd.read_excel(file_path,sheet_name)

if 1<=int(i)<=6:
    d = df.iloc[:, 2].tolist()

    l_time = []

    for j in range(len(d)):
        t_value = round(int(d[j][0:2]) * 60 + int(d[j][3:5]) + (float(d[j][6:9]) * 0.001), 3)
        l_time.append(t_value)

    for j in range(len(d) - 1):
        t_difference = round(l_time[j + 1] - l_time[j], 3)
        Data_list.append(t_difference)

elif int(i)==7:
    d = df.iloc[:, 0].tolist()

    for i in range(len(d)):
        Data_list.append(float(d[i]))

else:
    print("잘못 입력")
    exit()

Data_list.sort()

print(Data_list)
mean=sum(Data_list)/len(Data_list)
print(mean)

# 최적의 분포에 대한 모수 추정 함수
def estimate_parameters(best_dist, data):
    if best_dist == 'expon':
        params = expon.fit(data, floc=0)
         
    else:
        raise ValueError("Unsupported distribution")

    return params

dist_names = ["expon"]

dist_results = []
params = {}
for dist_name in dist_names :
    dist = getattr(scipy.stats, dist_name)
    param = dist.fit(Data_list)
    params[dist_name] = params
    Stat, p = scipy.stats.kstest(Data_list, dist_name, param)
    dist_results.append((dist_name, p))

print("Distribution")
print(dist_results)
best_dist, best_p = max(dist_results, key=lambda item: item[1])
print("제일 비슷한 분포 : %s" % best_dist)
print("그 분포의 p_value : %f" % best_p)

# 최적의 분포에 대한 모수 출력
params1 = estimate_parameters(best_dist, Data_list)
print("모수 :", params1)
print()