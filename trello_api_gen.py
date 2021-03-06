#!/usr/bin/python

import os
import re
import requests
import pystache

from urlparse import urljoin
from BeautifulSoup import BeautifulSoup as Soup

INDEX = 'https://developers.trello.com/templates/apis/advanced-reference.html'

METHOD_LOOKUP = {
    'GET': 'get',
    'PUT': 'update',
    'POST': 'new',
    'DELETE': 'delete',
}

def get_soup(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return Soup(resp.content)

def main():
    sections = get_sections()
    if not os.path.exists('trello'):
        os.mkdir('trello')
    for section in sections:
        write_section(section)

    with open(os.path.join('trello', '__init__.py'), 'wb') as fd:
        renderer = pystache.Renderer()
        trello_api = TrelloApi([module_name(section) for section in sections])
        fd.write(renderer.render(trello_api))

def get_sections():
    sections = []
    soup = get_soup(INDEX)

    ul = soup.find('div', {'class': 'api-ref-nav'}).ul
    for li in ul.findAll('li', recursive=False):
        href = li.a['href']
        href = href.replace('advanced-reference', 'templates/docs')
        sections.append(urljoin(INDEX, href + '.html'))
    return sections

def get_actions(section_url):
    actions = []
    soup = get_soup(section_url)

    for section in soup.findAll('div', {'class': 'section'}):
        try:
            method, url = [s.strip() for s in section.h2.findAll(text=True)][:2]
        except ValueError:
            continue

        args = []
        for li in section.ul.findAll('li', recursive=False):
            if 'arguments' in li.text.lower():
                args_ul = li.ul
                if args_ul:
                    for arg_li in args_ul.findAll('li', recursive=False):
                        arg = arg_li.code.text
                        required = 'required' in arg_li.text.lower()
                        args.append((arg, required))
        actions.append((method, url, args))
    return actions

def escape(variable):
    variable = variable.replace("/", "_")
    return variable

def function_args(url_args, id_arg, req_args, opt_args):
    if id_arg:
        req_args = [id_arg] + req_args
    return ', '.join(url_args + req_args + [escape(arg) + '=None' for arg in opt_args])

def request_args(request_type, req_args, opt_args):
    get_args = []
    post_args = []
    if request_type in ['GET', 'DELETE']:
        get_args += req_args
        get_args += opt_args
    else:
        post_args += req_args
        post_args += opt_args
    params = '{{{}}}'.format(', '.join(['"key": self._apikey', '"token": self._token'] + ['"{}": {}'.format(arg, arg) for arg in get_args]))
    data = '{{{}}}'.format(', '.join(['"{}": {}'.format(arg, escape(arg)) for arg in post_args])) if post_args else None
    return 'params={}, data={}'.format(params, data)

def module_name(section_url):
    module = section_url.split('/')[-1]
    module = module.split('.')[0]
    if module in ['search']:
        return module
    if module in ['batch']:
        return module + 'es'
    return module + 's'

def write_section(section_url):
    module = module_name(section_url)
    with open(os.path.join('trello', '{}.py'.format(module)), 'wb') as fd:
        renderer = pystache.Renderer(escape=lambda u: u)
        fd.write(renderer.render(ApiClass(section_url)))

class ApiClass(object):
    def __init__(self, section_url):
        super(ApiClass, self).__init__()
        self.module = module_name(section_url)
        self.actions = get_actions(section_url)

    def class_name(self):
        return self.module.title()

    def methods(self):
        methods = []
        for action in self.actions:
            url_parts = action[1].split('/')
            method_parts = [part.rstrip('s') for part in url_parts[3:] if not part.startswith('[')]
            method_name = '_'.join([METHOD_LOOKUP[action[0]]] + method_parts)
            id_arg = ([part.strip('[]').replace(' ', '_') for part in url_parts if part.startswith('[')] or [None])[0]
            url_args = [arg[0] for arg in action[2] if '[{}]'.format(arg[0]) in url_parts]
            if url_args:
                method_name = '{}_{}'.format(method_name, '_'.join(url_args))
            req_args = [arg[0] for arg in action[2] if arg[1] and arg[0] not in url_args]
            opt_args = [arg[0] for arg in action[2] if not arg[1]]
            def_args = function_args(url_args, id_arg, req_args, opt_args)
            args = request_args(action[0].upper(), req_args, opt_args)
            method = action[0].lower()
            url = '"https://trello.com{}".format({})'.format(re.sub(r'\[.*?\]', '{}', action[1]), ', '.join([id_arg] + url_args if id_arg else url_args))
            methods.append(dict(def_args=def_args, args=args, method=method, url=url, name=method_name))
        return methods

class TrelloApi(object):
    def __init__(self, sections):
        super(TrelloApi, self).__init__()
        self.sections = [{'module': section, 'class': section.title()} for section in sections]

if __name__ == '__main__':
    main()
