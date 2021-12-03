#!/usr/bin/env python

import jinja2 as jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from pathlib import Path


def load_data(file):
  # Opening JSON file
  f = open(file)

  # returns JSON object as
  # a dictionary
  data = json.load(f)

  # Closing file
  f.close()

  return data


def write_to_file(filename, data):
  file_path = f'../src/{filename}'
  file = open(file_path, "w")
  file.write(data)
  file.close()

  return print(f'file saved to {file_path}')


def create_index(templateEnv):
  data = load_data('data.json')
  template = templateEnv.get_template('index.html.j2')
  menu = [{'title': 'Bio', 'link': '/info.html'}]
  file = template.render(containers=data['containers'], menu=menu)  # this is where to put args to the template renderer

  write_to_file('index.html', file)


def create_project_pages(templateEnv, data):
  menu = [{'title': 'Bio', 'link': '/info.html'}]
  for project in data['projects']:
    template = templateEnv.get_template('project.html.j2')
    file = template.render(project=project, data=data['projects'], menu=menu)
    write_to_file(f"{project['url']}.html", file)


def create_filter_pages(templateEnv, data):
  filters = []
  projects = data['projects']
  menu = [{'title': 'Bio', 'link': '/info.html'}]

  # Path("../src/filter").mkdir(parents=True, exist_ok=True)

  for project in projects:
    tags = project['tags']
    filters.extend(tags)
  filters = list(set(filters))

  filter_pages = {}
  for filter_page in filters:
    filter_pages[f'{filter_page}'] = []

  for page in filter_pages:
    for project in projects:
      if page in project['tags']:
        # if filter_pages[f'"{filter_page}"'] not in filter_pages:
        filter_pages[f'{page}'].append(project)
        # else:
        #   filter_pages[f'{filter_page}'].extend(project)
        # filter_pages.append(f'{filter_page}')

  for page in filter_pages:
    template = templateEnv.get_template('index.html.j2')
    file = template.render(data=filter_pages[page], menu=menu)  # this is where to put args to the template renderer

    write_to_file(f'{page}.html', file)


def create_info_page(templateEnv, data):
  # for project in data['projects']:
  template = templateEnv.get_template('info.html.j2')
  menu = [{'title': 'Home', 'link': '/index.html'}]
  file = template.render(data=data['projects'], menu=menu)
  write_to_file(f"info.html", file)


def main():


  # print(data)

  templateLoader = FileSystemLoader(searchpath='./templates')
  templateEnv = Environment(
    loader=templateLoader,
    autoescape=True,
  )

  create_index(templateEnv)

  # create_project_pages(templateEnv, data)

  # create_info_page(templateEnv, data)
  # create_filter_pages(templateEnv, data)


if __name__ == '__main__':
  main()
