import settings
from app import app


def flask(config):
    app.run(host=config.HOST, port=int(config.PORT), debug=False)


def main():
    config = settings.load_config()
    flask(config=config)


if __name__ == "__main__":
    main()
