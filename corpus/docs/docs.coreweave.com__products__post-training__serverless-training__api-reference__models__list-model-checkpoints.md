# List Model Checkpoints

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/list-model-checkpoints

# List Model Checkpoints



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json GET /v1/preview/models/{model_id}/checkpoints
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/models/{model_id}/checkpoints:
    get:
      tags:
        - models
      summary: List Model Checkpoints
      operationId: list_model_checkpoints_v1_preview_models__model_id__checkpoints_get
      parameters:
        - name: model_id
          in: path
          required: true
          schema:
            type: string
            title: Model Id
        - name: after
          in: query
          required: false
          schema:
            type: string
            description: Cursor for pagination - ID of the last item from previous page
            title: After
          description: Cursor for pagination - ID of the last item from previous page
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            maximum: 100
            minimum: 1
            description: Number of items to return
            default: 20
            title: Limit
          description: Number of items to return
        - name: order
          in: query
          required: false
          schema:
            enum:
              - asc
              - desc
            type: string
            description: Sort order
            default: asc
            title: Order
          description: Sort order
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedResponse_CheckpointResponse_'
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
    PaginatedResponse_CheckpointResponse_:
      properties:
        object:
          type: string
          title: Object
          description: Object type identifier
          default: list
        data:
          items:
            $ref: '#/components/schemas/CheckpointResponse'
          type: array
          title: Data
          description: Array of items
        first_id:
          type: string
          title: First Id
          description: ID of the first item in the current page
          default: ''
        last_id:
          type: string
          title: Last Id
          description: ID of the last item in the current page
          default: ''
        has_more:
          type: boolean
          title: Has More
          description: Whether there are more items available
      type: object
      required:
        - data
        - has_more
      title: PaginatedResponse[CheckpointResponse]
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    CheckpointResponse:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        step:
          type: integer
          title: Step
        metrics:
          additionalProperties:
            type: number
          type: object
          title: Metrics
      type: object
      required:
        - id
        - step
        - metrics
      title: CheckpointResponse
      description: Schema for Checkpoint response.
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
