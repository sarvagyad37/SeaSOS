from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import httpx
from typing import Dict

# Replace these with your actual User Pool ID and AWS region
AWS_REGION = 'us-east-1'
COGNITO_USER_POOL_ID = 'your-user-pool-id'
COGNITO_APP_CLIENT_ID = 'your-app-client-id'
COGNITO_PUBLIC_KEYS_URL = f'https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency that will retrieve and validate the current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    try:
        # Validate the token and return the user's information
        return await validate_token(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Validate the JWT token
async def validate_token(token: str) -> Dict:
    # Fetch the public keys from AWS Cognito
    async with httpx.AsyncClient() as client:
        response = await client.get(COGNITO_PUBLIC_KEYS_URL)
        response.raise_for_status()
        public_keys = response.json()["keys"]

    # Decode the token's header to find out which key id (kid) it was signed with
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    key = [k for k in public_keys if k['kid'] == kid]
    if not key:
        raise JWTError("Invalid token: Key ID not found.")
    key = key[0]

    # Decode the token
    decoded_token = jwt.decode(
        token,
        key,
        algorithms=["RS256"],
        audience=COGNITO_APP_CLIENT_ID
    )

    # Perform additional checks, for example, on the token's 'iss' claim
    issuer = f'https://cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}'
    if decoded_token['iss'] != issuer:
        raise JWTError("Invalid token: Incorrect issuer.")

    # You can add more validations if needed (e.g., token use, expiration)

    return decoded_token
