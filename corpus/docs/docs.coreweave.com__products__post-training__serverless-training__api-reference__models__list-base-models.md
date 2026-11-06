# List Base Models

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/list-base-models

# List Base Models

> Models this deployment can train, including architecture validation.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json GET /v1/preview/base-models
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/base-models:
    get:
      tags:
        - models
      summary: List Base Models
      description: Models this deployment can train, including architecture validation.
      operationId: list_base_models_v1_preview_base_models_get
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                items:
                  type: string
                type: array
                title: Response List Base Models V1 Preview Base Models Get

````
