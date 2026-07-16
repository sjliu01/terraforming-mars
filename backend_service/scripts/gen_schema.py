#!/usr/bin/env python

import json
import logging
import os
import yaml

from fastapi.openapi.utils import get_openapi

from main import app

logger = logging.getLogger(__name__)

OUTPUT_PATH = "./schema/"

# Script to export schema to file
if __name__ == "__main__":
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # Export as JSON
    with open(os.path.join(OUTPUT_PATH, "openapi.json"), "w") as f:
        json.dump(schema, f, indent=2)

    # Export as YAML
    with open(os.path.join(OUTPUT_PATH, "openapi.yaml"), "w") as f:
        yaml.dump(schema, f, default_flow_style=False)

    logger.info("Schema exported to openapi.json and openapi.yaml")

