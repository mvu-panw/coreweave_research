# Create SFT Training Job

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/training-jobs/create-sft-training-job

# Create SFT Training Job

> Create a new SFT (Supervised Fine-Tuning) training job.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json POST /v1/preview/sft-training-jobs
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/sft-training-jobs:
    post:
      tags:
        - training-jobs
      summary: Create Sft Training Job
      description: Create a new SFT (Supervised Fine-Tuning) training job.
      operationId: Create_SFT_Training_Job_v1_preview_sft_training_jobs_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateSFTTrainingJob'
        required: true
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
    CreateSFTTrainingJob:
      properties:
        model_id:
          type: string
          format: uuid
          title: Model Id
        training_data_url:
          type: string
          title: Training Data Url
          description: >-
            W&B artifact path for training data (e.g.,
            'wandb-artifact:///entity/project/artifact-name:version')
        config:
          anyOf:
            - $ref: '#/components/schemas/SFTTrainingConfig'
            - type: 'null'
        experimental_config:
          anyOf:
            - $ref: '#/components/schemas/SFTExperimentalTrainingConfig'
            - type: 'null'
      additionalProperties: false
      type: object
      required:
        - model_id
        - training_data_url
      title: CreateSFTTrainingJob
      description: >-
        Schema for creating a new SFT (Supervised Fine-Tuning) TrainingJob.


        The client should upload the training data (trajectories.jsonl and
        metadata.json)

        to W&B Artifacts and provide the artifact URL.
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
    SFTTrainingConfig:
      properties:
        batch_size:
          anyOf:
            - type: integer
              maximum: 32
              minimum: 1
            - type: string
              const: auto
            - type: 'null'
          title: Batch Size
        learning_rate:
          anyOf:
            - type: number
            - items:
                type: number
              type: array
            - type: 'null'
          title: Learning Rate
        assistant_turns:
          type: string
          enum:
            - all
            - last
          title: Assistant Turns
          default: all
        metric_logging:
          anyOf:
            - $ref: '#/components/schemas/SFTMetricLoggingConfig'
            - type: 'null'
      additionalProperties: false
      type: object
      title: SFTTrainingConfig
      description: Schema for SFT training config.
    SFTExperimentalTrainingConfig:
      properties: {}
      additionalProperties: false
      type: object
      title: SFTExperimentalTrainingConfig
      description: Reserved SFT experimental config; no fields are currently supported.
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
    SFTMetricLoggingConfig:
      properties:
        enabled:
          type: boolean
          title: Enabled
          default: false
        target_training_step:
          anyOf:
            - type: integer
              exclusiveMinimum: 0
            - type: 'null'
          title: Target Training Step
      additionalProperties: false
      type: object
      title: SFTMetricLoggingConfig
      description: Schema for optional SFT metric logging.
  securitySchemes:
    HTTPBearer:
      type: http
      scheme: bearer

````
