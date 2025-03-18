def success_response(data, status=200):
    return {"status": "success", "result": data}, status

def error_response(message, status=400):
    return {"status": "error", "message": message}, status

def unexpected_error_response(message, status=500):
    return {"status": "error", "message": message}, status
