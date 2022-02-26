# Test cases

## User

### Login user

**Success**:
- [ ] Correct credentials

**Fail**:
- [ ] User does not exist
- [ ] Incorrect credentials

### Create user

**Success**:
- [ ] Unauthenticated

**Fail**:
- [ ] Authenticated
- [ ] Non-validated email

### Retrieve authenticated user

**Success**:
- [ ] Authenticated

**Fail**:
- [ ] Unauthenticated

### Retrieve user by id

**Success**:
- [ ] Authenticated

**Fail**:
- [ ] Unauthenticated
- [ ] User does not exist

## TextBlock

### Create block

**Success**:
- [ ] Authenticated and Editor
- [ ] Authenticated and Owner

**Fail**:
- [ ] Authenticated and View
- [ ] Unauthenticated

### Retrieve block by id

**Success**:
- [ ] Authenticated and View
- [ ] Authenticated and Editor
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated

### Update block by id

**Success**:
- [ ] Authenticated and Editor
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View

### Delete block by id

**Success**:
- [ ] Authenticated and Owner
- [ ] Authenticated and Editor

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View

## PermissionBlock

### Create permission block

**Success**:
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View
- [ ] Authenticated and Editor

### Retrieve permission blocks by block id

**Success**:
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View
- [ ] Authenticated and Editor

### Update permission block by id

**Success**:
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View
- [ ] Authenticated and Editor

### Delete permission block by id

**Success**:
- [ ] Authenticated and Owner

**Fail**:
- [ ] Unauthenticated
- [ ] Authenticated
- [ ] Authenticated and View
- [ ] Authenticated and Editor