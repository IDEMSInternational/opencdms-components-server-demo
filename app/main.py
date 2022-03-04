from base64 import b64decode
import importlib
import os
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI

app = FastAPI(
    title="OpenCDMS Components Api",
    version="1.0.0",
)


@app.get("/")
def status_check():
    return {"Status": "Running"}


@app.get("/exec")
def exec_test():
    # Function as string to be executed (converted via https://www.base64decode.org/ )
    code_b64 = "ZGVmIG1haW4oKToKICAgIHJldHVybiAiVGVzdCBzdWNjZXNzZnVsIg=="
    res = exec_code(code_b64, "main")
    return res


@ app.post("/exec")
def exec_post(py_code_b64: str, fn_name='main'):
    res = exec_code(py_code_b64, fn_name)
    return res


def exec_code(code_b64: str, fn_name='main'):
    task_id = uuid4()

    mod_path = f"app/modules/{task_id}.py"
    code = b64decode(code_b64).decode('utf-8')
    # Write function to module file
    with open(mod_path, "w") as file:
        file.write(code)

    mod = importlib.import_module(f"app.modules.{task_id}")
    if hasattr(mod, fn_name):
        fn = getattr(mod, fn_name)
        res = fn()
        os.remove(mod_path)
        return res

# TODO - add fallback if not found

    # (alternatives)
    # res1 = eval(mycode)
    # res2 = exec(mycode)

# Adapted from https://python.hotexamples.com/examples/importlib/-/find_spec/python-find_spec-function-examples.html
