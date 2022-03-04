import importlib
import os
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI

app = FastAPI()


# https://python.hotexamples.com/examples/importlib/-/find_spec/python-find_spec-function-examples.html


@app.get("/")
def read_root():
    return {"Status": "Running"}

#
# Adapted from https://python.hotexamples.com/examples/importlib/-/find_spec/python-find_spec-function-examples.html


@app.get("/exec")
def exec():
    # Function as string to be executed
    test_fn_string = """def main():
    print('exec  test')
    return 'Test Function Working'"""
    res = exec_code(test_fn_string, "main")
    return res


@ app.post("/exec")
def exec_post(code: str, fn_name='main', ):
    res = exec_code(code, fn_name)
    return res


def exec_code(code_str: str, fn_name='main'):
    task_id = uuid4()

    mod_path = f"app/modules/{task_id}.py"

    # Write function to module file
    with open(mod_path, "w") as file:
        file.write(code_str)

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
