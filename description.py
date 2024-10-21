from .assertion import PytrunAssertionError 

def description(message):
    def inner_decorator(fn):
        def inner(*args, **kwargs):
            error = None 

            try:
               fn(*args, **kwargs)

            except PytrunAssertionError as e:
                error = { "type": "PytrunAssertionError", "message": e.message }

            except AssertionError as e:
                error = { "type": "AssertionError" }
              
            except Exception as error:
                error = { "type": "Exception" }

            return [message, error]
        return inner
    return inner_decorator

