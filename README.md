# Checks API

![action status](https://github.com/ch4zzy/checks-api/actions/workflows/django.yml/badge.svg)
![action status](https://github.com/ch4zzy/checks-api/actions/workflows/pre-commit.yml/badge.svg)

[Here is the project with using only APIView](https://github.com/ch4zzy/checks-api-apiview)

The service receives information about a new order, creates checks for all the printers of the specified location in the database, and initiates asynchronous tasks for generating PDF files for these checks. If the location does not have any printers, an error is returned. If checks for this order have already been created, an error is returned along with the order number.


## Endpoints
```
GET /api/check/ - List of all  checks.
```
```
GET /api/check/<int:id>/ - Detail of current check.
```
```
GET /api/check/?point_id=<int:id>/ - List of checks for current point id.
```

```
PUT /api/check/<int:id>/update/ - check downloading and marking as printed.
```

```
POST /api/create/ - Check create.
```
## Request example.

```json
{
  "point_id": 1,
  "order": {
    "order_id": 2,
    "item": "Milk",
    "quantity": 2,
    "price": 10.99
  }
}
```

## Testing

Tested using pytest and pytest-django.
