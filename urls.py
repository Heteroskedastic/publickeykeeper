from flask import Blueprint


def register_api_urls(app):
    from api.serverapi.v0 import VApiCore, VVerify, VGetPubKey, VMessageDecrypt, VMessageEncrypt

    api_pages = Blueprint(
        'api',
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    api_pages.add_url_rule('/api', view_func=VApiCore.as_view('api'))
    api_pages.add_url_rule('/api/verify', view_func=VVerify.as_view('api-verify'))
    api_pages.add_url_rule('/api/get-key', view_func=VGetPubKey.as_view('api-get-key'))
    api_pages.add_url_rule('/api/message/encrypt', view_func=VMessageEncrypt.as_view('api-message-encrypt'), methods=['POST'])
    api_pages.add_url_rule('/api/message/decrypt', view_func=VMessageDecrypt.as_view('api-message-decrypt'), methods=['POST'])
    app.register_blueprint(api_pages)


def register_base_urls(app):
    from base.views import VVerify
    views_pages = Blueprint(
        'base',
        __name__,
        template_folder='templates',
        static_folder='static'
    )
    views_pages.add_url_rule('/test/verify', view_func=VVerify.as_view('views'), )
    app.register_blueprint(views_pages)
