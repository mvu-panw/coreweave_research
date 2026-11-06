# Create Model

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/create-model

# Create Model

> Create a new model.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json POST /v1/preview/models
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/models:
    post:
      tags:
        - models
      summary: Create Model
      description: Create a new model.
      operationId: create_model_v1_preview_models_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ModelCreate'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ModelResponse'
        '422':
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HTTPValidationError'
      security:
        - HTTPBearer: []
components:
  schemas:
    ModelCreate:
      properties:
        entity:
          anyOf:
            - type: string
            - type: 'null'
          title: Entity
          description: Team or username associated with the supplied W&B credential
          examples:
            - my-team
        project:
          type: string
          title: Project
          description: Project name in W&B where the model will be stored
          examples:
            - my-awesome-project
        name:
          type: string
          title: Name
          description: Unique name for the model within the project
          examples:
            - my-awesome-model
        base_model:
          type: string
          title: Base Model
          description: Base model identifier or HuggingFace model path to fine-tune from
          examples:
            - OpenPipe/Qwen3-14B-Instruct
        return_existing:
          type: boolean
          title: Return Existing
          description: >-
            If true, return existing model if one with the same name already
            exists instead of creating a new one
          default: false
      type: object
      required:
        - project
        - name
        - base_model
      title: ModelCreate
      description: Schema for creating a new Model.
    ModelResponse:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        entity:
          type: string
          title: Entity
        project:
          type: string
          title: Project
        name:
          type: string
          title: Name
        base_model:
          type: string
          title: Base Model
        run_id:
          anyOf:
            - type: string
            - type: 'null'
          title: Run Id
      type: object
      required:
        - id
        - entity
        - project
        - name
        - base_model
      title: ModelResponse
      description: Schema for Model response.
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
  securitySchemes:
    HTTPBearer:
      type: http
      scheme: bearer

````
