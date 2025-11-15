import uuid


def generate_serializer_errors(errors):
    """Return a readable string for serializer validation errors."""
    message = ""
    for key, values in errors.items():
        joined = ",".join(values)
        message += f"{key}: {joined} | "
    return message[:-3]


def create_response_data(statuscode, title, data, errors, message):
    """Standard API response format."""
    return {
        'statuscode': statuscode,
        'title': title,
        'data': data,
        'errors': errors,
        'message': message,
    }


def generate_field_id():
    return "f_" + uuid.uuid4().hex[:8]