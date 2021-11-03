import ivy
import math
import datetime


# This callback generates the indexes. (An index is an ordered list of nodes
# attached to a node via an 'index' property.)
@ivy.events.register('init_build')
def init():
    if config := ivy.site.config.get('holly'):

        # Generate the homepage index.
        if home := config.get('homepage'):
            root_urls = home.get('root_urls', [])
            sort_func = home.get('sort_func')
            sort_rev = home.get('reverse', True)
            per_page = home.get('per_page', 10)
            make_homepage_index(root_urls, sort_func, sort_rev, per_page)

        # Generate directory and tag indexes.
        for root in config.get('roots', []):
            root_url = root.get('root_url', '')
            tag_slug = root.get('tag_slug', 'tags')
            sort_func = root.get('sort_func')
            sort_rev = root.get('reverse', True)
            per_page = root.get('per_page', 10)
            per_tag_page = root.get('per_tag_page', 100)
            if node := ivy.nodes.node(root_url):
                make_node_index(node, sort_func, sort_rev, per_page)
                make_tag_indexes(node, tag_slug, sort_func, sort_rev, per_tag_page)


# This callback adds CSS classes to index pages.
@ivy.filters.register('class_list')
def add_classes(class_list, node):
    if node.get('is_index'):
        class_list.append('index')
    if node.get('is_dir_index'):
        class_list.append('dir-index')
    if node.get('is_tag_index'):
        class_list.append('tag-index')
    if node.get('is_homepage_index'):
        class_list.append('homepage-index')
    if node.get('is_paged'):
        class_list.append('paged')
    if node.get('is_tag_base'):
        class_list.append('tag-base')
    if node.get('is_node_index'): # Deprecated.
        class_list.append('node-index')
    return class_list


# Returns a list of all the node's descendant leaf nodes, i.e nodes with no children.
def get_leaf_nodes(node):
    leaf_nodes = []
    for child in node.children:
        if child.has_children:
            leaf_nodes.extend(get_leaf_nodes(child))
        else:
            leaf_nodes.append(child)
    return leaf_nodes


# Assembles a composite index for the homepage.
def make_homepage_index(root_urls, sort_func, sort_rev, per_page):
    entries = []
    for url in root_urls:
        if node := ivy.nodes.node(url):
            entries.extend(get_leaf_nodes(node))
    sort_index(entries, sort_func, sort_rev)
    node = ivy.nodes.root()
    node['index'] = entries
    node['is_index'] = True
    node['is_homepage_index'] = True
    split_index(node, per_page)


# Assembles an index of all the node's descendant leaf nodes. Attaches this index to the node.
# Recursively generates a similar index for all descendant parent nodes.
def make_node_index(node, sort_func, sort_rev, per_page):
    entries = []
    for child in node.children:
        if child.has_children:
            entries.extend(make_node_index(child, sort_func, sort_rev, per_page))
        else:
            entries.append(child)
    sort_index(entries, sort_func, sort_rev)
    node['index'] = entries
    node['is_index'] = True
    node['is_dir_index'] = True
    node['is_node_index'] = True # Deprecated.
    split_index(node, per_page)
    return entries


# Checks all descendant nodes of the root node for tag strings. Parses tags, converts them into
# Tag objects, assembles a set of tag index pages and attaches them to the root node.
def make_tag_indexes(root_node, tag_slug, sort_func, sort_rev, per_tag_page):
    tag_base = root_node.child(tag_slug)
    if tag_base is None:
        tag_base = ivy.nodes.Node()
        root_node.children.append(tag_base)
        tag_base.parent = root_node
        tag_base['slug'] = tag_slug
        tag_base['title'] = 'Tags'

    tag_map = {}
    url_base = root_node.url.rstrip('/') + f'/{tag_slug}/'
    def tag_parser(node):
        if (tagstring := node.get('tags')) is None:
            return
        node['tags'] = []
        for tag in (t.strip() for t in tagstring.split(',') if t.strip()):
            tag_map.setdefault(tag, []).append(node)
            node['tags'].append(Tag(tag, url_base + ivy.utils.slugify(tag) + '//'))
    root_node.walk(tag_parser)

    for tag, node_list in tag_map.items():
        slug = ivy.utils.slugify(tag)
        if tag_node := tag_base.child(slug):
            tag_node.meta.setdefault('index', []).extend(node_list)
        else:
            tag_node = ivy.nodes.Node()
            tag_base.children.append(tag_node)
            tag_node.parent = tag_base
            tag_node['title'] = tag
            tag_node['slug'] = slug
            tag_node['index'] = node_list
        sort_index(tag_node['index'], sort_func, sort_rev)
        tag_node['is_index'] = True
        tag_node['is_tag_index'] = True
        split_index(tag_node, per_tag_page)

    tag_base['is_tag_base'] = True
    tag_base.children.sort(key=lambda n: n.get('title', ''))


def sort_index(node_list, sort_func, sort_rev):
    if sort_func:
        node_list.sort(key=sort_func, reverse=sort_rev)
    else:
        default_date = datetime.date(2000, 1, 1)
        node_list.sort(key=lambda n: n.filepath)
        node_list.sort(key=lambda n: n.get('date') or default_date, reverse=True)


def split_index(node, per_page):
    entries = node['index']
    total_pages = math.ceil(float(len(entries)) / per_page)
    node['is_paged'] = False

    if total_pages > 1:
        node['index'] = entries[0:per_page]
        node['is_paged'] = True
        node['page_num'] = 1
        node['total_pages'] = total_pages
        node['prev_url'] = ''
        node['next_url'] = next_url(node.url, 1, total_pages)

        for page in range(2, total_pages + 1):
            page_node = ivy.nodes.Node()
            node.children.append(page_node)
            page_node.parent = node
            page_node.meta = node.meta.copy()
            page_node['slug'] = f'{page}'
            page_node['index'] = entries[per_page * (page-1):per_page * page]
            page_node['page_num'] = page
            page_node['prev_url'] = prev_url(node.url, page)
            page_node['next_url'] = next_url(node.url, page, total_pages)


def prev_url(base_url, page_num):
    if page_num == 1:
        return ''
    if page_num == 2:
        return base_url
    return base_url.rstrip('/') + f'/{page_num - 1}//'


def next_url(base_url, page_num, total_pages):
    if page_num == total_pages:
        return ''
    return base_url.rstrip('/') + f'/{page_num + 1}//'


class Tag:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'Tag({self.name}, {self.url})'

    def __str__(self):
        return f'<a href="{self.url}">{self.name}</a>'
