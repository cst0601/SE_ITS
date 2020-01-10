def success(payload = ""):
    return {"info": "success",
            "payload": payload}

def failure(payload = ""):
    return {"info": "failure",
            "payload": payload}

def redirect(location):
    location = str(location)
    if location[0] != "/":
        location = "/" + location
    return {"info": "redirect",
            "location": location}
