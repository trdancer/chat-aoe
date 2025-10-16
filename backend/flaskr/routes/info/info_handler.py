from flask import current_app, request, g

@current_app.route(f'/info')
def info():
    return {
        "patch": "85208",
        "api": "v1"
    }