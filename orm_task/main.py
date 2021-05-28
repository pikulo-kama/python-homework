if __name__ == '__main__':
    from app import application
    from app import views

    # app.App().getDb().create_all()
    application.App().getApp().run(debug=True)
