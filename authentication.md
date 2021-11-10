

## Authentication for Web Services

- Security Assertion Markup Languages (SAML) token, which supports both authenticatoin and authorization
- Token-based authentication, including JWT
- Digest authentication. A username and password are encoded and sent in a header.
- Mutual TLS authentication. Both ends store a known public certificate for the other endpoint. During authentication, a challenge is sent which is encrypted with an endpoint's private certificate.

Security:
- Token-based authentication can be subject to replay attacks
- Digest auth uses a challenge (from the server) and nonce (chosen by client) in the digest header, so is resistent to replay attacks.  But, the server needs to store the client's original password to verify the digest.
