if __name__ == '__main__':
    from app import app
    from app import controller

    app = app.App()
    app.addConfiguration({
        'SECRET_KEY': 'secret',
        'WTF_CSRF_ENABLE': True
    })

    app.getApp().run(debug=True)
