#!/usr/bin/env python3

__all__ = ['cubeupload']

class PluginBase:

    def __iter__(s):
        for d, e, h in zip(
                s.id_list, s.ext_list, s.hashes):
            yield {
                'site': s.site,
                'content_id': d,
                'content_hash': h,
                'content_extension': e,
                'content_url': s.content_url,
                'collection': s.collection,
                'original_url': s.original_url,
                'original_filename': s.original_filename,
            }
