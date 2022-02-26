
### Data Dictionary

### v2

The v1 model is generic and allows the platform to introduce more types. For the given requirements, we just need two
properties for every block:

- Title
- Text

The data dictionary (v2) is simplified as follows:

#### User

| Name     | Type | Description                                    | Properties |
|----------|------|------------------------------------------------|------------|
| id       | uuid | Primary key for User model. Defaults to uuid4. | pk, unique |
| email    | str  | Email address of the user.                     | unique     |
| password | str  | Hashed password of the user.                   |            |

#### PermissionBlock

| Name       | Type | Description                                                            | Properties |
|------------|------|------------------------------------------------------------------------|------------|
| id         | uuid | Primary key for PermissionBlock model. Defaults to uuid4.              | pk, unique |
| block_id   | uuid | Foreign key to Block table.                                            | fk         |
| user_id    | uuid | Foreign key to User table.                                             | fk         |
| permission | enum | Defines the permission level. <br/>Possible enums: Owner, Editor, View |            |

**Note**:
- Grants same permission to all child blocks.

#### TextBlock

| Name     | Type | Description                                                                                                                                     | Properties   |
|----------|------|-------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| id       | uuid | Primary key for TextBlock model. Defaults to uuid4.                                                                                             | pk, unique   |
| title    | str  | Title of the block.                                                                                                                             |              |
| text     | str  | Text content of the block.                                                                                                                      |              |
| children | list | Back links to children blocks from TextBlock table.                                                                                             |              |
| parent   | uuid | Foreign key to parent TextBlock table.                                                                                                          | fk, nullable |

### v1

#### User

| Name     | Type | Description                                    | Properties |
|----------|------|------------------------------------------------|------------|
| id       | uuid | Primary key for User model. Defaults to uuid4. | pk, unique |
| email    | str  | Email address of the user.                     | unique     |
| password | str  | Hashed password of the user.                   |            |

#### PermissionBlock

| Name       | Type | Description                                                            | Properties |
|------------|------|------------------------------------------------------------------------|------------|
| id         | uuid | Primary key for PermissionBlock model. Defaults to uuid4.              | pk, unique |
| block_id   | uuid | Foreign key to Block table.                                            | fk         |
| user_id    | uuid | Foreign key to User table.                                             | fk         |
| permission | enum | Defines the permission level. <br/>Possible enums: Owner, Editor, View |            |

**Note**:
- Grants same permission to all child blocks.

#### Block

| Name       | Type | Description                                                                                                                                     | Properties   |
|------------|------|-------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| id         | uuid | Primary key for Block model. Defaults to uuid4.                                                                                                 | pk, unique   |
| type       | enum | Block type which determines how a block is displayed and how the block's properties are interpreted by frontend. <br/><br/>Possible enums: text |              |
| properties | list | Back links to property values from PropertyValue table.                                                                                         |              |
| children   | list | Back links to children blocks from Block table.                                                                                                 |              |
| parent     | uuid | Foreign key to parent Block table.                                                                                                              | fk, nullable |  

#### PropertyValue

| Name     | Type | Description                                             | Properties |
|----------|------|---------------------------------------------------------|------------|
| id       | uuid | Primary key for PropertyValue model. Defaults to uuid4. | pk, unique |
| property | uuid | Foreign key to Property table.                          |            |
| value    | str  | Value of the property.                                  |            |
| block_id | uuid | Foreign key to Block table.                             |            |

#### Property

| Name     | Type | Description                                                                        | Properties |
|----------|------|------------------------------------------------------------------------------------|------------|
| id       | uuid | Primary key for Property model. Defaults to uuid4.                                 | pk, unique |
| type     | enum | Property type determines how the value is going to be interpreted by the frontend. |            |

**Validate model with requirements**

Using the data dictionary (v2), let's model the given requirements:

- Unlimited sections and subsections:
    - Section is a Block with type = 'section'.
    - It will have following the properties:
        1. type = 'title'
        2. type = 'text'

- Collaboration:
    - The blocks give one source of truth to unlimited number of consumers.

**How to extend for advanced features?**

- Blocks can be extended to show version history.
    - Maintain history of blocks.
- Blocks can be extended for conflict resolution.
    - Use timestamps such as updated_at to determine the latest block.
    - Migrations:
        - Introduce a reference uuid field for maintaining version history and conflict resolution.
