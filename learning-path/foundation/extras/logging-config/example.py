"""logging config example."""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("foundation.logging")


if __name__ == "__main__":
    logger.info("service_boot")
    logger.warning("retrying_external_call")
