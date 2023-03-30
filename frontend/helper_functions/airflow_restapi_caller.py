from typing import Any
import google.auth
from google.auth.transport.requests import AuthorizedSession
import requests
from google.oauth2 import service_account

# Path to your JSON key file
KEY_PATH = "frontend/helper_functions/creds.json"

# Scopes to access Google Cloud services
SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]
# Create Credentials object from the JSON key file and scopes
CREDENTIALS = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=SCOPES
)
# Following GCP best practices, these credentials should be
# constructed at start-up time and used throughout
# https://cloud.google.com/apis/docs/client-libraries-best-practices
# AUTH_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
# CREDENTIALS, _ = google.auth.default(scopes=[AUTH_SCOPE])



def make_composer2_web_server_request(url: str, method: str = "GET", **kwargs: Any) -> google.auth.transport.Response:
    """
    Make a request to Cloud Composer 2 environment's web server.
    Args:
      url: The URL to fetch.
      method: The request method to use ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT',
        'PATCH', 'DELETE')
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                  If no timeout is provided, it is set to 90 by default.
    """

    authed_session = AuthorizedSession(CREDENTIALS)

    # Set the default timeout, if missing
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90

    return authed_session.request(method, url, **kwargs)


def trigger_dag(dag_id: str, data: dict) -> str:
    """
    Make a request to trigger a dag using the stable Airflow 2 REST API.
    https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

    Args:
      web_server_url: The URL of the Airflow 2 web server.
      dag_id: The DAG ID.
      data: Additional configuration parameters for the DAG run (json).
    """
    web_server_url = "https://0ba1849854ed4c458db8e34bd91e36dc-dot-us-east1.composer.googleusercontent.com"
    endpoint = f"api/v1/dags/{dag_id}/dagRuns"
    request_url = f"{web_server_url}/{endpoint}"
    json_data = {"conf": data}

    response = make_composer2_web_server_request(
        request_url, method="POST", json=json_data
    )

    if response.status_code == 403:
        raise requests.HTTPError(
            "You do not have a permission to perform this operation. "
            "Check Airflow RBAC roles for your account."
            f"{response.headers} / {response.text}"
        )
    elif response.status_code != 200:
        response.raise_for_status()
    else:
        return response.text


if __name__ == "__main__":

    # TODO(developer): replace with your values
    dag_id = "ad_hoc"  # Replace with the ID of the DAG that you want to run.
    conf= {
        "bucket_name": "goes-team6",
        "file_name": "1680154907.mp3", 
        "file_name_trans" : "1680154907.txt"
    }
    # Replace with configuration parameters for the DAG run.
    # Replace web_server_url with the Airflow web server address. To obtain this
    # URL, run the following command for your environment:
    # gcloud composer environments describe example-environment \
    #  --location=your-composer-region \
    #  --format="value(config.airflowUri)"
    # web_server_url = (
    #     "https://0ba1849854ed4c458db8e34bd91e36dc-dot-us-east1.composer.googleusercontent.com"
    # )

    response_text = trigger_dag(dag_id=dag_id, data=conf
    )

    print(response_text)