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

