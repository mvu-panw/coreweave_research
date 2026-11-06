# Create Chat Completion

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/chat-completions/create-chat-completion

# Create Chat Completion

> Create a new chat completion.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json POST /v1/chat/completions
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/chat/completions:
    post:
      tags:
        - chat-completions
      summary: Create Chat Completion
      description: Create a new chat completion.
      operationId: create_chat_completion_v1_chat_completions_post
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ChatCompletionRequest'
        required: true
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChatCompletionResponse'
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
    ChatCompletionRequest:
      properties:
        model:
          type: string
          title: Model
        messages:
          items:
            additionalProperties: true
            type: object
          type: array
          title: Messages
      additionalProperties: true
      type: object
      required:
        - model
        - messages
      title: ChatCompletionRequest
    ChatCompletionResponse:
      properties:
        choices:
          items:
            $ref: '#/components/schemas/ChatChoice'
          type: array
          title: Choices
      additionalProperties: true
      type: object
      title: ChatCompletionResponse
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    ChatChoice:
      properties:
        message:
          anyOf:
            - $ref: '#/components/schemas/ChatMessage'
            - type: 'null'
      additionalProperties: true
      type: object
      title: ChatChoice
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
    ChatMessage:
      properties:
        content:
          title: Content
      additionalProperties: true
      type: object
      title: ChatMessage
  securitySchemes:
    HTTPBearer:
      type: http
      scheme: bearer

````
