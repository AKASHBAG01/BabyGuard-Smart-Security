import modules.shared_frame as shared_frame


def get_status():

    frame = shared_frame.latest_frame

    return {
        "backend": "running",
        "camera": frame is not None,
        "message": "AI Baby Security System Running"
    }