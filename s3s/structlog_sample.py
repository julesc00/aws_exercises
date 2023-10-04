import structlog

log = structlog.get_logger()
print(log.info("hello world", key="value"))
