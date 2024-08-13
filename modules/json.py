import requests
from argo_probe_json.exceptions import CriticalException


class Json:
    def __init__(self, url, timeout=30):
        self.url = url
        self.timeout = timeout

    def _get(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()

        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects,
            ValueError
        ) as e:
            raise CriticalException(str(e))

    def get(self):
        return self._get()

    def parse(self, key):
        data = self._get()

        keys = key.split(".")

        try:
            if len(keys) == 1:
                return data[key]

            else:
                value = data[keys[0]]
                for k in keys[1:]:
                    value = value[k]

                return value

        except KeyError:
            raise CriticalException(f"Key '{key}' not found")
