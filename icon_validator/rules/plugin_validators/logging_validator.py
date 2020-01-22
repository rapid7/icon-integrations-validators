from icon_validator.rules.validator import KomandPluginValidator


class LoggingValidator(KomandPluginValidator):

    @staticmethod
    def validate_import_logging(section):
        logging_found = False
        logging_getlogger_found = False

        for f in section:
            if "import logging" in f:
                logging_found = True
            if "logging.getLogger" in f:
                logging_getlogger_found = True

        # logging is imported without presence of logging.GetLogger
        if logging_found and not logging_getlogger_found:
            raise Exception("One or more files imports logging, update to self.logger.")

    def validate(self, spec):
        # Logging update is only for Python plugins
        image = None
        for line in spec.raw_dockerfile():
            if line.startswith("FROM"):
                parent = line.replace("FROM", "").strip()
                parts = parent.split(":")
                image = parts[0].strip()
                break  # Only one FROM within a Dockerfile, so just exit early instead of continuing to loop

        if not image:
            raise Exception("No FROM statement found within the Dockerfile.")

        if image == "komand/go-plugin-2":
            return None
        elif image == "komand/go-plugin":
            raise Exception("Plugin is using a deprecated Go parent image.")

        LoggingValidator.validate_import_logging(spec.raw_trigger_files())
        LoggingValidator.validate_import_logging(spec.raw_action_files())
        LoggingValidator.validate_import_logging(spec.raw_connection_file())
        LoggingValidator.validate_import_logging(spec.raw_util_files())
