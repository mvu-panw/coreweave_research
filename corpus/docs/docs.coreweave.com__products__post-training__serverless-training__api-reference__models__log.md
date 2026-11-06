# Log

Source: https://docs.coreweave.com/products/post-training/serverless-training/api-reference/models/log

# Log

> Log trajectories and calculate metrics.



## OpenAPI

````yaml products/post-training/serverless-training/api-reference/openapi.json POST /v1/preview/models/{model_id}/log
openapi: 3.1.0
info:
  title: Serverless Training
  version: 1.0.0
servers:
  - url: https://forge.coreweave.com/api/training
security: []
paths:
  /v1/preview/models/{model_id}/log:
    post:
      tags:
        - models
      summary: Log
      description: Log trajectories and calculate metrics.
      operationId: log_v1_preview_models__model_id__log_post
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
              $ref: '#/components/schemas/LogRequest'
      responses:
        '200':
          description: Successful Response
          content:
            application/json:
              schema: {}
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
    LogRequest:
      properties:
        split:
          type: string
          title: Split
        trajectory_groups:
          items:
            $ref: '#/components/schemas/TrajectoryGroup'
          type: array
          title: Trajectory Groups
      type: object
      required:
        - split
        - trajectory_groups
      title: LogRequest
      description: Schema for logging trajectories.
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: '#/components/schemas/ValidationError'
          type: array
          title: Detail
      type: object
      title: HTTPValidationError
    TrajectoryGroup:
      properties:
        trajectories:
          items:
            $ref: '#/components/schemas/Trajectory'
          type: array
          title: Trajectories
        exceptions:
          items:
            $ref: '#/components/schemas/PydanticException'
          type: array
          title: Exceptions
        metadata:
          additionalProperties: true
          type: object
          title: Metadata
        metrics:
          additionalProperties:
            anyOf:
              - type: number
              - type: integer
              - type: boolean
          type: object
          title: Metrics
        logs:
          items:
            type: string
          type: array
          title: Logs
      type: object
      title: TrajectoryGroup
      description: ART trajectory group, including exchange and group-level state.
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
    Trajectory:
      properties:
        exchanges:
          additionalProperties: true
          type: object
          title: Exchanges
        messages_and_choices:
          items:
            anyOf:
              - $ref: '#/components/schemas/ChatCompletionDeveloperMessageParam'
              - $ref: '#/components/schemas/ChatCompletionSystemMessageParam'
              - $ref: '#/components/schemas/ChatCompletionUserMessageParam'
              - $ref: '#/components/schemas/ChatCompletionAssistantMessageParam'
              - $ref: '#/components/schemas/ChatCompletionToolMessageParam'
              - $ref: '#/components/schemas/ChatCompletionFunctionMessageParam'
              - $ref: '#/components/schemas/Choice'
          type: array
          title: Messages And Choices
        tools:
          anyOf:
            - items:
                $ref: '#/components/schemas/ChatCompletionFunctionToolParam'
              type: array
            - type: 'null'
          title: Tools
        additional_histories:
          items:
            $ref: '#/components/schemas/LegacyHistory'
          type: array
          title: Additional Histories
        reward:
          type: number
          title: Reward
          default: 0
        initial_policy_version:
          anyOf:
            - type: integer
            - type: 'null'
          title: Initial Policy Version
        final_policy_version:
          anyOf:
            - type: integer
            - type: 'null'
          title: Final Policy Version
        metrics:
          additionalProperties:
            anyOf:
              - type: number
              - type: integer
              - type: boolean
          type: object
          title: Metrics
        metadata:
          additionalProperties: true
          type: object
          title: Metadata
        logs:
          items:
            type: string
          type: array
          title: Logs
        start_time:
          type: string
          format: date-time
          title: Start Time
      additionalProperties: true
      type: object
      title: Trajectory
      description: Preserve trajectory fields added by newer ART producers.
    PydanticException:
      properties:
        type:
          type: string
          title: Type
        message:
          type: string
          title: Message
        traceback:
          type: string
          title: Traceback
      type: object
      required:
        - type
        - message
        - traceback
      title: PydanticException
    ChatCompletionDeveloperMessageParam:
      properties:
        content:
          anyOf:
            - type: string
            - items:
                $ref: '#/components/schemas/ChatCompletionContentPartTextParam'
              type: array
          title: Content
        role:
          type: string
          const: developer
          title: Role
        name:
          type: string
          title: Name
      additionalProperties: true
      type: object
      required:
        - content
        - role
      title: ChatCompletionDeveloperMessageParam
      description: >-
        Developer-provided instructions that the model should follow, regardless
        of

        messages sent by the user. With o1 models and newer, `developer`
        messages

        replace the previous `system` messages.
    ChatCompletionSystemMessageParam:
      properties:
        content:
          anyOf:
            - type: string
            - items:
                $ref: '#/components/schemas/ChatCompletionContentPartTextParam'
              type: array
          title: Content
        role:
          type: string
          const: system
          title: Role
        name:
          type: string
          title: Name
      additionalProperties: true
      type: object
      required:
        - content
        - role
      title: ChatCompletionSystemMessageParam
      description: >-
        Developer-provided instructions that the model should follow, regardless
        of

        messages sent by the user. With o1 models and newer, use `developer`
        messages

        for this purpose instead.
    ChatCompletionUserMessageParam:
      properties:
        content:
          anyOf:
            - type: string
            - items:
                anyOf:
                  - $ref: '#/components/schemas/ChatCompletionContentPartTextParam'
                  - $ref: '#/components/schemas/ChatCompletionContentPartImageParam'
                  - $ref: >-
                      #/components/schemas/ChatCompletionContentPartInputAudioParam
                  - $ref: '#/components/schemas/File'
              type: array
          title: Content
        role:
          type: string
          const: user
          title: Role
        name:
          type: string
          title: Name
      additionalProperties: true
      type: object
      required:
        - content
        - role
      title: ChatCompletionUserMessageParam
      description: |-
        Messages sent by an end user, containing prompts or additional context
        information.
    ChatCompletionAssistantMessageParam:
      properties:
        role:
          type: string
          const: assistant
          title: Role
        audio:
          anyOf:
            - $ref: '#/components/schemas/Audio'
            - type: 'null'
        content:
          anyOf:
            - type: string
            - items:
                anyOf:
                  - $ref: '#/components/schemas/ChatCompletionContentPartTextParam'
                  - $ref: '#/components/schemas/ChatCompletionContentPartRefusalParam'
              type: array
            - type: 'null'
          title: Content
        function_call:
          anyOf:
            - $ref: '#/components/schemas/FunctionCall'
            - type: 'null'
        name:
          type: string
          title: Name
        refusal:
          anyOf:
            - type: string
            - type: 'null'
          title: Refusal
        tool_calls:
          items:
            anyOf:
              - $ref: >-
                  #/components/schemas/ChatCompletionMessageFunctionToolCallParam
              - $ref: '#/components/schemas/ChatCompletionMessageCustomToolCallParam'
          type: array
          title: Tool Calls
      additionalProperties: true
      type: object
      required:
        - role
      title: ChatCompletionAssistantMessageParam
      description: Messages sent by the model in response to user messages.
    ChatCompletionToolMessageParam:
      properties:
        content:
          anyOf:
            - type: string
            - items:
                $ref: '#/components/schemas/ChatCompletionContentPartTextParam'
              type: array
          title: Content
        role:
          type: string
          const: tool
          title: Role
        tool_call_id:
          type: string
          title: Tool Call Id
      additionalProperties: true
      type: object
      required:
        - content
        - role
        - tool_call_id
      title: ChatCompletionToolMessageParam
    ChatCompletionFunctionMessageParam:
      properties:
        content:
          anyOf:
            - type: string
            - type: 'null'
          title: Content
        name:
          type: string
          title: Name
        role:
          type: string
          const: function
          title: Role
      additionalProperties: true
      type: object
      required:
        - content
        - name
        - role
      title: ChatCompletionFunctionMessageParam
    Choice:
      properties:
        finish_reason:
          type: string
          enum:
            - stop
            - length
            - tool_calls
            - content_filter
            - function_call
          title: Finish Reason
        index:
          type: integer
          title: Index
        logprobs:
          anyOf:
            - $ref: '#/components/schemas/ChoiceLogprobs'
            - type: 'null'
        message:
          $ref: '#/components/schemas/ChatCompletionMessage'
      additionalProperties: true
      type: object
      required:
        - finish_reason
        - index
        - message
      title: Choice
    ChatCompletionFunctionToolParam:
      properties:
        function:
          $ref: '#/components/schemas/FunctionDefinition'
        type:
          type: string
          const: function
          title: Type
      additionalProperties: true
      type: object
      required:
        - function
        - type
      title: ChatCompletionFunctionToolParam
      description: A function tool that can be used to generate a response.
    LegacyHistory:
      properties:
        messages_and_choices:
          items:
            anyOf:
              - $ref: '#/components/schemas/ChatCompletionDeveloperMessageParam'
              - $ref: '#/components/schemas/ChatCompletionSystemMessageParam'
              - $ref: '#/components/schemas/ChatCompletionUserMessageParam'
              - $ref: '#/components/schemas/ChatCompletionAssistantMessageParam'
              - $ref: '#/components/schemas/ChatCompletionToolMessageParam'
              - $ref: '#/components/schemas/ChatCompletionFunctionMessageParam'
              - $ref: '#/components/schemas/Choice'
          type: array
          title: Messages And Choices
        tools:
          anyOf:
            - items:
                $ref: '#/components/schemas/ChatCompletionFunctionToolParam'
              type: array
            - type: 'null'
          title: Tools
      type: object
      required:
        - messages_and_choices
      title: LegacyHistory
    ChatCompletionContentPartTextParam:
      properties:
        text:
          type: string
          title: Text
        type:
          type: string
          const: text
          title: Type
      type: object
      required:
        - text
        - type
      title: ChatCompletionContentPartTextParam
      description: >-
        Learn about [text
        inputs](https://platform.openai.com/docs/guides/text-generation).
    ChatCompletionContentPartImageParam:
      properties:
        image_url:
          $ref: '#/components/schemas/ImageURL'
        type:
          type: string
          const: image_url
          title: Type
      additionalProperties: true
      type: object
      required:
        - image_url
        - type
      title: ChatCompletionContentPartImageParam
      description: >-
        Learn about [image
        inputs](https://platform.openai.com/docs/guides/vision).
    ChatCompletionContentPartInputAudioParam:
      properties:
        input_audio:
          $ref: '#/components/schemas/InputAudio'
        type:
          type: string
          const: input_audio
          title: Type
      additionalProperties: true
      type: object
      required:
        - input_audio
        - type
      title: ChatCompletionContentPartInputAudioParam
      description: >-
        Learn about [audio
        inputs](https://platform.openai.com/docs/guides/audio).
    File:
      properties:
        file:
          $ref: '#/components/schemas/FileFile'
        type:
          type: string
          const: file
          title: Type
      additionalProperties: true
      type: object
      required:
        - file
        - type
      title: File
      description: >-
        Learn about [file inputs](https://platform.openai.com/docs/guides/text)
        for text generation.
    Audio:
      properties:
        id:
          type: string
          title: Id
      additionalProperties: true
      type: object
      required:
        - id
      title: Audio
      description: |-
        Data about a previous audio response from the model.
        [Learn more](https://platform.openai.com/docs/guides/audio).
    ChatCompletionContentPartRefusalParam:
      properties:
        refusal:
          type: string
          title: Refusal
        type:
          type: string
          const: refusal
          title: Type
      additionalProperties: true
      type: object
      required:
        - refusal
        - type
      title: ChatCompletionContentPartRefusalParam
    FunctionCall:
      properties:
        arguments:
          type: string
          title: Arguments
        name:
          type: string
          title: Name
      additionalProperties: true
      type: object
      required:
        - arguments
        - name
      title: FunctionCall
      description: >-
        Deprecated and replaced by `tool_calls`.


        The name and arguments of a function that should be called, as generated
        by the model.
    ChatCompletionMessageFunctionToolCallParam:
      properties:
        id:
          type: string
          title: Id
        function:
          $ref: '#/components/schemas/Function'
        type:
          type: string
          const: function
          title: Type
      additionalProperties: true
      type: object
      required:
        - id
        - function
        - type
      title: ChatCompletionMessageFunctionToolCallParam
      description: A call to a function tool created by the model.
    ChatCompletionMessageCustomToolCallParam:
      properties:
        id:
          type: string
          title: Id
        custom:
          $ref: '#/components/schemas/Custom'
        type:
          type: string
          const: custom
          title: Type
      additionalProperties: true
      type: object
      required:
        - id
        - custom
        - type
      title: ChatCompletionMessageCustomToolCallParam
      description: A call to a custom tool created by the model.
    ChoiceLogprobs:
      properties:
        content:
          anyOf:
            - items:
                $ref: '#/components/schemas/ChatCompletionTokenLogprob'
              type: array
            - type: 'null'
          title: Content
        refusal:
          anyOf:
            - items:
                $ref: '#/components/schemas/ChatCompletionTokenLogprob'
              type: array
            - type: 'null'
          title: Refusal
      additionalProperties: true
      type: object
      title: ChoiceLogprobs
      description: Log probability information for the choice.
    ChatCompletionMessage:
      properties:
        content:
          anyOf:
            - type: string
            - type: 'null'
          title: Content
        refusal:
          anyOf:
            - type: string
            - type: 'null'
          title: Refusal
        role:
          type: string
          const: assistant
          title: Role
        annotations:
          anyOf:
            - items:
                $ref: '#/components/schemas/Annotation'
              type: array
            - type: 'null'
          title: Annotations
        audio:
          anyOf:
            - $ref: '#/components/schemas/ChatCompletionAudio'
            - type: 'null'
        function_call:
          anyOf:
            - $ref: '#/components/schemas/FunctionCall'
            - type: 'null'
        tool_calls:
          anyOf:
            - items:
                anyOf:
                  - $ref: '#/components/schemas/ChatCompletionMessageFunctionToolCall'
                  - $ref: '#/components/schemas/ChatCompletionMessageCustomToolCall'
              type: array
            - type: 'null'
          title: Tool Calls
      additionalProperties: true
      type: object
      required:
        - role
      title: ChatCompletionMessage
      description: A chat completion message generated by the model.
    FunctionDefinition:
      properties:
        name:
          type: string
          title: Name
        description:
          type: string
          title: Description
        parameters:
          additionalProperties: true
          type: object
          title: Parameters
        strict:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Strict
      additionalProperties: true
      type: object
      required:
        - name
      title: FunctionDefinition
    ImageURL:
      properties:
        url:
          type: string
          title: Url
        detail:
          type: string
          enum:
            - auto
            - low
            - high
          title: Detail
      additionalProperties: true
      type: object
      required:
        - url
      title: ImageURL
    InputAudio:
      properties:
        data:
          type: string
          title: Data
        format:
          type: string
          enum:
            - wav
            - mp3
          title: Format
      additionalProperties: true
      type: object
      required:
        - data
        - format
      title: InputAudio
    FileFile:
      properties:
        file_data:
          type: string
          title: File Data
        file_id:
          type: string
          title: File Id
        filename:
          type: string
          title: Filename
      additionalProperties: true
      type: object
      title: FileFile
    Function:
      properties:
        arguments:
          type: string
          title: Arguments
        name:
          type: string
          title: Name
      additionalProperties: true
      type: object
      required:
        - arguments
        - name
      title: Function
      description: The function that the model called.
    Custom:
      properties:
        input:
          type: string
          title: Input
        name:
          type: string
          title: Name
      additionalProperties: true
      type: object
      required:
        - input
        - name
      title: Custom
      description: The custom tool that the model called.
    ChatCompletionTokenLogprob:
      properties:
        token:
          type: string
          title: Token
        bytes:
          anyOf:
            - items:
                type: integer
              type: array
            - type: 'null'
          title: Bytes
        logprob:
          type: number
          title: Logprob
        top_logprobs:
          items:
            $ref: '#/components/schemas/TopLogprob'
          type: array
          title: Top Logprobs
      additionalProperties: true
      type: object
      required:
        - token
        - logprob
        - top_logprobs
      title: ChatCompletionTokenLogprob
    Annotation:
      properties:
        type:
          type: string
          const: url_citation
          title: Type
        url_citation:
          $ref: '#/components/schemas/AnnotationURLCitation'
      additionalProperties: true
      type: object
      required:
        - type
        - url_citation
      title: Annotation
      description: A URL citation when using web search.
    ChatCompletionAudio:
      properties:
        id:
          type: string
          title: Id
        data:
          type: string
          title: Data
        expires_at:
          type: integer
          title: Expires At
        transcript:
          type: string
          title: Transcript
      additionalProperties: true
      type: object
      required:
        - id
        - data
        - expires_at
        - transcript
      title: ChatCompletionAudio
      description: >-
        If the audio output modality is requested, this object contains data

        about the audio response from the model. [Learn
        more](https://platform.openai.com/docs/guides/audio).
    ChatCompletionMessageFunctionToolCall:
      properties:
        id:
          type: string
          title: Id
        function:
          $ref: '#/components/schemas/Function'
        type:
          type: string
          const: function
          title: Type
      additionalProperties: true
      type: object
      required:
        - id
        - function
        - type
      title: ChatCompletionMessageFunctionToolCall
      description: A call to a function tool created by the model.
    ChatCompletionMessageCustomToolCall:
      properties:
        id:
          type: string
          title: Id
        custom:
          $ref: '#/components/schemas/Custom'
        type:
          type: string
          const: custom
          title: Type
      additionalProperties: true
      type: object
      required:
        - id
        - custom
        - type
      title: ChatCompletionMessageCustomToolCall
      description: A call to a custom tool created by the model.
    TopLogprob:
      properties:
        token:
          type: string
          title: Token
        bytes:
          anyOf:
            - items:
                type: integer
              type: array
            - type: 'null'
          title: Bytes
        logprob:
          type: number
          title: Logprob
      additionalProperties: true
      type: object
      required:
        - token
        - logprob
      title: TopLogprob
    AnnotationURLCitation:
      properties:
        end_index:
          type: integer
          title: End Index
        start_index:
          type: integer
          title: Start Index
        title:
          type: string
          title: Title
        url:
          type: string
          title: Url
      additionalProperties: true
      type: object
      required:
        - end_index
        - start_index
        - title
        - url
      title: AnnotationURLCitation
      description: A URL citation when using web search.
  securitySchemes:
    HTTPBearer:
      type: http
      scheme: bearer

````
