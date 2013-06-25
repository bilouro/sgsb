# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required

#from django import forms
#from django.core import serializers
#from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
#from django.core.urlresolvers import reverse
#from django.template import RequestContext
#from django.core.paginator import Paginator
#from django.contrib.auth import logout
#from django.core.files.base import ContentFile
#from django.db.models import Q

#from django.contrib.auth.models import User
#from django.db import transaction

#from django.utils import simplejson
#from django.core.cache import cache

#import datetime
from django.conf import settings
from util import utils
from django.views.generic.list import ListView
from django.utils import timezone

from cadastro.models import *

@login_required
def index(request):
    return render_to_response('index.html', {'user':request.user})


def inicial(request):
    return redirect(settings.LOGIN_REDIRECT_URL)