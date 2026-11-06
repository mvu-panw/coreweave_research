# Delete Model Checkpoints

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/delete-model-checkpoints

# Delete Model Checkpoints

> Delete specific checkpoints for a model.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json DELETE /v1/preview/models/{model_id}/checkpoints
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/models/{model_id}/checkpoints:
    delete:
      tags:
        - models
      summary: Delete Model Checkpoints
      description: Delete specific checkpoints for a model.
      operationId: delete_model_checkpoints_v1_preview_models__model_id__checkpoints_delete
      parameters:
        - name: model_id
          in: path
          required: true
          schema:
            type: string
            title: Model Id
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeleteCheckpointsRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteCheckpointsResponse'
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
    DeleteCheckpointsRequest:
      properties:
        steps:
          items:
            type: integer
          type: array
          title: Steps
      type: object
      required:
        - steps
      title: DeleteCheckpointsRequest
      description: Schema for deleting checkpoints.
    DeleteCheckpointsResponse:
      properties:
        deleted_count:
          type: integer
          title: Deleted Count
        not_found_steps:
          items:
            type: integer
          type: array
          title: Not Found Steps
      type: object
      required:
        - deleted_count
        - not_found_steps
      title: DeleteCheckpointsResponse
      description: Schema for delete checkpoints response.
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
