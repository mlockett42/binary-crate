from __future__ import absolute_import, print_function
from cavorite import c, t, Router
from cavorite.HTML import *
import js
import copy
from .navigation import BCChrome

def projectdropdownitem(title, data_target, projectname, redraw_function):
    source = None
    def modaltrigger(e):
        global project_name
        project_name = projectname
        source.get_root().mount_redraw()
        jquery = js.globals['$']
        jquery(data_target).modal()
    source = li([a({'data-toggle': "modal", 'data-target': data_target, 'href': get_current_hash(), 'onclick': modaltrigger}, [t(title), ]), ])
    return source


projects = ['Pong Game', 'Resume Website', 'Twitter Clone', 'Website', 'Python Functions', 'Space Invaders']

class Project(div):
    def __init__(self, title):
        self.title = title
        super(Project, self).__init__(cssClass="col-md-3 col-sm-4")

    def get_children(self):
        ret = [
          div(cssClass="wrimagecard wrimagecard-topimage", children=[
            div(cssClass="wrimagecard-topimage_header", style="background-color: rgba(51, 105, 232, 0.1)", children=[
              center([i(cssClass="fa fa-code fa-5x", style="color:#3369e8")]),
            ]),
            div(cssClass="wrimagecard-topimage_title", children=[
              div(cssClass='dropdown', children=[
              li({'class': "fa fa-pencil fa-lg edit", 'id': "menu1", 'data-toggle': "dropdown"}),
                ul({'class': "dropdown-menu", 'role': "menu", 'aria-labelledby':"menu1"}, [
                  projectdropdownitem('Rename', "#renameProj", self.title, self.get_root().mount_redraw),
                  projectdropdownitem('Share', "#shareProj", self.title, self.get_root().mount_redraw),
                  projectdropdownitem('Delete', "#deleteProj", self.title, self.get_root().mount_redraw),
                ]),
              ]),
              p(self.title),
            ]),
          ]),
        ]
        ret[0].parent = self
        return ret

def projectsfn():
    return [Project(projname) for projname in projects]

body = js.globals.document.body

def get_current_hash():
    return str(js.globals.window.location.hash)

class ModalTrigger(a):
    def __init__(self, attribs, children, target):
        attribs = copy.copy(attribs)
        attribs.update({'data-toggle': "modal", 'data-target': target, 'href': get_current_hash()})
        super(ModalTrigger, self).__init__(attribs, children)


class Modal(div):
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        super(Modal, self).__init__({'class': "modal fade", "id":id, "tabindex": "-1", "role": "dialog", "aria-labeledby": "{}Label".format(id), "aria-hidden": "true"})

    def get_children(self):
        return  [
                  div({'class': "modal-dialog", "role": "document"}, [
                    div({'class': 'modal-content'}, [
                      div({'class': 'modal-header'}, [
                        h5({'class': 'modal-title', 'id':  "{}Label".format(self.id)}, self.title),
                        html_button({'type': 'button', 'class': 'close', 'data-dismiss': 'modal', 'aria-label': 'Close'}, [
                          span({'aria-hidden': 'true'}, 'X'),
                        ]),
                      ]),
                      div({'class': 'modal-body'}, [
                        form(self.body)
                      ]),
                      div({'class': 'modal-footer'}, [
                        html_button({'type': "button", 'class':"btn btn-secondary", 'data-dismiss':"modal"}, 'Cancel'),
                        html_button({'type': "button", 'class':"btn btn-primary"}, 'OK'),
                      ]),
                    ]),
                  ]),
                ]

project_name = 'No Project'

def get_project_name():
    return project_name

dashboard_view = BCChrome([
                      li({'class': 'nav-item li-create-new'}, [
                        form({'action': '#'}, [
                          ModalTrigger({'class': "btn btn-default navbar-btn crt-btn"}, "Create New", "#createNew"),
                        ]),
                      ]),
                    ],
                    projectsfn,
                    [
                      Modal("deleteProj", "Delete Project", [
                        p({'class': 'text-center'}, [
                          t("Are you sure you want to delete "),
                          strong([t(get_project_name)]),
                          t(", this will also delete all projects and data."),
                        ]),
                      ]),
                      Modal("renameProj", "Rename Project", [
                        form([
                          div({'class': 'form-group'}, [
                            label({'class':"col-form-label", 'for':"formGroupExampleInput"}, 'Title'),
                            html_input({'type': "text", 'class':"form-control", 'id':"formGroupExampleInput", 'value':get_project_name}),
                          ]),
                          div({'class': 'form-group'}, [
                            label({'for':"exampleFormControlTextarea1"}, 'Description'),
                            textarea({'class': "form-control", 'id': "exampleFormControlTextarea1", 'rows':"3"}),
                          ]),
                        ]),
                      ]),
                      Modal("shareProj", "Share Project", [
                        form([
                          div({'class': 'form-group'}, [
                            label({'class':"col-form-label", 'for':"formGroupExampleInput"}, 'Title'),
                            html_input({'type': "text", 'class':"form-control", 'id':"formGroupExampleInput", 'placeholder':"http://bc.com/o82Ssdms/"}),
                          ]),
                          div({'class': 'form-group'}, [
                            label({'for':"exampleFormControlTextarea1"}, 'Share On:'),
                            i({'class': 'fa fa-facebook', 'aria-hidden': 'true'}),
                            i({'class': 'fa fa-twitter', 'aria-hidden': 'true'}),
                            i({'class': 'fa fa-envelope-o', 'aria-hidden': 'true'}),
                          ]),
                        ]),
                      ]),
                    ])
                    


