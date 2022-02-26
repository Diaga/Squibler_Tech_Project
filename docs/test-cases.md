# Test cases

## User

### Login user

**Success**:
- [x] Correct credentials

**Fail**:
- [x] User does not exist
- [x] Incorrect credentials

### Create user

**Success**:
- [x] Unauthenticated

**Fail**:
- [x] Authenticated
- [x] Non-validated email

### Retrieve authenticated user

**Success**:
- [x] Authenticated

**Fail**:
- [x] Unauthenticated

### Retrieve user by id

**Success**:
- [x] Authenticated

**Fail**:
- [x] Unauthenticated
- [x] User does not exist

## TextBlock

### Create block

**Success**:
- [x] Authenticated and Editor
- [x] Authenticated and Owner

**Fail**:
- [x] Authenticated and View
- [x] Authenticated
- [x] Unauthenticated

### Retrieve block by id

**Success**:
- [x] Authenticated and View
- [x] Authenticated and Editor
- [x] Authenticated and Owner

**Fail**:
- [x] Unauthenticated
- [x] Authenticated

### Update block by id

**Success**:
- [x] Authenticated and Editor
- [x] Authenticated and Owner

**Fail**:
- [x] Unauthenticated
- [x] Authenticated
- [x] Authenticated and View

### Delete block by id

**Success**:
- [x] Authenticated and Owner
- [x] Authenticated and Editor

**Fail**:
- [x] Unauthenticated
- [x] Authenticated
- [x] Authenticated and View

## PermissionBlock

### Create permission block

**Success**:
- [x] Authenticated and Owner

**Fail**:
- [x] Unauthenticated
- [x] Authenticated
- [x] Authenticated and View
- [x] Authenticated and Editor

### Retrieve permission blocks by block id

**Success**:
- [x] Authenticated and Owner

**Fail**:
- [x] Unauthenticated
- [x] Authenticated
- [x] Authenticated and View
- [x] Authenticated and Editor

### Update permission block by id

**Success**:
- [x] Authenticated and Owner

**Fail**:
- [x] Unauthenticated
- [x] Authenticated
- [x] Authenticated and View
- [x] Authenticated and Editor

### Delete permission block by id

**Success**:
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View
- [ ] Authenticated and Editor
