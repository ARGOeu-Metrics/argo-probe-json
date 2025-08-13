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
            error = str(e)
            if self.url in error:
                error = error.replace(self.url, "")

            raise CriticalException(error)

    def get(self):
        return self._get()

    def parse(self, key):
        data = self._get()

        keys = key.split(".")

        try:
            if len(keys) == 1:
                if key.isdigit():
                    key = int(key)
                return data[key]

            else:
                if keys[0].isdigit():
                    value = data[int(keys[0])]

                elif keys[0] == "*":
                    value = data

                else:
                    value = data[keys[0]]

                for i in range(1, len(keys)):
                    k = keys[i]
                    if k.isdigit():
                        k = int(k)

                    if keys[i] == "*":
                        pass

                    elif keys[i - 1] == "*":
                        value = [v[k] for v in value]

                    else:
                        value = value[k]

                return value

        except KeyError:
            raise CriticalException(f"Key '{key}' not found")
