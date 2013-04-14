# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
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

#from prototipoIphone.prototipo.models import *
#from prototipoIphone.prototipo.forms import *

#from django.utils import simplejson
#from django.core.cache import cache

#import datetime
#import re
from django.conf import settings
from util import utils

@login_required
def index(request):
    return render_to_response('index.html', {'user':request.user})
