# Health Check

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/health/health-check

# Health Check



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json GET /v1/health
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/health:
    get:
      tags:
        - health
      summary: Health Check
      operationId: health_check_v1_health_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}

````
