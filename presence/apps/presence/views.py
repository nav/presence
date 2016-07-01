import random
import hashlib

import json
from django.views.generic import TemplateView

from ..whiteboard.models import Message


class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, *args, **kwargs):
        page = self.request.path
        page_hash = hashlib.sha1(page).hexdigest()
        titles = ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                  'Cras tristique magna eu nulla sollicitudin tristique.',
                  'Integer a tristique odio.',
                  'Suspendisse mattis posuere luctus.',
                  'Pellentesque imperdiet nisl nec odio iaculis aliquam.',
                  'Quisque vitae lacinia dolor.',
                  'Pellentesque ut leo facilisis, congue mauris.']
        content = [[titles[int(random.randint(1, 999) % len(titles))] \
                        for j in range(random.randint(5,10))] \
                            for i in range(5)]
        index = int(page_hash, 16) % (len(titles))
        messages = Message.objects.select_related('comment__user').filter(page=page_hash)
        messages = [{'id': m.pk,
                     'comment': m.comment.comment,
                     'submit_date': m.comment.submit_date.strftime('%Y-%m-%d'),
                     'hash': hashlib.md5(m.comment.user.email).hexdigest()} for m in messages]
        context = dict(title=titles[index],
                       content=content,
                       page=page_hash,
                       comments=json.dumps(messages))
        return context

