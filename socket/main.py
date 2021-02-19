from socketserver import BaseRequestHandler, TCPServer
from urllib.parse import unquote
import re


DEFAULT_BUFFER_SIZE = 1024


class TCPHandler(BaseRequestHandler):

    def handle(self) -> None:

        data = self.request.recv(DEFAULT_BUFFER_SIZE)

        while len(data) != 0:

            data = self._get_content(data, "content")

            print(f"\n{self.client_address[0]}#{self.client_address[1]}: {data}")
            print()

            self.request.send(data.upper())

            data = self.request.recv(DEFAULT_BUFFER_SIZE)
            data = self._get_content(data, "content")

    @staticmethod
    def _get_content(data, parameter_name: str):
        regexp = f"/?{parameter_name}=(.*) HTTP/1.1"

        try:
            match = unquote(    # replace URL characters like %22
                re.findall(regexp, str(data))[0]    # get first match
            )
        except IndexError:
            match = ""

        return bytes(match.encode("utf-8"))

    def finish(self) -> None:
        print(">>>>\n")


if __name__ == "__main__":
    host = 'localhost', 8080

    TCPServer.allow_reuse_address = True
    server = TCPServer(host, TCPHandler)
    TCPServer.allow_reuse_address = True

    server.serve_forever()
