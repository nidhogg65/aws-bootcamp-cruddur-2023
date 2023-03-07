# Week 2 — Distributed Tracing

## Technical Tasks

### Instrument AWS X-Ray into backend flask application

### Create a group
```
aws xray create-group --group-name "Cruddur" --filter-expression "service(\"backend-flask\")"
```

### Create a sampling rule source json
```
{
    "SamplingRule": {
        "RuleName": "Cruddur",
        "ResourceARN": "*",
        "Priority": 9000,
        "FixedRate": 0.1,
        "ReservoirSize": 5,
        "ServiceName": "backend-flask",
        "ServiceType": "*",
        "Host": "*",
        "HTTPMethod": "*",
        "URLPath": "*",
        "Version": 1
    }
}
```

### Create a sampling rule itself
```
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```

### Add Deamon Service to Docker Compose
```
xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-east-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```

We need to add these two env vars to our backend-flask in our `docker-compose.yml` file

```
AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```

After running the Cruddur with x-ray daemon, I did a couple of requests. As a result the traces were gathered, sent to AWS and displayed in AWS CloudWatch X-Ray traces panel.

![image](https://user-images.githubusercontent.com/25799157/223406004-e2923dfa-2b40-4408-809e-a8867cf9aed1.png)

### Instrument X-Ray to Notifications Activities endpoint
I added parent and nested child subsegments in `notifications_activities.py`.

```
# Start a parent subsegment
parent_subsegment = xray_recorder.begin_subsegment('notifications_activities')
parent_subsegment.put_annotation('URI', '/api/activities/notifications')

now = datetime.now(timezone.utc).astimezone()

# Start a child subsegment
child_subsegment = xray_recorder.begin_subsegment('returning_mock_data')

======Mock Data=====

xray_dict = {'number': len(results)}
child_subsegment.put_metadata('notification results', xray_dict)

# End a parent subsegment
xray_recorder.end_subsegment()
# End a child subsegment
xray_recorder.end_subsegment()
```

After calling that endpoint, I could see the traces in AWS CloudWatch X-Ray traces panel.

![image](https://user-images.githubusercontent.com/25799157/223445566-58252aa9-b70d-41e3-8d64-61643529f104.png)

### Implement CloudWatch Logs
After adding `watchtower` dependency to `requirements.txt` file, I configured logger to use AWS CloudWatch in `app.py`.

```
# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("This is Cruddur app!!!")
```
```
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
```
I also passed the required env vars in `docker-compose.yaml`

```
AWS_DEFAULT_REGION: "${AWS_DEFAULT_REGION}"
AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
```

As a result, after calling the `/api/activities/home`, I could see the logs in AWS CloudWatch.

![image](https://user-images.githubusercontent.com/25799157/223474122-c47c9136-bac8-4ace-80a3-4e1158b0b728.png)

### Rollbar
To initialize Rollbar I added this lines to `app.py`.

```
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
```

Added env var in `docker-compose.yaml`.

```
ROLLBAR_ACCESS_TOKEN: "${ROLLBAR_ACCESS_TOKEN}"
```

As a result, after an exception happens in the code, I can see in Rollbar UI.

![image](https://user-images.githubusercontent.com/25799157/223503761-596466e7-14a1-4117-9136-624365c7a486.png)
