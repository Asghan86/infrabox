import re
from builtins import int, range

from pyinfrabox import ValidationError
from pyinfrabox.utils import *

def special_match(strg, search=re.compile(r'[^a-z0-9_-]').search):
    return not bool(search(strg))

def check_name(n, path):
    check_text(n, path)
    if not special_match(n):
        raise ValidationError(path, "'%s' not a valid value" % n)


def parse_depends_on_condition(d, path):
    check_allowed_properties(d, path, ("job", "on"))
    check_required_properties(d, path, ("job", "on"))
    check_name(d['job'], path + '.job')

    on = d['on']
    if not isinstance(on, list):
        raise ValidationError(path + ".on", "must be a list")

    if not on:
        raise ValidationError(path + ".on", "must not be empty")


    on_used = {}
    for i in on:
        if i not in ('finished', 'error', 'failure', '*'):
            raise ValidationError(path + ".on", "%s is not a valid value" % i)

        if i in on_used:
            raise ValidationError(path + ".on", "%s used twice" % i)

        on_used[i] = True


def parse_depends_on(a, path):
    if not isinstance(a, list):
        raise ValidationError(path, "must be an list")

    if not a:
        raise ValidationError(path, "must not be empty")

    for i in range(0, len(a)):
        n = a[i]
        p = '[%s]' % i

        if isinstance(n, dict):
            # contains conditions
            parse_depends_on_condition(n, path + p)
        else:
            # no conditions, default to 'finished'
            check_name(n, path + p)

def check_version(v, path):
    if not isinstance(v, int):
        raise ValidationError(path, "must be an int")

    if v != 1:
        raise ValidationError(path, "unsupported version")

def parse_build_args(e, path):
    if not isinstance(e, dict):
        raise ValidationError(path, "must be an object")

    for key in e:
        value = e[key]
        p = path + "." + key
        check_text(value, p)

def parse_secret_ref(value, p):
    if not isinstance(value, dict):
        raise ValidationError(p, "must be an object")

    if "$secret" not in value:
        raise ValidationError(p, "must contain a $secret")

    check_text(value['$secret'], p + ".$secret")

def parse_environment(e, path):
    if not isinstance(e, dict):
        raise ValidationError(path, "must be an object")

    for key in e:
        value = e[key]
        p = path + "." + key

        if isinstance(value, dict):
            parse_secret_ref(value, p)
        else:
            try:
                check_text(value, p)
            except:
                raise ValidationError(p, "must be a string or object")


def parse_git(d, path):
    check_allowed_properties(d, path, ("type", "name", "commit", "clone_url", "depends_on", "environment"))
    check_required_properties(d, path, ("type", "name", "commit", "clone_url"))
    check_name(d['name'], path + ".name")
    check_text(d['commit'], path + ".commit")
    check_text(d['clone_url'], path + ".clone_url")

    if 'depends_on' in d:
        parse_depends_on(d['depends_on'], path + ".depends_on")

    if 'environment' in d:
        parse_environment(d['environment'], path + ".environment")

def parse_workflow(d, path):
    check_allowed_properties(d, path, ("type", "name", "infrabox_file", "depends_on"))
    check_required_properties(d, path, ("type", "name", "infrabox_file"))
    check_name(d['name'], path + ".name")
    check_text(d['infrabox_file'], path + ".infrabox_file")

    if 'depends_on' in d:
        parse_depends_on(d['depends_on'], path + ".depends_on")

def parse_limits(d, path):
    check_allowed_properties(d, path, ("memory", "cpu"))
    check_required_properties(d, path, ("memory", "cpu"))

    check_number(d['cpu'], path + ".cpu")
    check_number(d['memory'], path + ".memory")

    if d['cpu'] <= 0:
        raise ValidationError(path + ".cpu", "must be greater than 0")

    if d['memory'] <= 255:
        raise ValidationError(path + ".memory", "must be greater than 255")

def parse_kubernetes_limits(d, path):
    check_allowed_properties(d, path, ("memory", "cpu"))
    check_required_properties(d, path, ("memory", "cpu"))

    check_number(d['cpu'], path + ".cpu")
    check_number(d['memory'], path + ".memory")

    if d['cpu'] <= 0:
        raise ValidationError(path + ".cpu", "must be greater than 0")

    if d['memory'] <= 255:
        raise ValidationError(path + ".memory", "must be greater than 255")

def parse_add_capabilities(d, path):
    check_string_array(d, path)

def parse_capabilities(d, path):
    check_allowed_properties(d, path, ('add',))

    if 'add' in d:
        parse_add_capabilities(d['add'], path + '.add')

def parse_security_context(d, path):
    check_allowed_properties(d, path, ('capabilities',))

    if 'capabilities' in d:
        parse_capabilities(d['capabilities'], path + '.capabilities')

def parse_resources_kubernetes(d, path):
    check_allowed_properties(d, path, ('limits',))
    check_required_properties(d, path, ("limits",))

    parse_kubernetes_limits(d['limits'], path + ".limits")

def parse_resources(d, path):
    check_allowed_properties(d, path, ("limits", "kubernetes"))
    check_required_properties(d, path, ("limits",))

    parse_limits(d['limits'], path + ".limits")

