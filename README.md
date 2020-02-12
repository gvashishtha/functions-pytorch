---
page_type: sample
languages:
- python
- html
products:
- azure
description: "Make machine learning predictions with TensorFlow and Azure Functions"
urlFragment: functions-python-tensorflow-tutorial
---

# Make machine learning predictions with PyTorch and Azure Functions

## Run locally

### Activate virtualenv 

1. `cd start`
1. `python -m venv .venv`
1. `source .venv/bin/activate`

### Initialize function app

1. `func init --worker-runtime python`
1. `func new --name classify --template "HTTP trigger"`

### Copy resources into the classify folder, assuming you run these commands from start

1. `cp ../resources/model/* classify`
1. `cp ../resources/predict.py classify`
1. Add the following dependencies to start/requirements.txt:

```bash
torch>=1.4
numpy==1.15.4
requests
```
1. Install dependencies with `pip install --no-cache-dir -r requirements.txt`

### Update the function to run predictions

1. Add an import statement to `classify/__init__.py`

```{py}
import logging
import json
import azure.functions as func

from .predict import predict

```

1. Replace the entire contents of the `main` function with the following code:

```{py}
def main(req: func.HttpRequest) -> func.HttpResponse:
    
    msg = req.params.get('message')
    logging.info(f'Message received {msg}')
    if not msg:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            msg = req_body.get('message')

    if msg:
        results = predict(msg)
        results = results[0][1]
        logging.info(f'results is {results}')

        headers = {
            "Content-type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }

        return func.HttpResponse(json.dumps(results), headers = headers)
    else:
        return func.HttpResponse(
             "Please pass a message on the query string or in the request body",
             status_code=400
        )

```

### Run the local function

1. Run `func start` from within the start folder with the virtual environment activated.
1. Run `http://localhost:7071/api/classify?message=thisisatest`

## License

See [LICENSE](LICENSE).

## Contributing

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
  
