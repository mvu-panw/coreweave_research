# Delete gateway

Source: https://docs.coreweave.com/products/inference/reference/api-overview/gatewayservice/delete-gateway

# Delete gateway

> Delete a CoreWeave inference gateway by its UUID.

> [!NOTE]
>
> * The API server is `https://api.coreweave.com`.
> * Replace `{API_ACCESS_TOKEN}` with your [CoreWeave API access token](https://docs.coreweave.com/security/authn-authz/manage-api-access-tokens.md).
> * For required permissions, see [IAM Access Policies](https://docs.coreweave.com/security/iam/access-policies.md).

A successful response returns the deleted gateway object,
including its final state at the moment of deletion.

```bash title="Example request" theme={"system"}
curl -X DELETE https://api.coreweave.com/v1alpha1/inference/gateways/{id} \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer {API_ACCESS_TOKEN}"
```


## OpenAPI

````yaml /openapi/inference/openapi.yaml delete /v1alpha1/inference/gateways/{id}
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
  /v1alpha1/inference/gateways/{id}:
    delete:
      tags:
        - GatewayService
      summary: Delete gateway
      description: Deletes a gateway by ID. Returns the deleted gateway.
      operationId: GatewayService_DeleteGateway
      parameters:
        - name: id
          in: path
          description: The unique identifier of the gateway to delete, UUID format
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteGatewayResponse'
        default:
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
components:
  schemas:
    DeleteGatewayResponse:
      description: Response for DeleteGateway
      type: object
      properties:
        gateway:
          description: The gateway that was deleted
          allOf:
            - $ref: '#/components/schemas/Gateway'
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
    Gateway:
      description: Gateway object with specification and status fields
      type: object
      properties:
        spec:
          description: The specification of the gateway
          allOf:
            - $ref: '#/components/schemas/GatewaySpec'
          readOnly: true
        status:
          description: The status of the gateway
          allOf:
            - $ref: '#/components/schemas/GatewayStatus'
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
    GatewaySpec:
      description: GatewaySpec contains the specification for a Gateway
      type: object
      properties:
        id:
          description: The unique identifier of the gateway, UUID format
          type: string
          readOnly: true
        name:
          description: >-
            The human readable name of the gateway. Combined with
            organization_id and the
             deployment base domain it forms the gateway's public FQDN
             (<name>.<orgId>.gw.<baseDomain>). See CreateGatewayRequest.name and
             UpdateGatewayRequest.name for the length cap applied on write.
          type: string
          readOnly: true
        zones:
          description: >-
            The Availability Zones the gateway is deployed in. The field accepts
            an array, but gateways are currently limited to one zone. The
            available zones are returned by `GET
            /v1alpha1/inference/gateways/parameters`.
          type: array
          items:
            type: string
          readOnly: true
        coreWeaveAuth:
          description: >-
            CoreWeave IAM authentication. Validates inference requests using the
            same CoreWeave API access tokens used to call the management API.
          allOf:
            - $ref: '#/components/schemas/CoreWeaveAuth'
        weightsAndBiasesAuth:
          description: >-
            Weights & Biases authentication. Validates inference requests using
            W&B SaaS credentials. W&B self-hosted is not currently supported.
          allOf:
            - $ref: '#/components/schemas/WeightsAndBiasesAuth'
        organizationId:
          description: The organization ID that owns the gateway
          type: string
          readOnly: true
        endpointConfiguration:
          description: >-
            Optional endpoint configuration. Use `additionalDns` to register
            additional DNS names that you point at the gateway endpoint
            manually.
          allOf:
            - $ref: '#/components/schemas/EndpointConfiguration'
        bodyBasedRouting:
          description: Body based routing
          allOf:
            - $ref: '#/components/schemas/BodyBasedRouting'
        headerBasedRouting:
          description: Header based routing
          allOf:
            - $ref: '#/components/schemas/HeaderBasedRouting'
        pathBasedRouting:
          description: Path based routing
          allOf:
            - $ref: '#/components/schemas/PathBasedRouting'
    GatewayStatus:
      description: GatewayStatus contains the status fields for a Gateway
      type: object
      properties:
        createdAt:
          description: The time at which the gateway was created.
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          description: The time at which the gateway was last updated.
          type: string
          format: date-time
          readOnly: true
        status:
          description: >-
            The overall status of the gateway. `STATUS_UNSPECIFIED` means the
            status has not been set. See the [Inference API
            overview](https://docs.coreweave.com/products/inference/reference/api-overview#status-values)
            for the meaning of each value. Once `STATUS_READY`, the gateway
            exposes one or more endpoint URLs in `endpoints`.
          type: string
          format: enum
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_CREATING
            - STATUS_UPDATING
            - STATUS_DELETING
            - STATUS_ERROR
            - STATUS_FAILED
            - STATUS_READY
          readOnly: true
        conditions:
          description: List of conditions representing detailed status information
          type: array
          items:
            $ref: '#/components/schemas/Condition'
          readOnly: true
        endpoints:
          description: >-
            The endpoint URLs for the gateway. The default endpoint follows the
            pattern `https://[GATEWAY-NAME].[ORG-ID].gw.cwinference.com`;
            additional entries appear when `endpointConfiguration.additionalDns`
            is set.
          type: array
          items:
            type: string
          readOnly: true
    CoreWeaveAuth:
      description: Use CoreWeave Identity and Access Management (IAM) authentication.
      type: object
      properties:
        organizations:
          description: >-
            The organizations allowed to authenticate. If omitted, the
            organization that owns the gateway is used. Only one organization is
            supported.
          type: array
          items:
            type: string
    WeightsAndBiasesAuth:
      description: Use W&B auth
      type: object
      properties:
        apiKey:
          description: The W&B organization API key. Required if `serverUrl` is set.
          type: string
        serverUrl:
          description: Optional W&B server URL. Defaults to the W&B shared SaaS instance.
          type: string
        enableUsageReports:
          description: Send inference usage data to W&B for tracking.
          type: boolean
        enableRateLimiting:
          description: Enable W&B-controlled rate limiting for inference requests.
          type: boolean
    EndpointConfiguration:
      description: Configuration options for the gateway endpoint, DNS, TLS, etc.
      type: object
      properties:
        additionalDns:
          description: >-
            Additional DNS configurations, these DNS need to be configured to
            point to the gateway endpoint manually
          type: array
          items:
            type: string
        edgeProxyMode:
          description: >-
            How client traffic reaches the gateway. `EDGE_PROXY_MODE_MANAGED`
            proxies traffic through CoreWeave's managed edge network: DDoS
            mitigation and WAF, with TLS terminated at the edge and the origin
            address kept out of public DNS. `EDGE_PROXY_MODE_DIRECT` connects
            clients straight to the gateway's load balancer, with no edge
            filtering and the load balancer address published in DNS.
            `EDGE_PROXY_MODE_UNSPECIFIED` (or omitting the field) applies the
            platform default, currently managed.
          type: string
          format: enum
          enum:
            - EDGE_PROXY_MODE_UNSPECIFIED
            - EDGE_PROXY_MODE_MANAGED
            - EDGE_PROXY_MODE_DIRECT
        allowedSourceIpRanges:
          description: >-
            Client source IP ranges permitted to reach the gateway, in CIDR
            notation (IPv4 or IPv6), up to
             50 entries. An empty list applies no source restriction. Use a full-length prefix for a single
             address (e.g. "203.0.113.5/32").
          type: array
          items:
            type: string
    BodyBasedRouting:
      description: Body based routing configuration
      type: object
      properties:
        apiType:
          description: >-
            Well-known API type for routing. `API_TYPE_OPENAI` extracts the
            model name from the `model` field in the JSON request body
            (OpenAI-compatible behavior). The zero value `API_TYPE_UNSPECIFIED`
            is never valid to send.
          type: string
          format: enum
          enum:
            - API_TYPE_OPENAI
      required:
        - apiType
    HeaderBasedRouting:
      description: >-
        Header based routing configuration, uses a header value to route
        requests to the model by name
      type: object
      properties:
        headerName:
          description: >-
            The HTTP header to read the model name from on each inference
            request. Must be 1-100 characters.
          type: string
      required:
        - headerName
    PathBasedRouting:
      description: >-
        Path-based routing configuration. The model name is read from the first
        segment of the URL path (for example, `/my-model/v1/chat/completions`).
        URL-encode model names that contain special characters.
      type: object
      properties: {}
    Condition:
      description: Condition represents a detailed status condition for resources
      type: object
      properties:
        type:
          description: Type of condition
          type: string
          readOnly: true
        status:
          description: >-
            The status of the condition: `STATUS_TRUE` or `STATUS_FALSE`, or
            `STATUS_UNSPECIFIED` when the status has not been set.
          type: string
          format: enum
          enum:
            - STATUS_UNSPECIFIED
            - STATUS_FALSE
            - STATUS_TRUE
          readOnly: true
        lastUpdateTime:
          description: Last time the condition was updated
          type: string
          format: date-time
          readOnly: true
        reason:
          description: Reason for the condition's last transition
          type: string
          readOnly: true
        message:
          description: Human-readable message indicating details about the condition
          type: string
          readOnly: true
        zone:
          description: Zone associated with the condition
          type: string
          readOnly: true
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: CoreWeave API access token sent as a bearer token.
      x-default: Bearer {API_ACCESS_TOKEN}

````
