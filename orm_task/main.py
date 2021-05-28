if __name__ == '__main__':
    from app import app
    from app import views

    # app.App().getDb().create_all()
    app.App().getApp().run(debug=True)
