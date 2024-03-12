## Using Cross-Origin Resource Sharing (CORS)

Cross-origin resource sharing is a mechanism that allows restricted resources 
on a web page to be requested from another origin (domain outside the domain 
from which the first resource was served).

### Enable CORS in API

To enable CORS in your Connexion API use a Flask extension 
[Flask-Cors](https://flask-cors.readthedocs.io/en/latest/). 
Update the application factory function where you define your APP to set CORS 
headers:

```
from flask_cors import CORS

app = connexion.App(...)
app.add_api(...)

# add CORS support
CORS(app.app)
```

See Connexion [CORS Support](https://connexion.readthedocs.io/en/latest/cookbook.html#cors-support) 
documentation.

### CORS with Endpoints

Allow CORS by setting `'allowCors': True` under `x-google-endpoints` in 
the swagger.json spec that you deploy to GCE. You may need to update related 
code in our `deploy_endpoints.sh` script.

See the documentation [Adding CORS support](https://cloud.google.com/endpoints/docs/openapi/specify-esp-v2-startup-options#cors).
