# Decisions
This document includes details about the implemented and skipped feautures during my development.

## ✅ Features implemented

- **Strong password policy**
    + 8 chars
    + 1 lowercase
    + 1 uppercase
    + 1 number
    + 1 special char
    + Cannot contain username
    + Cannot be a common password

One of my priorities as a developer is cybersecurity. Protecting users confidentiality takes very little time for the benefit in terms of security posture.

- **JWT authentication**

Using JWT avoid storing cookies in the server and allows a secure token workflow.

I decided to keep the folders ```apps/auth/``` and ```apps/users/``` separate. This way the apps organization is based on functionality, as the authentication and user interaction via the API serve two different purposes.

- **Swagger**
    + Running on &rarr; ```/api/docs/```
    + Set the access token in the authorize box like this &rarr; ```Bearer <access_token>```

I decided to use Swagger as an additional documentation resource and, mainly, as a testing tool.

Easy to setup and very useful.

## ❌ Features skipped

- **TaskHistory model**

I believe this added too much workload to the task for the actual benefit it brings.

In addition to this, the tight deadline for the task made me prioritize other functionalities.