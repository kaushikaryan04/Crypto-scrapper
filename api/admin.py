from django.contrib import admin
from .models import Job , Coin , CoinOutput , Link , Contract

admin.site.register(Job)
admin.site.register(Coin)
admin.site.register(Link)
admin.site.register(Contract)
admin.site.register(CoinOutput)
