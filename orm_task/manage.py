if __name__ == '__main__':
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from orm_task.app.application import App
    App().getManager().run()
