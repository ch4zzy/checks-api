# Checks API

The service receives information about a new order, creates checks for all the printers of the specified location in the database, and initiates asynchronous tasks for generating PDF files for these checks. If the location does not have any printers, an error is returned. If checks for this order have already been created, an error is returned along with the order number.


## Endpoints
GET `/api/check/` - List of all  checks.
GET `/api/check/<int:id>/printer_list/` - List of all checks for current printer.
GET `/api/checkfile/<int:id>/` - check downloading and marking as printed.

POST `/api/create/` - Check create.
Request example.

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
