from ai.jobs_api import search_jobs
import json

jobs = search_jobs("Python Developer")

print(type(jobs))
print()

print(jobs)