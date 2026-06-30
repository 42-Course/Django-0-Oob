#!/usr/bin/python3
from elem import Elem, Text
from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                      Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)


class Page:
    """Wraps a tree of Elem and validates / renders it."""

    TAG_CLASSES = {
        'html': Html, 'head': Head, 'body': Body, 'title': Title,
        'meta': Meta, 'img': Img, 'table': Table, 'th': Th, 'tr': Tr,
        'td': Td, 'ul': Ul, 'ol': Ol, 'li': Li, 'h1': H1, 'h2': H2,
        'p': P, 'div': Div, 'span': Span, 'hr': Hr, 'br': Br,
    }

    def __init__(self, root):
        if not isinstance(root, Elem):
            raise TypeError("Page root must inherit from Elem.")
        self.root = root

    def _kind(self, node):
        if type(node) == Text:
            return 'text'
        for tag, cls in Page.TAG_CLASSES.items():
            if type(node) == cls:
                return tag
        return None

    def is_valid(self, elem=None):
        if elem is None:
            elem = self.root
        if type(elem) == Text:
            return True
        kind = self._kind(elem)
        if kind is None:
            return False

        children = elem.content
        child_kinds = [self._kind(c) for c in children]
        if None in child_kinds:
            return False

        if kind == 'html':
            if child_kinds != ['head', 'body']:
                return False
        elif kind == 'head':
            if child_kinds != ['title']:
                return False
        elif kind in ('body', 'div'):
            allowed = {'h1', 'h2', 'div', 'table', 'ul', 'ol', 'span', 'text'}
            if not all(k in allowed for k in child_kinds):
                return False
        elif kind in ('title', 'h1', 'h2', 'li', 'th', 'td'):
            if len(children) != 1 or child_kinds[0] != 'text':
                return False
        elif kind == 'p':
            if not all(k == 'text' for k in child_kinds):
                return False
        elif kind == 'span':
            if not all(k in ('text', 'p') for k in child_kinds):
                return False
        elif kind in ('ul', 'ol'):
            if len(children) < 1 or not all(k == 'li' for k in child_kinds):
                return False
        elif kind == 'tr':
            if len(children) < 1 or not all(k in ('th', 'td')
                                            for k in child_kinds):
                return False
            if 'th' in child_kinds and 'td' in child_kinds:
                return False
        elif kind == 'table':
            if len(children) < 1 or not all(k == 'tr' for k in child_kinds):
                return False

        return all(self.is_valid(c) for c in children)

    def __str__(self):
        if type(self.root) == Html:
            return '<!DOCTYPE html>\n' + str(self.root)
        return str(self.root)

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))


def expect(page, valid):
    result = page.is_valid()
    status = 'OK' if result == valid else 'KO'
    print('[{}] expected valid={}, got {}'.format(status, valid, result))


if __name__ == '__main__':
    good = Page(Html([
        Head([Title(Text("Hello ground!")), Meta(Text("blabla"))]),
        Body([
            H1(Text("Oh no, not again!")),
            Img({'src': 'http://i.imgur.com/pfp3T.jpg'}),
        ]),
    ]))
    # Img is allowed inside Body? No -> body only allows the listed set.
    expect(good, False)

    valid_page = Page(Html([
        Head(Title(Text("A valid page"))),
        Body([
            H1(Text("Title")),
            Div([
                Table([
                    Tr([Th(Text("h1")), Th(Text("h2"))]),
                    Tr([Td(Text("a")), Td(Text("b"))]),
                ]),
                Ul([Li(Text("one")), Li(Text("two"))]),
                Span([P(Text("paragraph"))]),
            ]),
        ]),
    ]))
    expect(valid_page, True)

    # Head must contain exactly one Title.
    expect(Page(Html([Head([]), Body([])])), False)
    # Tr cannot mix Th and Td.
    expect(Page(Table([Tr([Th(Text("x")), Td(Text("y"))])])), False)
    # Ul must only contain Li.
    expect(Page(Ul([Li(Text("ok")), P(Text("bad"))])), False)
    # Standalone valid table.
    expect(Page(Table([Tr([Td(Text("only"))])])), True)

    print('--- rendered valid page ---')
    print(valid_page)
    valid_page.write_to_file('page.html')
