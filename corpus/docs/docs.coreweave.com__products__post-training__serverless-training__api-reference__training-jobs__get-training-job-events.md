# Get Training Job Events

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job-events

# Get Training Job Events

> Get events for a training job.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json GET /v1/preview/training-jobs/{training_job_id}/events
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/training-jobs/{training_job_id}/events:
    get:
      tags:
        - training-jobs
      summary: Get Training Job Events
      description: Get events for a training job.
      operationId: >-
        get_training_job_events_v1_preview_training_jobs__training_job_id__events_get
      parameters:
        - name: training_job_id
          in: path
          required: true
          schema:
            type: string
            title: Training Job Id
        - name: after
          in: query
          required: false
          schema:
            type: string
            description: Cursor for pagination
            title: After
          description: Cursor for pagination
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
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: >-
                  #/components/schemas/PaginatedResponse_TrainingJobEventResponse_
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
    PaginatedResponse_TrainingJobEventResponse_:
      properties:
        object:
          type: string
          title: Object
          description: Object type identifier
          default: list
        data:
          items:
            $ref: '#/components/schemas/TrainingJobEventResponse'
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
      title: PaginatedResponse[TrainingJobEventResponse]
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    TrainingJobEventResponse:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        type:
          $ref: '#/components/schemas/TrainingJobEventType'
        data:
          additionalProperties: true
          type: object
          title: Data
      type: object
      required:
        - id
        - type
        - data
      title: TrainingJobEventResponse
      description: Schema for TrainingJobEvent response.
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
    TrainingJobEventType:
      type: string
      enum:
        - training_started
        - gradient_step
        - training_ended
        - training_failed
      title: TrainingJobEventType
      description: Training job event type enumeration.
  securitySchemes:
    HTTPBearer:
      type: http
      scheme: bearer

````
