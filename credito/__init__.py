# from server import app
import os


def run_server():
    import uvicorn

    uvicorn.run(
        "credito.server:app",
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 9000)),
        # reload=True,
    )
