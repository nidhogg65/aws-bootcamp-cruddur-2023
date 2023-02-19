# Week 0 — Billing and Architecture

## Technical Tasks

### Create an admin IAM user
The admin IAM user had been created before the bootcamp started. However, I didn't have an admin group, so I created it then and added the admin user in there.
![image](https://user-images.githubusercontent.com/25799157/218456482-6902b674-8adc-41c3-bc1e-bb408a37cc3b.png)

### Generate Access Keys for accessing the CLI
The Access Keys have been generated for the admin IAM user.
![image](https://user-images.githubusercontent.com/25799157/219001835-f010faeb-c363-422a-8667-f61cf79747e4.png)

### Install AWS CLI / Use CloudShell
Installed AWS CLI into gitpod CDE, imported Access Keys and managed to connect to AWS using those AWS credentials.
Played around with AWS CLI in gitpod CDE as well as checked out CloudShell in AWS.

### Setup a budget for Cruddur
I setup a budget of 10$ with one alert of 50% threshold using cloud console.
![image](https://user-images.githubusercontent.com/25799157/218746335-e604826b-57a9-4a9e-987d-b4a0a1f36373.png)

### Create a CloudWatch alarm
The Cloudwatch alarm with SNS topic and subscription was setup for exceeding maximum budget (>10$) using cloud console.
![image](https://user-images.githubusercontent.com/25799157/218746720-cac6aa60-d3a7-432e-a1b9-922896a3bc00.png)

### Conceptual Diagram in [LucidChart](https://lucid.app/lucidchart/94542c4a-9da2-4d5a-9b12-7808195b4040/edit?viewport_loc=-478%2C-194%2C2994%2C1437%2C0_0&invitationId=inv_d7579df8-1946-4eb3-aa33-616713a51e95)
![image](https://user-images.githubusercontent.com/25799157/219471164-94dfa309-8e5f-4bc1-a124-d4b5efca0b69.png)

### Logical Diagram in [LucidChart](https://lucid.app/lucidchart/862813c4-2ad0-4fbf-b69c-003064d867ca/edit?viewport_loc=-904%2C-691%2C4992%2C2397%2C0_0&invitationId=inv_a9d827b3-9b20-4a57-93f1-7f4749fa9c88)
![image](https://user-images.githubusercontent.com/25799157/219647745-018a27b0-e4cc-4d8f-b10f-e1edf37fe842.png)

## Challenges

### Use EventBridge to hookup Health Dashboard to SNS and send notification when there is a service health issue
EventBridge rule
![image](https://user-images.githubusercontent.com/25799157/219770369-c203c897-ade5-4bcd-8cc1-fa946314acef.png)
SNS topic
![image](https://user-images.githubusercontent.com/25799157/219770870-dbba5d9c-216b-49a3-9080-f124d8668c9d.png)
Subscription
![image](https://user-images.githubusercontent.com/25799157/219771459-a000775c-faa7-475a-abdc-12f28225895e.png)

### Add MFA for root, IAM user
Added MFA for root account
![image](https://user-images.githubusercontent.com/25799157/219000691-3876176e-477f-4bf0-beb3-14dc02ec4325.png)
Added MFA for admin user
![image](https://user-images.githubusercontent.com/25799157/219001573-b8ca31ab-853a-4c05-94fb-c91b196b4b5f.png)






