# Diff-Match-Patch

Please view original documentation at [GitHub Link](https://github.com/google/diff-match-patch).

## About
Diff Match Patch is a high-performance library in multiple languages that manipulates plain text.

## Design decision

### Motivation
In case of large text update, rather than sending the whole updated text, just send
patches to be applied to save bandwidth.

### Conclusion
Whenever `text` field is to be updated, the request can contain the field name suffixed
by `_patch` such as `text_patch`. In this case, the patch is applied to the existing field.

**Note**: Cannot update using both field and `field_patch` in same request.
