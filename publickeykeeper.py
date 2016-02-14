import os
from base import app

os.environ["DIAG_CONFIG_MODULE"] = "config.prod"
if __name__ == '__main__':
    app.run()
