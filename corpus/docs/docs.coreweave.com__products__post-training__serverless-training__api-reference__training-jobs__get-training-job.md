# Get Training Job

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/get-training-job

# Get Training Job

> Get a training job by ID.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json GET /v1/preview/training-jobs/{training_job_id}
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/training-jobs/{training_job_id}:
    get:
      tags:
        - training-jobs
      summary: Get Training Job
      description: Get a training job by ID.
      operationId: get_training_job_v1_preview_training_jobs__training_job_id__get
      parameters:
        - name: training_job_id
          in: path
          required: true
          schema:
            type: string
            title: Training Job Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TrainingJobResponse'
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
    TrainingJobResponse:
      properties:
        id:
          type: string
          format: uuid
          title: Id
        model_id:
          type: string
          format: uuid
          title: Model Id
        status:
          $ref: '#/components/schemas/TrainingJobStatus'
        progress:
          anyOf:
            - type: number
            - type: 'null'
          title: Progress
        error_message:
          anyOf:
            - type: string
            - type: 'null'
          title: Error Message
        training_start:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Training Start
        training_end:
          anyOf:
            - type: string
              format: date-time
            - type: 'null'
          title: Training End
        created_at:
          type: string
          format: date-time
          title: Created At
        updated_at:
          type: string
          format: date-time
          title: Updated At
      type: object
      required:
        - id
        - model_id
        - status
        - progress
        - error_message
        - training_start
        - training_end
        - created_at
        - updated_at
      title: TrainingJobResponse
      description: Schema for TrainingJob response.
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    TrainingJobStatus:
      type: string
      enum:
        - PENDING
        - RUNNING
        - COMPLETED
        - FAILED
        - CANCELLED
      title: TrainingJobStatus
      description: Training job status enumeration.
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
