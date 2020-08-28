import json
import requests


# This function is temporarily here
def handle_response(response):
    print("\nResponse status code:")
    print(response.status_code)
    print("\nResponse headers:")
    print(json.dumps(dict(response.headers), indent=4))
    print("\nResponse json:")
    try:
        print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print("-")

class Firecrest:
    """Stores all the client information.
    """
    def __init__(self, firecrest_url=None, authentication=None):
        self._firecrest_url = firecrest_url
        self._authentication = authentication

    def _json_response(self, response, expected_status_code):
        status_code = response.status_code
        if status_code >= 400:
            handle_response(response)
            raise Exception('Status code: '+str(status_code)+' '+repr(response.json()))
        elif status_code != expected_status_code:
            handle_response(response)
            raise Exception(f'status_code ({status_code}) != expected_status_code ({expected_status_code})')

        handle_response(response)

        return response.json()

    # Status
    def all_services(self):
        url = f"{self._firecrest_url}/status/services"
        headers = {f"Authorization": f"Bearer {self._authentication.get_access_token()}"}
        resp = requests.get(url=url, headers=headers)

        return self._json_response(resp, 200)["out"]

    def service(self, servicename):
        url = f"{self._firecrest_url}/status/services/{servicename}"
        headers = {f"Authorization": f"Bearer {self._authentication.get_access_token()}"}
        resp = requests.get(url=url, headers=headers)

        return self._json_response(resp, 200)["out"]

    def all_systems(self):
        url = f"{self._firecrest_url}/status/systems"
        headers = {f"Authorization": f"Bearer {self._authentication.get_access_token()}"}
        resp = requests.get(url=url, headers=headers)

        return self._json_response(resp, 200)["out"]

    def system(self, systemsname):
        url = f"{self._firecrest_url}/status/systems/{systemsname}"
        headers = {f"Authorization": f"Bearer {self._authentication.get_access_token()}"}
        resp = requests.get(url=url, headers=headers)

        return self._json_response(resp, 200)["out"]

    def parameters(self):
        url = f"{self._firecrest_url}/status/parameters"
        headers = {f"Authorization": f"Bearer {self._authentication.get_access_token()}"}
        resp = requests.get(url=url, headers=headers)

        return self._json_response(resp, 200)["out"]

    # Utilities
    def list_files(self, machine, targetPath, showhidden=None):
        url = f"{self._firecrest_url}/utilities/ls"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        params = {
            "targetPath": f"{targetPath}"
        }
        if showhidden:
            params["showhidden"] = showhidden

        resp = requests.get(
            url=url,
            headers=headers,
            params=params,
        )

        return self._json_response(resp, 200)["output"]

    def mkdir(self, machine, targetPath, p=None):
        url = f"{self._firecrest_url}/utilities/mkdir"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        data = {"targetPath": targetPath}
        if p:
            data["p"] = p

        resp = requests.post(
            url=url,
            headers=headers,
            data=data,
        )

        self._json_response(resp, 201)

    def mv(self, machine, sourcePath, targetPath):
        url = f"{self._firecrest_url}/utilities/rename"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        data = {
            "targetPath": targetPath,
            "sourcePath": sourcePath
        }

        resp = requests.put(
            url=url,
            headers=headers,
            data=data,
        )

        self._json_response(resp, 200)

    def chmod(self, machine, targetPath, mode):
        url = f"{self._firecrest_url}/utilities/chmod"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        data = {
            "targetPath": targetPath,
            "mode": mode
        }

        resp = requests.put(
            url=url,
            headers=headers,
            data=data,
        )

        self._json_response(resp, 200)

    def chown(self, machine, targetPath, owner=None, group=None):
        if owner is None and group is None:
            return

        url = f"{self._firecrest_url}/utilities/chown"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        data = {
            "targetPath": targetPath
        }
        if owner:
            data["owner"] = owner

        if group:
            data["group"] = group

        resp = requests.put(
            url=url,
            headers=headers,
            data=data,
        )

        self._json_response(resp, 200)

    def copy(self, machine, sourcePath, targetPath):
        url = f"{self._firecrest_url}/utilities/copy"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        data = {
            "targetPath": targetPath,
            "sourcePath": sourcePath
        }

        resp = requests.post(
            url=url,
            headers=headers,
            data=data,
        )

        self._json_response(resp, 201)

    def file_type(self, machine, targetPath):
        url = f"{self._firecrest_url}/utilities/file"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        params = {
            "targetPath": targetPath
        }

        resp = requests.get(
            url=url,
            headers=headers,
            params=params,
        )

        return self._json_response(resp, 200)["out"]

    def symlink(self, machine, targetPath, linkPath):
        url = f"{self._firecrest_url}/utilities/symlink"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        data = {
            "targetPath": targetPath,
            "linkPath": linkPath
        }

        resp = requests.post(
            url=url,
            headers=headers,
            data=data,
        )

        self._json_response(resp, 201)

    def simple_download(self, machine, sourcePath, targetPath):
        """Blocking call to download a small file.

        The size of file that is allowed can be found from the parameters() call.

        sourcePath is in the machine's filesystem
        targetPath is in the local filesystem
        """

        url = f"{self._firecrest_url}/utilities/download"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }
        params = {
            "sourcePath": sourcePath
        }

        resp = requests.get(
            url=url,
            headers=headers,
            params=params,
        )

        if resp.status_code == 200:
            with open(targetPath, "wb") as f:
                f.write(resp.content)
        else:
            raise Exception('Status code: '+str(resp.status_code)+' '+repr(resp.json()))

    def simple_upload(self, machine, sourcePath, targetPath):
        """Blocking call to upload a small file.

        The size of file that is allowed can be found from the parameters() call.

        sourcePath: in the local filesystem
        targetPath: in the machine's filesystem
        """

        url = f"{self._firecrest_url}/utilities/upload"
        headers = {
            "Authorization": f"Bearer {self._authentication.get_access_token()}",
            "X-Machine-Name": machine,
        }

        with open(sourcePath, "rb") as f:
            data = {
                "targetPath": targetPath,
                "sourcePath": f
            }

            resp = requests.post(
                url=url,
                headers=headers,
                data=data,
            )

        self._json_response(resp, 201)

    def simple_delete():
        """Blocking call to delete a small file.

        The size of file that is allowed can be found from the parameters() call.
        """
        pass

    def checksum(self):
        pass

    def view(self):
        pass

