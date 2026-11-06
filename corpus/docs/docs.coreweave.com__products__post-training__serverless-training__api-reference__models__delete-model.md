# Delete Model

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/delete-model

# Delete Model

> Delete a model, all its checkpoints, artifacts, and the associated W&B run.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json DELETE /v1/preview/models/{model_id}
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/models/{model_id}:
    delete:
      tags:
        - models
      summary: Delete Model
      description: >-
        Delete a model, all its checkpoints, artifacts, and the associated W&B
        run.
      operationId: delete_model_v1_preview_models__model_id__delete
      parameters:
        - name: model_id
          in: path
          required: true
          schema:
            type: string
            title: Model Id
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteModelResponse'
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
    DeleteModelResponse:
      properties:
        model_id:
          type: string
          format: uuid
          title: Model Id
        deleted_checkpoints:
          type: integer
          title: Deleted Checkpoints
        deleted_run:
          type: boolean
          title: Deleted Run
      type: object
      required:
        - model_id
        - deleted_checkpoints
        - deleted_run
      title: DeleteModelResponse
      description: Schema for delete model response.
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
