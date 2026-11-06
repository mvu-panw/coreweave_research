# Get deployment parameters

Source: https://docs.coreweave.com/products/inference/reference/api-overview/deploymentservice/get-deployment-parameters

# Get deployment parameters

> Enumerate the available gateways, runtime engines, and instance types for deployment creation.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

The response includes:

* `gatewayIds`: gateway IDs in the caller's organization
  that can be referenced by a new deployment.
* `runtimeParameters.runtimeEngineOptions`: runtime options
  grouped by engine name and version. Each version lists
  configuration options, environment variables, and its
  lifecycle state.
* `resourceParameters.instanceTypes`: instance types
  available for deployment.

```bash title="Example request" theme={"system"}
curl -X GET https://api.coreweave.com/v1alpha1/inference/deployments/parameters \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml get /v1alpha1/inference/deployments/parameters
openapi: 3.0.3
info:
  title: CoreWeave Inference API
  version: 0.0.1
  description: >-
    The CoreWeave Inference API provides programmatic control over inference
    gateways, model deployments, and capacity claims.
servers:
  - url: https://api.coreweave.com
    description: CoreWeave production API.
security:
  - bearerAuth: []
tags:
  - name: CapacityClaimService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting
      CapacityClaim reservations of GPU hardware for inference deployments.
  - name: DeploymentService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting model
      deployments. Each deployment associates a model with one or more gateways
      and configures runtime, resources, autoscaling, and traffic.
  - name: GatewayService
    description: >-
      Endpoints for creating, listing, getting, updating, and deleting inference
      gateways. Gateways provide authentication, request routing, load
      balancing, and traffic splitting for one or more deployments.
  - name: HotLoadService
    description: >-
      Endpoints for creating, listing, getting, and canceling checkpoint
      hot-loads. A hot-load loads a new set of model weights into a running
      deployment's replicas without restarting the inference processes or
      recreating the replicas.
paths:
  /v1alpha1/inference/deployments/parameters:
    get:
      tags:
        - DeploymentService
      summary: Get deployment parameters
      description: >-
        Returns the available gateways, runtime engines and versions, runtime
        config keys, and instance types for use when creating a deployment.
      operationId: DeploymentService_GetDeploymentParameters
      parameters:
        - name: gatewayIds
          in: query
          description: >-
            Optional set of gateway IDs to scope the returned parameters to.
            When provided, the response
             enumerates only the values valid across every listed gateway, so a deployment targeting this
             exact set and using only the returned values passes validation. Empty means all of the
             organization's gateways (the values are enumerated across them without the cross-gateway
             intersection).
          schema:
            type: array
            items:
              type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetDeploymentParametersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    GetDeploymentParametersResponse:
      description: Response for GetDeploymentParameters
      type: object
      properties:
        gatewayIds:
          description: >-
            The gateway IDs in the caller's organization that can be referenced
            by a new deployment.
          type: array
          items:
            type: string
        runtimeParameters:
          description: The available runtime parameters for the deployments
          allOf:
            - $ref: '#/components/schemas/DeploymentRuntimeParameters'
          readOnly: true
        resourceParameters:
          description: The available resource parameters for the deployments
          allOf:
            - $ref: '#/components/schemas/DeploymentResourceParameters'
          readOnly: true
      required:
        - gatewayIds
    Status:
      description: >-
        Standard error response. `code` is a
        [`google.rpc.Code`](https://cloud.google.com/apis/design/errors#error_codes);
        `message` is human-readable English; `details` carries machine-readable
        error details when present.
      type: object
      properties:
        code:
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          type: integer
          format: int32
        message:
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
          type: string
        details:
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
    DeploymentRuntimeParameters:
      description: The available parameters for runtime configuration
      type: object
      properties:
        runtimeVersions:
          description: >-
            Deprecated. Use `runtimeEngineOptions` instead. Lists the available
            runtime versions for each engine.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/DeploymentRuntimeParameters_RuntimeVersions'
          readOnly: true
        runtimeConfigOptions:
          description: >-
            Deprecated. Use `runtimeEngineOptions` instead. Lists the available
            configuration options for each engine.
          type: object
          additionalProperties:
            $ref: >-
              #/components/schemas/DeploymentRuntimeParameters_RuntimeConfigOptions
          readOnly: true
        engineEnvOptions:
          description: >-
            Deprecated. Use `runtimeEngineOptions` instead. Lists the available
            environment variables for each engine.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/DeploymentRuntimeParameters_EngineEnvOptions'
          readOnly: true
        runtimeEngineOptions:
          description: >-
            The available runtime parameters, grouped by engine name and
            version.
          type: object
          additionalProperties:
            $ref: >-
              #/components/schemas/DeploymentRuntimeParameters_RuntimeEngineOptions
          readOnly: true
    DeploymentResourceParameters:
      description: The available parameters for resource configuration
      type: object
      properties:
        instanceTypes:
          description: >-
            Available instance types. May be empty — e.g. when a gateway_ids
            filter selects gateways that
             share no common instance type, or when the organization has no gateways.
          type: array
          items:
            type: string
          readOnly: true
    GoogleProtobufAny:
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      type: object
      properties:
        '@type':
          description: The type of the serialized message.
          type: string
      additionalProperties: true
    DeploymentRuntimeParameters_RuntimeVersions:
      description: List of runtime versions
      type: object
      properties:
        versions:
          description: The version strings
          type: array
          items:
            type: string
          readOnly: true
    DeploymentRuntimeParameters_RuntimeConfigOptions:
      description: The available runtime config options
      type: object
      properties:
        allowedKeys:
          description: The allowed engine config keys
          type: array
          items:
            type: string
          readOnly: true
    DeploymentRuntimeParameters_EngineEnvOptions:
      description: The available engine environment variable options
      type: object
      properties:
        allowedNames:
          description: The allowed engine environment variable names.
          type: array
          items:
            type: string
          readOnly: true
    DeploymentRuntimeParameters_RuntimeEngineOptions:
      description: The available runtime parameters for an engine.
      type: object
      properties:
        versions:
          description: The available runtime parameters, grouped by version.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/RuntimeEngineOptions_VersionOptions'
          readOnly: true
    RuntimeEngineOptions_VersionOptions:
      description: The available runtime parameters for an engine version.
      type: object
      properties:
        configOptions:
          description: >-
            The available engine configuration options, grouped by configuration
            name.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/VersionOptions_ParameterOptions'
          readOnly: true
        envOptions:
          description: >-
            The available engine environment variables, grouped by variable
            name.
          type: object
          additionalProperties:
            $ref: '#/components/schemas/VersionOptions_ParameterOptions'
          readOnly: true
        lifecycle:
          description: >-
            The lifecycle state of this runtime engine version.
            `LIFECYCLE_STABLE` is stable and available for new and existing
            deployments. `LIFECYCLE_UNSTABLE` is available for use but isn't yet
            stable. `LIFECYCLE_DEPRECATED` is available only to existing
            deployments already using the version. `LIFECYCLE_UNSPECIFIED` means
            the lifecycle state hasn't been set.
          type: string
          format: enum
          enum:
            - LIFECYCLE_UNSPECIFIED
            - LIFECYCLE_STABLE
            - LIFECYCLE_UNSTABLE
            - LIFECYCLE_DEPRECATED
          readOnly: true
    VersionOptions_ParameterOptions:
      description: Metadata for a runtime configuration parameter.
      type: object
      properties: {}
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
