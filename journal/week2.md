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
