import os
import sys
import time

import psutil
from pymilvus import connections, Collection

# 初始化milvus
connections.connect(
    alias="new_platform",
    host="localhost",
    port=19530
)

free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 4))+'GB'

print(f"服务器当前可用内存: {free}")
print(f'当前进程占用内存：{psutil.Process(os.getpid()).memory_info().rss/1024/1024/1024:.4f} GB')

print("################################## load connection start ##################################")


entityCollection = Collection("entityCollection", using="new_platform")
entityCollection.load()

time.sleep(3)

print("################################## load connection end ##################################")

print(f"entityCollection占用内存: {sys.getsizeof(entityCollection)/1024/1024} MB")
print(f'当前进程占用内存：{psutil.Process(os.getpid()).memory_info().rss/1024/1024/1024:.4f} GB')

free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 4))+'GB'
print(f"服务器当前可用内存: {free}")
