# Routes

## User

### Login user

- **URL:** v2/auth/login/
- **Method:** POST

**Request:**

```json
{
  "username": "test@example.com",
  "password": "<password>"
}
```

**Response:**

```json
{
  "token": "<token>"
}
```

### Create user

- **URL:** v2/user/
- **Method:** POST

**Request:**

```json
{
  "email": "test@example.com",
  "password": "<password>"
}
```

**Response:**

```json
{
  "id": "<uuid>",
  "email": "test@example.com"
}
```

### Retrieve authenticated user

- **URL:** v2/user/
- **Method:** GET
- **Permissions:**
    - Auth

**Response:**

```json
{
  "id": "<uuid>",
  "email": "test@example.com"
}
```

### Retrieve user by id

- **URL:** v2/user/<:id>
- **Method:** GET
- **Permissions:**
    - Auth

**Response:**

```json
{
  "id": "<:id>",
  "email": "test@example.com"
}
```

## TextBlock

### Create block

- **URL:** v2/block/
- **Method:** POST
- **Permissions**:
    - Editor or above
    - Auth

**Request:**

```json
{
  "title": "Intro",
  "text": "This document is ...",
  "parent": "<uuid?>"
}
```

**Response:**

```json
{
  "id": "<uuid>",
  "title": "Intro",
  "text": "This document is ...",
  "children": [],
  "parent": "<uuid?>"
}
```

### Retrieve block by id

- **URL:** v2/block/<:id>
- **Method:** GET
- **Permissions**:
    - View or above
    - Auth

**Response:**

```json
{
  "id": "<:id>",
  "title": "Intro",
  "text": "This document is ...",
  "children": [
    "<uuid>",
    "<uuid>"
  ],
  "parent": "<uuid?>"
}
```

### Update block by id

- **URL:** v2/block/<:id>
- **Method:** PATCH
- **Permissions**:
    - Editor or above
    - Auth

**Request:**

```json
{
  "title": "Intro to platform"
}
```

**Response:**

```json
{
  "id": "<:id>",
  "title": "Intro to platform",
  "text": "This document is ...",
  "children": [
    "<uuid>",
    "<uuid>"
  ],
  "parent": "<uuid?>"
}
```

### Delete block by id

- **URL:** v2/block/<:id>
- **Method:** DELETE
- **Permissions**:
    - Editor or above
    - Auth

**Response:**

```json
{
  "id": "<:id>",
  "title": "Intro to platform",
  "text": "This document is ...",
  "children": [
    "<uuid>",
    "<uuid>"
  ],
  "parent": "<uuid?>"
}
```

## PermissionBlock

### Create permission block

- **URL:** v2/permission/block/
- **Method:** POST
- **Permissions**:
    - Owner
    - Auth

**Request:**

```json
{
  "block_id": "<uuid>",
  "email": "test@email.com",
  "permission": "View"
}
```

**Response:**

```json
{
  "id": "<uuid>",
  "block_id": "<uuid>",
  "user_id": "<uuid>",
  "permission": "View"
}
```

### Retrieve permission blocks by block id

- **URL:** v2/permission/block
- **Params:**: block_id
- **Method:** GET
- **Permissions**:
    - Owner
    - Auth

**Response:**

```json
[
  {
    "id": "<uuid>",
    "block_id": "<:block_id>",
    "email": "test@example.com",
    "permission": "Owner"
  },
  {
    "id": "<uuid>",
    "block_id": "<:block_id>",
    "email": "test@email.com",
    "permission": "View"
  }
]
```

### Update permission block by id

- **URL:** v2/permission/block/<:id>
- **Method:** PATCH
- **Permissions**:
    - Owner
    - Auth

**Request:**

```json
{
  "permission": "Editor"
}
```

**Response:**

```json
{
  "id": "<:id>",
  "block_id": "<uuid>",
  "email": "test@email.com",
  "permission": "Editor"
}
```

### Delete permission block by id

- **URL:** v2/permission/block/<:id>
- **Method:** DELETE
- **Permissions**:
    - Owner
    - Auth

**Response:**

```json
{
  "id": "<:id>",
  "block_id": "<uuid>",
  "email": "test@email.com",
  "permission": "Editor"
}
```
