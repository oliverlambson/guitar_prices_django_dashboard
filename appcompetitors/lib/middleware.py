import sys
from django.conf import settings
from django.db import connection
from django.utils import termcolors


class QueryPrintingMiddleware:
    """
    Prints the number of database queries for every request/response.

    This class is a modified version of the middleware source found at:
    http://www.szotten.com/david/show-number-of-queries-in-runserver-output.html

    The code is nearly identical but has been updated to comply with the new
    Django middleware format.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        start = None

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if settings.DEBUG:
            self.start = len(connection.queries)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if settings.DEBUG and 'runserver' in sys.argv and self.start is not None:
            red = termcolors.make_style(opts=('bold',), fg='red')
            yellow = termcolors.make_style(opts=('bold',), fg='yellow')

            count = len(connection.queries) - self.start
            output = '# queries: %s' % count
            output = output.ljust(15)

            # add some colour
            if count > 100:
                output = red(output)
            elif count > 10:
                output = yellow(output)

            # runserver just prints its output to sys.stderr, so follow suite
            sys.stderr.write(output)

        return response
