import azure.functions as func
import logging
import sys
import importlib.util
from pathlib import Path

blueprint = func.Blueprint()

# Function to load the .pyc file
def load_pyc(pyc_file):
    spec = importlib.util.spec_from_file_location("hello", pyc_file)
    hello = importlib.util.module_from_spec(spec)
    sys.modules["hello"] = hello
    spec.loader.exec_module(hello)
    return hello

# Load the .pyc file
pyc_file = Path("__pycache__") / "hello.cpython-311.pyc"
hello = load_pyc(pyc_file)


@blueprint.route(route="http1", auth_level=func.AuthLevel.ANONYMOUS)
def http1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
        
    hello.main()
    
    return func.HttpResponse(f"Hello there! This HTTP triggered function executed successfully.")

# Register the Blueprint
app = func.FunctionApp()
app.register_functions(blueprint)