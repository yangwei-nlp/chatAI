"""
删除Milvus的collection
"""

import os

os.chdir("../..")

from pymilvus import utility, connections

connections.connect(
    alias="new_platform",
    host="localhost",
    port=19530,
)

for collection in utility.list_collections(using="new_platform"):
    print(collection)

print("删除后:")

utility.drop_collection("course_doc", using="new_platform")
# utility.drop_collection("resource_doc", using="new_platform")
# utility.drop_collection("curriculum_doc", using="new_platform")
# utility.drop_collection("exercise_doc", using="new_platform")
for collection in utility.list_collections(using="new_platform"):
    print(collection)
