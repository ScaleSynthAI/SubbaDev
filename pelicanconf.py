import os
import json

AUTHOR = 'Subba Taniparti'
SITENAME = 'Subba Taniparti'
SITEURL = ''  # Kept blank for local relative links

PATH = 'content'
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'

# Feed generation
FEED_ALL_ATOM = 'feed.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Custom theme path
THEME = 'themes/subba'

import datetime
import re
CURRENT_YEAR = datetime.datetime.now().year
LAST_UPDATED = datetime.datetime.now().strftime("%B %d, %Y")

def estimate_reading_time(content):
    # Strip HTML tags and split by space
    words = len(re.sub('<[^<]+?>', '', content).split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"

JINJA_FILTERS = {
    'reading_time': estimate_reading_time
}

# URL structure and Clean URLs
ARTICLE_URL = 'writing/{slug}/'
ARTICLE_SAVE_AS = 'writing/{slug}/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

ARCHIVES_URL = 'writing/'
ARCHIVES_SAVE_AS = 'writing/index.html'

# Disable unused indexes to keep site low-chrome
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

# Load resume data from content/data/resume.json
RESUME_FILE = os.path.join(os.path.dirname(__file__), 'content', 'data', 'resume.json')
if os.path.exists(RESUME_FILE):
    with open(RESUME_FILE, 'r') as f:
        RESUME_DATA = json.load(f)
else:
    RESUME_DATA = {}

# Load projects data from content/data/projects.json
PROJECTS_FILE = os.path.join(os.path.dirname(__file__), 'content', 'data', 'projects.json')
if os.path.exists(PROJECTS_FILE):
    with open(PROJECTS_FILE, 'r') as f:
        PROJECTS_DATA = json.load(f)
else:
    PROJECTS_DATA = []

# Sitemap configurations
PLUGINS = ['pelican.plugins.sitemap']
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.8,
        'pages': 0.7
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Static paths
STATIC_PATHS = ['images', 'cv', 'extra/robots.txt']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}

DEFAULT_PAGINATION = False
