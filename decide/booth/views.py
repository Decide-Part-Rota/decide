import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from census.models import Census
from voting.models import Voting
from base import mods


# TODO: check permissions and census
class BoothView(TemplateView):
    template_name = 'booth/booth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})

            # Casting numbers to string to manage in javascript with BigInt
            # and avoid problems with js and big number conversion
            for k, v in r[0]['pub_key'].items():
                r[0]['pub_key'][k] = str(v)

            context['voting'] = json.dumps(r[0])
        except:
            raise Http404

        context['KEYBITS'] = settings.KEYBITS

        return context

class BoothListView(TemplateView):
    template_name = 'booth/boothList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        censo = Census.objects.filter(voter_id=self.request.user.id)
        votaciones_participa = [c.voting_id for c in censo]
        votaciones = Voting.objects.filter(public=True)

        dict_no_participa= {}
        dict_participa= {}
        for v in votaciones:
            tupla=(v.id,v.name,v.desc,v.public)
            if v.id not in votaciones_participa:
                dict_no_participa.update({v.id:tupla})
            else:
                dict_participa.update({v.id:tupla})

        context["userdata"]=self.request.user
        context["votacionesNoParticipa"]=json.dumps(dict_no_participa, indent=4)
        context["votacionesParticipa"]=json.dumps(dict_participa, indent=4)
        return context


class BoothListPrivateView(TemplateView):
    template_name = 'booth/boothListPrivate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        censo = Census.objects.filter(voter_id=self.request.user.id)
        votaciones_participa = [c.voting_id for c in censo]
        votaciones = Voting.objects.filter(public=True)

        dict_no_participa= {}
        dict_participa= {}
        for v in votaciones:
            tupla=(v.id,v.name,v.desc,v.public)
            if v.id not in votaciones_participa:
                dict_no_participa.update({v.id:tupla})
            else:
                dict_participa.update({v.id:tupla})
                print("hey")

        context["userdata"]=self.request.user
        context["votacionesNoParticipa"]=json.dumps(dict_no_participa, indent=4)
        context["votacionesParticipa"]=json.dumps(dict_participa, indent=4)
        return context

