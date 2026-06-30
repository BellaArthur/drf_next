
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    page_size              = 10
    page_size_query_param  = 'page_size'
    max_page_size          = 100

    def get_paginated_response(self, data):
        return Response({
            'status':  'success',
            'message': 'Data retrieved successfully',
            'data': {
                'count':     self.page.paginator.count,
                'pages':     self.page.paginator.num_pages,
                'next':      self.get_next_link(),
                'previous':  self.get_previous_link(),
                'results':   data,
            }
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'status':  {'type': 'string'},
                'message': {'type': 'string'},
                'data': {
                    'type': 'object',
                    'properties': {
                        'count':    {'type': 'integer'},
                        'pages':    {'type': 'integer'},
                        'next':     {'type': 'string', 'nullable': True},
                        'previous': {'type': 'string', 'nullable': True},
                        'results':  schema,
                    }
                }
            }
        }



class APIResponse:
    
    @staticmethod
    def success(data=None, message='Success', status_code=200):
        from rest_framework import status
        response = {
            'status':  'success',
            'message': message,
        }
        if data is not None:
            response['data'] = data
        return Response(response, status=status_code)

    @staticmethod
    def error(message='An error occurred', errors=None, status_code=400):
        from rest_framework import status
        response = {
            'status':  'error',
            'message': message,
        }
        if errors is not None:
            response['errors'] = errors
        return Response(response, status=status_code)