def parse_docker(d, path):
    check_allowed_properties(d, path, ("type", "name", "docker_file", "depends_on", "resources",
                                       "build_only", "keep", "environment",
                                       "build_arguments", "deployments", "timeout", "security_context"))
    check_required_properties(d, path, ("type", "name", "docker_file", "resources"))
    check_name(d['name'], path + ".name")
    check_text(d['docker_file'], path + ".docker_file")
    parse_resources(d['resources'], path + ".resources")

    if 'build_only' in d:
        check_boolean(d['build_only'], path + ".build_only")

    if 'keep' in d:
        check_boolean(d['keep'], path + ".keep")

    if 'depends_on' in d:
        parse_depends_on(d['depends_on'], path + ".depends_on")

    if 'environment' in d:
        parse_environment(d['environment'], path + ".environment")

    if 'build_arguments' in d:
        parse_build_args(d['build_arguments'], path + ".build_arguments")

    if 'deployments' in d:
        parse_deployments(d['deployments'], path + ".deployments")

    if 'timeout' in d:
        check_number(d['timeout'], path + ".timeout")

    if 'security_context' in d:
        parse_security_context(d['security_context'], path + '.security_context')

def parse_docker_compose(d, path):
    check_allowed_properties(d, path, ("type", "name", "docker_compose_file", "depends_on", "environment", "resources"))
    check_required_properties(d, path, ("type", "name", "docker_compose_file", "resources"))
    check_name(d['name'], path + ".name")
    check_text(d['docker_compose_file'], path + ".docker_compose_file")
    parse_resources(d['resources'], path + ".resources")

    if 'depends_on' in d:
        parse_depends_on(d['depends_on'], path + ".depends_on")

    if 'environment' in d:
        parse_environment(d['environment'], path + ".environment")

def parse_wait(d, path):
    check_allowed_properties(d, path, ("type", "name", "depends_on"))
    check_required_properties(d, path, ("type", "name"))
    check_name(d['name'], path + ".name")

    if 'depends_on' in d:
        parse_depends_on(d['depends_on'], path + ".depends_on")

def parse_deployment_docker_registry(d, path):
    check_allowed_properties(d, path, ("type", "host", "repository", "username", "password", "tag"))
    check_required_properties(d, path, ("type", "host", "repository"))
    check_text(d['host'], path + ".host")
    check_text(d['repository'], path + ".repository")

    if 'username' in d:
        check_text(d['username'], path + ".username")

    if 'tag' in d:
        check_text(d['tag'], path + ".tag")

    if 'password' in d:
        parse_secret_ref(d['password'], path + ".password")

def parse_deployments(e, path):
    if not isinstance(e, list):
        raise ValidationError(path, "must be an array")

    if not e:
        raise ValidationError(path, "must not be empty")

    for i in range(0, len(e)):
        elem = e[i]
        p = "%s[%s]" % (path, i)

        if 'type' not in elem:
            raise ValidationError(p, "does not contain a 'type'")

        t = elem['type']

        if t == 'docker-registry':
            parse_deployment_docker_registry(elem, p)
        else:
            raise ValidationError(p, "type '%s' not supported" % t)


def parse_jobs(e, path):
    if not isinstance(e, list):
        raise ValidationError(path, "must be an array")

    if not e:
        raise ValidationError(path, "must not be empty")

    for i in range(0, len(e)):
        elem = e[i]
        p = "%s[%s]" % (path, i)

        if 'type' not in elem:
            raise ValidationError(p, "does not contain a 'type'")

        t = elem['type']

        if t == 'git':
            parse_git(elem, p)
        elif t == 'wait':
            parse_wait(elem, p)
        elif t == 'workflow':
            parse_workflow(elem, p)
        elif t == 'docker':
            parse_docker(elem, p)
        elif t == 'docker-compose':
            parse_docker_compose(elem, p)
        else:
            raise ValidationError(p, "type '%s' not supported" % t)

def parse_document(d):
    check_allowed_properties(d, "#", ("version", "jobs"))
    check_required_properties(d, "#", ("version", "jobs"))

    check_version(d['version'], "#version")

    if 'jobs' in d:
        parse_jobs(d['jobs'], "#jobs")

def validate_json(d):
    parse_document(d)

    if 'jobs' not in d:
        return True

    jobs = {}
    for i in range(0, len(d['jobs'])):
        job = d['jobs'][i]
        job_name = job['name']

        path = "#jobs[%s]" % i

        if jobs.get(job_name, None):
            raise ValidationError(path + ".name", "Job name '%s' already exists" % job_name)

        if job_name == 'Create Jobs':
            raise ValidationError(path + ".name", "Job name may not be 'Create Jobs'")

        jobs[job_name] = job

        if 'depends_on' not in job:
            continue

        deps = {}
        for depends_on in job['depends_on']:
            parent_name = None

            if isinstance(depends_on, dict):
                parent_name = depends_on['job']
            else:
                parent_name = depends_on

            if job_name == parent_name:
                raise ValidationError(path, "Job '%s' may not depend on itself" % parent_name)

            if parent_name not in jobs:
                raise ValidationError(path + ".depends_on", "Job '%s' not found" % parent_name)

            if parent_name in deps:
                raise ValidationError(path + ".depends_on", "'%s' duplicate dependencies" % parent_name)

            deps[parent_name] = True

    return True
