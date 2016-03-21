#Deal with > 1.8 as per https://github.com/django/django/pull/3902/commits/b2b3b7f5f2d45d567e1aea9842a719a44fbc9235
#from django.http.response import REASON_PHRASES as STATUS_CODE_TEXT
######################################################################################################################
#That didn't work (I think because I need a fresher Django) so I'm going to just import it raw
#as per : https://github.com/jdufresne/django/blob/a9aec1154e5b65fcaf608801905a1bbafcfbfbf7/django/http/response.py
REASON_PHRASES = {
    100: 'CONTINUE',
    101: 'SWITCHING PROTOCOLS',
    102: 'PROCESSING',
    200: 'OK',
    201: 'CREATED',
    202: 'ACCEPTED',
    203: 'NON-AUTHORITATIVE INFORMATION',
    204: 'NO CONTENT',
    205: 'RESET CONTENT',
    206: 'PARTIAL CONTENT',
    207: 'MULTI-STATUS',
    208: 'ALREADY REPORTED',
    226: 'IM USED',
    300: 'MULTIPLE CHOICES',
    301: 'MOVED PERMANENTLY',
    302: 'FOUND',
    303: 'SEE OTHER',
    304: 'NOT MODIFIED',
    305: 'USE PROXY',
    306: 'RESERVED',
    307: 'TEMPORARY REDIRECT',
    308: 'PERMANENT REDIRECT',
    400: 'BAD REQUEST',
    401: 'UNAUTHORIZED',
    402: 'PAYMENT REQUIRED',
    403: 'FORBIDDEN',
    404: 'NOT FOUND',
    405: 'METHOD NOT ALLOWED',
    406: 'NOT ACCEPTABLE',
    407: 'PROXY AUTHENTICATION REQUIRED',
    408: 'REQUEST TIMEOUT',
    409: 'CONFLICT',
    410: 'GONE',
    411: 'LENGTH REQUIRED',
    412: 'PRECONDITION FAILED',
    413: 'REQUEST ENTITY TOO LARGE',
    414: 'REQUEST-URI TOO LONG',
    415: 'UNSUPPORTED MEDIA TYPE',
    416: 'REQUESTED RANGE NOT SATISFIABLE',
    417: 'EXPECTATION FAILED',
    418: "I'M A TEAPOT",
    422: 'UNPROCESSABLE ENTITY',
    423: 'LOCKED',
    424: 'FAILED DEPENDENCY',
    426: 'UPGRADE REQUIRED',
    428: 'PRECONDITION REQUIRED',
    429: 'TOO MANY REQUESTS',
    431: 'REQUEST HEADER FIELDS TOO LARGE',
    500: 'INTERNAL SERVER ERROR',
    501: 'NOT IMPLEMENTED',
    502: 'BAD GATEWAY',
    503: 'SERVICE UNAVAILABLE',
    504: 'GATEWAY TIMEOUT',
    505: 'HTTP VERSION NOT SUPPORTED',
    506: 'VARIANT ALSO NEGOTIATES',
    507: 'INSUFFICIENT STORAGE',
    508: 'LOOP DETECTED',
    510: 'NOT EXTENDED',
    511: 'NETWORK AUTHENTICATION REQUIRED',
}
STATUS_CODE_TEXT = REASON_PHRASES
######################################################################################################################


#https://gist.github.com/Suor/7870909

import re, logging
from django.conf import settings
#from django.core.handlers.wsgi import STATUS_CODE_TEXT


req_handler = logging.FileHandler(settings.BASE_DIR + '/logs/requests.log')
print(settings.BASE_DIR + '/logs/requests.log')
req_handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(message)s')
req_handler.setFormatter(formatter)

req_log = logging.getLogger('requests')
req_log.propagate = False
req_log.addHandler(req_handler)


def log_cond(request):
    #Everything at the moment
    return True

class HeadersLoggingMiddleware(object):
    def process_response(self, request, response):
        if log_cond(request):
            print("In HeadersLoggingMiddleware A")
            keys = sorted(filter(lambda k: re.match(r'(HTTP_|CONTENT_)', k), request.META))
            keys = ['REMOTE_ADDR'] + keys
            meta = ''.join("%s=%s\n" % (k, request.META[k]) for k in keys)

            try:
                status_text = STATUS_CODE_TEXT[response.status_code]
            except KeyError:
                status_text = 'UNKNOWN STATUS CODE'
            status = '%s %s' % (response.status_code, status_text)
            response_headers = [(str(k), str(v)) for k, v in response.items()]
            for c in response.cookies.values():
                response_headers.append(('Set-Cookie', str(c.output(header=''))))
            headers = ''.join("%s: %s\n" % c for c in response_headers)
            print("In HeadersLoggingMiddleware B")
            print('"%s %s\n%s\n%s\n%s' % (request.method, request.build_absolute_uri(), meta,
                                                 status, headers))
            req_log.info('"%s %s\n%s\n%s\n%s' % (request.method, request.build_absolute_uri(), meta,
                                                 status, headers))
            print("In HeadersLoggingMiddleware C")
        return response

