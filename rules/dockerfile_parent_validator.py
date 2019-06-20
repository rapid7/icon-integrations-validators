from .validator import KomandPluginValidator


class DockerfileParentValidator(KomandPluginValidator):
    def validate(self, spec):
        spec_str = ''.join(spec.raw_dockerfile())

        valid_images = [
          'komand/go-plugin-2', 'komand/python-2-plugin', 'komand/python-3-plugin', 'komand/python-pypy3-plugin', 
          'komand/python-3-slim-plugin', 'komand/python-2-slim-plugin',
          'komand/python-2-27-slim-plugin', 'komand/python-3-37-slim-plugin', 'komand/python-2-27-plugin', 'komand/python-3-37-plugin',
          'komand/python-2-27-full-plugin', 'komand/python-pypy3-full-plugin'
        ]
        root_spec_found = False
        for line in spec.raw_dockerfile():
            if line.startswith('FROM'):
                parent = line.replace('FROM', '').strip()
                parts = parent.split(':')
                image = parts[0].strip()
                if image == 'komand/python-plugin':
                    raise Exception('Parent Dockerfile komand/python-plugin is no longer supported. '
                                    'Use komand/python-2-plugin, komand/python-3-plugin, or komand/python-pypy3-plugin instead.')
                elif image == 'komand/go-plugin':
                    raise Exception('Parent Dockerfile komand/go-plugin is no longer supported. '
                                    'Use komand/go-plugin-2 instead.')
                elif image not in valid_images:
                    raise Exception('Unrecognized parent Dockerfile')
            if line.startswith('ADD ./plugin.spec.yaml /plugin.spec.yaml'):
                root_spec_found = True

        # Komand code checks for /plugin.spec.yaml in the plugin container
        if not root_spec_found:
            raise Exception('Dockerfile missing line: ADD ./plugin.spec.yaml /plugin.spec.yaml')
