# API Gateway

A single entry point to other services.

## Implemented Features

### User Registration

Identical in signature to the registration method in the Auth service. Proxies the request to the registration method in the Auth service.

### User Authentication

Identical in signature to the authentication method in the Auth service. Proxies the request to the authentication method in the Auth service.

### Transaction Creation

Identical in signature to the transaction creation method in the Transactions service. Before forwarding  the request to the transaction creation method, the Transactions service verifies the validity of the provided JWT token using the JWT token validation method in the Auth service.

### Getting User Transaction Report

Identical in signature to the transaction report retrieval method in the Transactions service. Before forwarding  the request to the transaction report retrieval method, the Transactions service verifies the validity of the provided JWT token using the JWT token validation method in the Auth service.

### Vector Generation

Identical in signature to the vector generation method in the Face Verification service. Before forwarding the request to the vector generation method, the Face Verification service verifies the validity of the provided JWT token using the JWT token validation method in the Auth service.
