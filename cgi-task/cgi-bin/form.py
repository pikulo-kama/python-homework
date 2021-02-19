#!/usr/bin/env python3

import cgi


class FormHandler:

    FIELD_IS_NOT_SET = "Field is not set"

    def __init__(self):
        self.first = ""
        self.second = ""
        self.subject_one = []
        self.subject_two = ""

    def parse_form(self):
        form = cgi.FieldStorage()

        self.first = form.getfirst("first", self.FIELD_IS_NOT_SET)
        self.second = form.getfirst("second", self.FIELD_IS_NOT_SET)

        fields_count = int(form.getfirst("fields_count"))

        self.subject_one = [form.getfirst(f"subject_one_{i}", None) for i in range(1, fields_count)]

        print(self.subject_one)
        self.subject_two = form.getfirst("subject_two", self.FIELD_IS_NOT_SET)

    def render_response(self):
        print("Content-type: text/html\n")
        print("""<!DOCTYPE HTML>
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>Обробка даних форми</title>
                </head>
                <body>""")

        print("<h1>Обробка даних форми!</h1>")
        print(f"<p>First: {self.first}</p>")
        print(f"<p>Second: {self.second}</p>")
        print(f"<p>First subject: {', '.join(self.subject_one)}</p>")
        print(f"<p>Second subject: {self.subject_two}</p>")

        print("""</body>
                </html>""")


handler = FormHandler()

handler.parse_form()
handler.render_response()
