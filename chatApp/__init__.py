from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    # config.add_route('send','/send/{first}')
    # config.add_route('message','/message')
    config.add_route('chatbox','/chatbox/{name}')
    config.add_route('history','/history/{name}')
    # config.add_route('send','/send')
    config.scan('.views')
    return config.make_wsgi_app()
