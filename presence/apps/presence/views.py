import random
import hashlib
from django.views.generic import TemplateView

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
        context = dict(title=titles[index],
                       content=content,
                       page=page_hash)
        return context
