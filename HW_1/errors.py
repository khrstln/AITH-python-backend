from typing import Callable


async def send_error(status: int, send: Callable) -> None:
    body_dict = {400: b'{"detail": "Bad Request"}',
                 404: b'{"detail": "Not Found"}',
                 422: b'{"detail": "Unprocessable Entity"}'}

    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [(b'content-type', b'application/json')],
    })
    await send({
        'type': 'http.response.body',
        'body': body_dict[status],
    })
