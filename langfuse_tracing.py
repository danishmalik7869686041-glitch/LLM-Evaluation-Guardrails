
import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def create_trace(name: str, input_data: dict):
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST")

    if not public_key or not secret_key or not host:
        return None

    client = None

    try:
        client = Langfuse(
            public_key=public_key,
            secret_key=secret_key,
            host=host,
            timeout=2.0,
        )

        span = client.start_observation(
            name=name,
            input=input_data,
            as_type="span",
        )

        return client, span

    except Exception as error:
        if client:
            try:
                client.shutdown()
            except Exception:
                pass

        print(f"Langfuse trace could not start: {error}")
        return None
