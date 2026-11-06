# Get capacity claim parameters

Source: https://docs.coreweave.com/products/inference/reference/api-overview/capacityclaimservice/get-capacity-claim-parameters

# Get capacity claim parameters

> Enumerate the available instance types per Availability Zone for CapacityClaim creation.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

The response includes `zoneInstanceTypes`, a map keyed by
Availability Zone (for example, `US-WEST-04A`) whose values
list the `instanceId` strings that are valid for a
CapacityClaim in that zone.

```bash title="Example request" theme={"system"}
curl -X GET https://api.coreweave.com/v1alpha1/inference/capacityclaims/parameters \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml get /v1alpha1/inference/capacityclaims/parameters
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
  /v1alpha1/inference/capacityclaims/parameters:
    get:
      tags:
        - CapacityClaimService
      summary: Get capacity claim parameters
      description: >-
        Returns the available instance types per Availability Zone for use when
        creating a CapacityClaim.
      operationId: CapacityClaimService_GetCapacityClaimParameters
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GetCapacityClaimParametersResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    GetCapacityClaimParametersResponse:
      description: Response for GetCapacityClaimParameters
      type: object
      properties:
        zoneInstanceTypes:
          description: >-
            Map keyed by Availability Zone (for example, `US-WEST-04A`) whose
            values list the `instanceId` strings that are valid for a
            CapacityClaim in that zone.
          type: object
          additionalProperties:
            $ref: >-
              #/components/schemas/GetCapacityClaimParametersResponse_InstanceTypes
          readOnly: true
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
    GetCapacityClaimParametersResponse_InstanceTypes:
      description: List of available instance types
      type: object
      properties:
        instanceIds:
          description: List of instance type IDs
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
