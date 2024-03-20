from dosei_sdk import Dosei

port = 8080
dosei = Dosei(
    name="fastapi",
    port=port,
    run=f"uvicorn helloworld.main:app --host 0.0.0.0 --port {port}"
)
