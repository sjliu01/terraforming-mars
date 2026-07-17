#!/usr/bin/env python

import logging

import main
import yaml
from fastapi.openapi.utils import get_openapi

logger = logging.getLogger(__name__)

OUTPUT_PATH = "./src/lib/server/schema/openapi.yaml"

# Script to export schema to file
if __name__ == "__main__":
    schema = get_openapi(
        title=main.app.title,
        version=main.app.version,
        routes=main.app.routes,
    )

    # Export as YAML
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(schema, f, default_flow_style=False)

    logger.info(f"Schema exported to {OUTPUT_PATH}")
