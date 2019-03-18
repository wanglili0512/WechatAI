from flask_script import Manager

from app import create_app
my_app = create_app()

manager = Manager(my_app)

if __name__ == '__main__':
    manager.run()
