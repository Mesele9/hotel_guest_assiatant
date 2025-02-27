import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guest_assistant.settings')

# Initialize the Django ASGI application early
django_application = get_asgi_application()

# Now that Django is initialized, import Channels and routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from chat import routing  # Your app-specific WebSocket routing

# Define the ASGI application with ProtocolTypeRouter
application = ProtocolTypeRouter({
    "http": django_application,  # Reuse the initialized Django application
    "websocket": SessionMiddlewareStack(  # Sessions first
        AuthMiddlewareStack(  # Then authentication
            URLRouter(routing.websocket_urlpatterns)  # Your WebSocket routes
        )
    ),
})