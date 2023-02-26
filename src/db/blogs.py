# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
from deta import Deta
from dotenv import load_dotenv
from schemas import Schemas
from typing import Tuple


# ---------------------------------------------------------------------------- #
# --- User Database ---------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()

class BlogsDB():

    schemas = Schemas()
    PROJECT_KEY = os.getenv('DETA_KEY')
    deta = Deta(PROJECT_KEY)
    blogs = deta.Base('blogs')


    def get_all_blogs(self) -> Tuple[int, str, list[dict]]:
        try:
            res = self.blogs.fetch()
            all_items = res.items

            while res.last:
                res = self.blogs.fetch(last=res.last)
                all_items += res.items
            
            all_blogs = self.__all_blogs(all_items)
            return 200, 'succesfully fetched blogs from db.', all_blogs
        except Exception:
            return 500, 'could not load blogs from db.', None


    def __all_blogs(self, items: list[dict]) -> list[dict]:
        formatted = []
        for item in items:
            data = {
                'key': item['key'],
                'title': item['title'],
                'intro': item['intro'],
                'image': item['images'][0]
            }
            formatted.append(data)
        return formatted


    def get_blog_by_key(self, key:str) -> Tuple[int, str, dict]:
        try:
            blog = self.blogs.get(key)
            if blog is None:
                return 404, f"no blog with key '{key}' found in db.", None

            return 200, f"successfully found blog with key '{key}'", blog
        except:
            return 500, f"an error occurred while fetching blog with key '{key}'", None
