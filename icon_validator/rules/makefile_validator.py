from .validator import KomandPluginValidator
import os
import subprocess


class MakefileValidator(KomandPluginValidator):

    @staticmethod
    def validate_tarball(target):
        l = ''.join(target)
        if '\trm -rf build' not in l:
            raise Exception('Makefile does not contain current tarball target: rm -rf build.')
        if '\trm -rf $(PKG)' not in l:
            raise Exception('Makefile does not contain current tarball target: rm -rf $(PKG).')
        if '\ttar -cvzf $(PKG) --exclude=$(PKG) --exclude=tests --exclude=run.sh *' not in l:
            raise Exception('Makefile does not contain current tarball target:'
                            ' tar -cvzf $(PKG) --exclude=$(PKG) --exclude=tests --exclude=run.sh *.')

    @staticmethod
    def validate_runner_old(target):
        if target.startswith('runner: $(NAME)'):
            raise Exception('Makefile contains old runner target: runner: $(NAME)')
        if target.startswith('$(NAME)-run:'):
            raise Exception('Makefile contains old runner target: $(NAME)-run')

    @staticmethod
    def validate_runner_new(target):
        l = ''.join(target)
        if '\t@ln -f -s ../tools/run.sh run.sh' not in l:
            raise Exception('Makefile does not contain current runner: @ln -f -s ../tools/run.sh run.sh.')

    @staticmethod
    def validate_regenerate(target):
        l = ''.join(target)
        if l == '\ticon-plugin generate python --regenerate' or '\ticon-plugin generate python --regenerate':
            pass
        else:
            raise Exception('Makefile does not contain current regenerate: icon-plugin generate python --regenerate.')


    @staticmethod
    def validate_python(target):
        l = ''.join(target)
        if 'python2' in l:
            raise Exception('Makefile does not contain current python intepreter: python.')


    @staticmethod
    def validate_validate(target):
        l = ''.join(target)
        if 'make -C ../ install-ci &> /dev/null && komand-plugin-ci validate' not in l:
            raise Exception(
                    'Makefile does not contain current validate target: \n'
                    '@test -d ../0_ci && make -C ../ install-ci &> /dev/null '
                    '&& komand-plugin-ci validate . || true'
                    )
        if 'mdl' not in l:
            raise Exception(
                    'Makefile does not contain current validate target: '
                    '@test -x ../tools/mdl.sh && ../tools/mdl.sh || true'
                    )
        if 'flake8.sh' not in l:
            raise Exception(
                    'Makefile does not contain current validate target: '
                    '@test -x ../tools/flake8.sh && ../tools/flake8.sh || true')
        if 'bandit.sh' not in l:
            raise Exception(
                    'Makefile does not contain current validate target: '
                    '@test -x ../tools/bandit.sh && ../tools/bandit.sh || true')

    @staticmethod
    def validate_syntax(path_to_makefile):
        result = subprocess.run(["make", "-n", "-C", path_to_makefile], capture_output=True)
        err = result.stderr.decode("utf-8").strip()
        if err is not "":
            raise Exception(f'Makefile not properly formatted: {err}')

    def validate(self, spec):
        d = spec.directory
        # MakefileValidator.validate_syntax(d)
        for i in spec.raw_makefile().split('\n\n'):
            line = i.split('\n')
            if line[0].startswith('runner:'):
                MakefileValidator.validate_runner_new(line)
            if line[0].startswith('runner: $(NAME)'):
                MakefileValidator.validate_runner_old(line)
            if line[0].startswith('$(NAME)-run:'):
                MakefileValidator.validate_runner_old(line)
            if line[0].startswith('validate:'):
                MakefileValidator.validate_validate(line)
            if os.path.isdir('{}/{}'.format(d, 'bin')) and not os.path.isdir('{}/{}'.format(d, 'connection')):
                # Python plugins
                if line[0].startswith('regenerate:'):
                    MakefileValidator.validate_regenerate(line)
            if line[0].startswith('tarball:'):
                MakefileValidator.validate_tarball(line)
            MakefileValidator.validate_python(line)
