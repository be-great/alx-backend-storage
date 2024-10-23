#!/usr/bin/env python3
"""
0. Writing strings to Redis
1. Reading from Redis and
 recovering original type
2. Incrementing values
3. Storing lists
4. Retrieving lists
5. Implementing an expiring web cache and tracker
"""


class Cache:
    def __init__(self):
        """Initialize Redis connection and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis using a random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn:
            Optional[Callable] = None) -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and apply an
        optional conversion function.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string value from Redis."""
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer value from Redis."""
        return self.get(key, int)


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment the call count each time the method is called."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs of a function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store input/output history and return the output."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable):
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    method_name = method.__qualname__
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        str0 = f"{method_name}(*{inp.decode('utf-8')})"
        str1 = str0 + f" -> {out.decode('utf-8')}"
        print(str1)


Cache.store = count_calls(call_history(Cache.store))
