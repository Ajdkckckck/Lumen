# Profile Service

This file contains functions to retrieve user statistics and metrics from the database.

## Functions

### get_user_statistics(user_id)
Retrieves statistics for a given user.

- **Parameters:**
    - `user_id`: The ID of the user to retrieve statistics for.
- **Returns:** A dictionary containing user statistics.

### get_user_metrics(user_id)
Retrieves metrics for a given user.

- **Parameters:**
    - `user_id`: The ID of the user to retrieve metrics for.
- **Returns:** A dictionary containing user metrics.

### Example Usage

```python
# Fetch user statistics
statistics = get_user_statistics(1)

# Fetch user metrics
metrics = get_user_metrics(1)
```