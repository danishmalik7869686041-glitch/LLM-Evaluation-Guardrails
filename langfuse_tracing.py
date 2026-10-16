
import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

def create_trace(name: str, input_data: dict):
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST")

    if not public_key or not secret_key or not host:
        print("Langfuse keys/host missing; trace skipped.")
        return None

    try:
        client = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host,
        )

        trace = client.start_span(
            name=name,
            input=input_data,
        )
        return client, trace

    except Exception as error:
        print(f"Langfuse trace could not start: {error}")
        return None
