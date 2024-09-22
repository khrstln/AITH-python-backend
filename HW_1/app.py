import json
from typing import Any, Callable, Dict
from urllib.parse import parse_qs

from .math_funcs import factorial, fibonacci, mean
from .errors import send_error


async def app(scope: Dict[str, Any], receive: Callable,
              send: Callable) -> None:
    if scope['type'] != 'http':
        return

    method = scope['method']
    path = scope['path']

    if path.startswith('/factorial') and method == 'GET':
        await handle_factorial(scope, send)
        return

    elif path.startswith('/fibonacci') and method == 'GET':
        await handle_fibonacci(path, send)
        return

    elif path.startswith('/mean') and method == 'GET':
        await handle_mean(receive, send)
        return

    await send_error(404, send)


async def send_json_response(send, data, status=200):
    response_body = json.dumps(data).encode('utf-8')
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [
            (b'content-type', b'application/json'),
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
    })


async def receive_body(receive: Callable) -> bytes:
    body = b""

    while True:
        message = await receive()

        body += message.get('body', b'')
        if not message.get('more_body', False):
            break

    return body


async def handle_factorial(scope: Dict[str, Any], send: Callable) -> None:
    print("factorial")
    query_string = scope['query_string'].decode('utf-8')
    params = parse_qs(query_string)

    if 'n' not in params:
        await send_error(422, send)
        return

    try:
        n = int(params['n'][0])
        if n < 0:
            await send_error(400, send)
            return
        await send_json_response(send, {"result": factorial(n)})
        return
    except ValueError:
        await send_error(422, send)
        return


async def handle_fibonacci(path: str, send: Callable) -> None:
    try:
        n = int(path.split('/')[-1])

        if n < 0:
            await send_error(400, send)
            return

        await send_json_response(send, {"result": fibonacci(n)})
        return

    except ValueError:
        await send_error(422, send)
        return


async def handle_mean(receive: Callable, send: Callable) -> None:
    body = await receive_body(receive)
    try:
        nums = json.loads(body)

        if len(nums) == 0:
            await send_error(400, send)
            return

        if not isinstance(nums, list) or not all(
                isinstance(x, (int, float)) for x in nums):
            await send_error(422, send)
            return

        await send_json_response(send, {"result": mean(nums)})
        return
    except (json.JSONDecodeError, TypeError):
        await send_error(422, send)
        return
