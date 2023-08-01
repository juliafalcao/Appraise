"""
Appraise evaluation framework

See LICENSE for usage details
"""
from datetime import datetime
from hashlib import md5
from inspect import currentframe
from inspect import getframeinfo

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.defaulttags import register

from Appraise.settings import BASE_CONTEXT
from Appraise.utils import _get_logger
from Dashboard.models import LANGUAGE_CODES_AND_NAMES, PROFICIENCY_LEVELS, MIN_PROFICIENCY, LANGUAGE_PAIRS
from Dashboard.models import UserInviteToken
from Dashboard.utils import generate_confirmation_token
from EvalData.models import DirectAssessmentTask
from EvalData.models import TASK_DEFINITIONS
from EvalData.models import TaskAgenda

import translated_texts

@register.filter
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)

@register.filter
def index(indexable, i):
    return indexable[i]

TASK_TYPES = tuple([tup[1] for tup in TASK_DEFINITIONS])
TASK_RESULTS = tuple([tup[2] for tup in TASK_DEFINITIONS])

# TODO: task names should be stored in task classes as an attribute
TASK_NAMES = {tup[1]: tup[0].lower() for tup in TASK_DEFINITIONS}
TASK_URLS = {tup[0].lower(): tup[3] for tup in TASK_DEFINITIONS}


from deprecated import add_deprecated_method

LOGGER = _get_logger(name=__name__)

HITS_REQUIRED_BEFORE_ENGLISH_ALLOWED = 0


# HTTP error handlers supporting COMMIT_TAG.
def _page_not_found(request, template_name='404.html'):
    """
    Custom HTTP 404 handler that preserves URL_PREFIX.
    """
    del template_name  # Unused.

    LOGGER.info(
        'Rendering HTTP 404 for user "%s". Request.path=%s',
        request.user.username or "Anonymous",
        request.path,
    )

    ui_lang = _get_ui_lang(request)
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)

    context = {
        **BASE_CONTEXT,
        "ui_lang": ui_lang,
        **lang_texts,
    }

    return render(request, 'Dashboard/404.html', context)


def _server_error(request, template_name='500.html'):
    """
    Custom HTTP 500 handler that preserves URL_PREFIX.
    """
    del template_name  # Unused.

    LOGGER.info(
        'Rendering HTTP 500 for user "%s". Request.path=%s',
        request.user.username or "Anonymous",
        request.path,
    )

    ui_lang = _get_ui_lang(request)
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)

    context = {
        **BASE_CONTEXT,
        "ui_lang": ui_lang,
        **lang_texts,
    }

    return render(request, 'Dashboard/500.html', context)


def sso_login(request, username, password):
    """
    Forces SSO login for the given username:password credentials.
    If another user is already logged in, it will be logged out.
    """
    # Login user and redirect to dashboard page.
    if request.user.username:
        LOGGER.info('Logging out user "%s"', request.user.username)
        logout(request)

    user = authenticate(username=username, password=password)
    login(request, user)

    LOGGER.info(
        'Rendering SSO login view for user "%s".',
        request.user.username or "Anonymous",
    )

    return redirect('dashboard')

def _get_ui_lang(request):
    # get from cookie if already defined
    ui_lang = request.COOKIES.get("ui_lang", None)

    if not ui_lang:
        ui_lang = "eng" # leave English as default at first

        # if user is logged in: check their source language to set as UI language
        if request.user.username:
            for _src, _tgt in LANGUAGE_PAIRS:
                if request.user.groups.filter(name=_src).exists():
                    ui_lang = _src

        # if anonymous: try and get user's location with the IP
        else:
            try:
                ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", None))
                geoip = GeoIP2("/home/juliafalcao/geoip_dbs")
                country = geoip.country(ip)["country_name"]
                print("COUNTRY:", country)

                if country.lower() in ["spain", "france"]:
                    # including France because of the French Basque Country but the users can always manually change the language if needed
                    ui_lang = "spa"
            except Exception as e:
                print("Error finding country:", e)

    return ui_lang

def signin(request, extra_context=None):
    logout(request)
    username = None
    password = None

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')

    # get UI language and the corresponding translated texts
    ui_lang = _get_ui_lang(request)
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)

    context = {
        "active_page": "sign-in",
        "ui_lang": ui_lang,
        **lang_texts,
    }

    context.update(BASE_CONTEXT)
    if extra_context:
        context.update(extra_context)

    response = render(request, 'Dashboard/signin.html', context)
    response.set_cookie("ui_lang", ui_lang)
    return response

def signout(request, extra_context=None):
    logout(request)
    return redirect('frontpage')

def frontpage(request, extra_context=None):
    """
    Appraise front page.
    """
    LOGGER.info(
        'Rendering frontpage view for user "%s".',
        request.user.username or "Anonymous",
    )

    # get UI language and the corresponding translated texts
    ui_lang = _get_ui_lang(request)
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)

    context = {
        "active_page": "frontpage",
        "ui_lang": ui_lang,
        **lang_texts,
    }

    context.update(BASE_CONTEXT)
    if extra_context:
        context.update(extra_context)

    response = render(request, 'Dashboard/frontpage.html', context)
    response.set_cookie("ui_lang", ui_lang)
    return response

def _validate_passwords(password1: str, password2: str) -> (bool, str):
    if (not password1 or not password2):
        return (False, "missing_password")

    if password1 != password2:
        return (False, "passwords_not_matching")

    # password rules
    if len(password1) < 4:
        return (False, "password_too_short")

    return (True, None)

def _validate_languages(languages: list, proficiency_levels: dict) -> (bool, str):
    if not languages:
        return (False, "no_language_selected")

    for lang in languages:
        if proficiency_levels.get(lang, None) in [None, ""]:
            return (False, "missing_proficiency_level")

    return (True, None)

def create_profile(request):
    """
    Renders the create profile view.
    """
    errors = None
    username = None
    lp_code = None
    languages = []
    proficiency_levels = {}
    src, tgt = None, None

    language_names = LANGUAGE_CODES_AND_NAMES
    proficiency_level_choices = PROFICIENCY_LEVELS

    focus_input = 'id_username'

    if request.method == "POST":
        username = request.POST.get('username', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)

        _password_ok, _password_error = _validate_passwords(password1, password2)

        lp_code = request.POST.get("lp_code", None)
        languages = lp_code.split("-")
        (src, tgt) = languages

        proficiency_levels = {
            src: request.POST.get("proficiency-level-src", None),
            tgt: request.POST.get("proficiency-level-tgt", None),
        }

        _languages_ok, _languages_error = _validate_languages(languages, proficiency_levels) # TODO

        if username and languages and _password_ok and _languages_ok:
            try:
                # Check if desired username is already in use.
                current_user = User.objects.filter(username=username)
                if current_user.exists():
                    raise ValueError('username_already_exists')

                # Set password
                password = password1

                # Compute set of evaluation languages for this user.
                user_groups = []
                for code in languages:
                    language_group = Group.objects.filter(name=code)
                    if language_group.exists():
                        user_groups.extend(language_group)

                    language_level_group = Group.objects.filter(name=f"{code}-{proficiency_levels[code]}")
                    if language_level_group.exists():
                        user_groups.extend(language_level_group)

                # Hardcoded: add to public-users group
                public_users_group = Group.objects.filter(name="public-users")
                if public_users_group.exists():
                    user_groups.extend(public_users_group)

                # Create new user account
                user = User.objects.create_user(username=username, password=password)

                # Update group settings for the new user account.
                for group in user_groups:
                    user.groups.add(group)

                user.save()

                # Login user and redirect to dashboard page.
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('dashboard')

            # For validation errors, invalidate the respective value.
            except ValueError as issue:
                if issue.args[0] == 'invalid_username':
                    username = None

                else:
                    username = None
                    languages = None

            # For any other exception, clean up and ask user to retry.
            except Exception:
                from traceback import format_exc

                print(format_exc())  # TODO: need logger here!
                username = None
                languages = None

        # Detect which input should get focus for next page rendering.
        if not username:
            focus_input = 'id_username'
            errors = ['invalid_username']

        elif not _password_ok:
            focus_input = 'password1'
            errors = ['general_password_error', _password_error]

        elif not _languages_ok:
            focus_input = 'id_languages'
            errors = [_languages_error]

    # get UI language and the corresponding translated texts
    ui_lang = _get_ui_lang(request)
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)

    context = {
        'active_page': 'create-profile',
        'errors': errors,
        'focus_input': focus_input,
        'username': username,
        'languages': languages,
        'lp_code': lp_code,
        'proficiency_levels': proficiency_levels,
        'src': src,
        'tgt': tgt,
        'language_names': language_names,
        'proficiency_level_choices': proficiency_level_choices,
        'title': 'Register',

        'ui_lang': ui_lang,
        **lang_texts,
    }
    context.update(BASE_CONTEXT)

    response = render(request, 'Dashboard/create-profile.html', context)
    response.set_cookie("ui_lang", ui_lang)
    return response

@login_required
def dashboard(request):
    """
    Appraise dashboard page.
    """
    _t1 = datetime.now()

    template_context = {'active_page': 'dashboard'}
    template_context.update(BASE_CONTEXT)

    annotations = 0  # Completed items
    hits = 0  # Completed HITs
    total_hits = 0  # Total number of HITs expected from the user
    for result_cls in TASK_RESULTS:
        annotations += result_cls.get_completed_for_user(request.user)
        _hits, _total = result_cls.get_hit_status_for_user(request.user)
        hits, total_hits = hits + _hits, total_hits + _total

    # If user still has an assigned task, only offer link to this task.
    current_task = None
    for task_cls in TASK_TYPES:
        if not current_task:
            current_task = task_cls.get_task_for_user(request.user)


        # Check if marketTargetLanguage for current_task matches user languages.
        if current_task:
            code = current_task.marketTargetLanguageCode()
            # print('  User groups:', request.user.groups.all())
            # if code not in request.user.groups.values_list('name', flat=True):
            #     _msg = 'Language %s not specified for user %s. Giving up task %s'
            #     LOGGER.info(_msg, code, request.user.username, current_task)

            #     current_task.assignedTo.remove(request.user)
            #     current_task = None

    print('  Current task: {0}'.format(current_task))

    # set languages in order [src, tgt] according to existing language pairs
    languages = []

    for _src, _tgt in LANGUAGE_PAIRS:
        if request.user.groups.filter(name=_src).exists() and request.user.groups.filter(name=_tgt).exists():
            languages.extend([_src, _tgt])

    (src, tgt) = languages
    language_names = [LANGUAGE_CODES_AND_NAMES[lang_code] for lang_code in languages]

    # check proficiency levels
    proficiency_level_accepted = True

    for lang_code in languages:
        proficiency_group_query_set = request.user.groups.filter(name__contains=f"{lang_code}-")
        if proficiency_group_query_set.exists():
            proficiency_group = proficiency_group_query_set[0].name
            proficiency_level = proficiency_group.split("-")[-1]

            if PROFICIENCY_LEVELS.index(proficiency_level) < PROFICIENCY_LEVELS.index(MIN_PROFICIENCY):
                LOGGER.info(f"Proficiency level `{proficiency_group}` insufficient")
                proficiency_level_accepted = False

    _t2 = datetime.now()

    # Compute set of language codes eligible for next task.

    # Mapping: task type => campaign name => list of languages
    languages_map = {task_cls: {} for task_cls in TASK_TYPES}

    if not current_task:
        # Remove any language for which no free task is available.
        from Campaign.models import Campaign

        # Mapping: task type => campaigns as QuerySet
        campaign_map = {task_cls: None for task_cls in TASK_TYPES}

        for campaign in Campaign.objects.all():
            print('Campaign: {0}'.format(campaign.campaignName))

            for task_cls in campaign_map:
                campaign_map[task_cls] = task_cls.objects.filter(
                    campaign__campaignName=campaign.campaignName
                )

            for task_cls in campaign_map:
                if campaign_map[task_cls].exists():
                    languages_map[task_cls][campaign.campaignName] = []
                    languages_map[task_cls][campaign.campaignName].extend(languages)

            for code in languages:
                next_task_available = None

                _cls = DirectAssessmentTask
                for task_cls in campaign_map:
                    if campaign_map[task_cls].exists():
                        _cls = task_cls
                        break

                next_task_available = _cls.get_next_free_task_for_language(
                    code, campaign, request.user
                )

                if not next_task_available:
                    for task_cls in campaign_map:
                        if campaign_map[task_cls].exists():
                            languages_map[task_cls][campaign.campaignName].remove(code)

            # _type and _languages variables are only for debug
            for task_cls in campaign_map:
                if campaign_map[task_cls].exists():
                    _type = TASK_NAMES[task_cls]
                    _languages = languages_map[task_cls]
                    break

    _t3 = datetime.now()

    # Collect total annotation time
    times = {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0}
    for task_cls in TASK_RESULTS:
        duration = task_cls.get_time_for_user(request.user)
        secs = duration.total_seconds()
        days = duration.days
        times['days'] += days
        times['hours'] += int((secs - (days * 86400)) / 3600)
        times['minutes'] += int(((secs - (days * 86400)) % 3600) / 60)
        times['seconds'] += int((secs - (days * 86400)) % 60)

    _t4 = datetime.now()

    # All languages per task type
    # Mapping: task name => list of (code, language, campaign, task_url)
    all_languages = {}
    for task_cls, campaign_languages in languages_map.items():
        task_name = TASK_NAMES[task_cls]
        task_url = TASK_URLS[task_name]

        for camp_name, lang_codes in campaign_languages.items():
            for lang_code in lang_codes:
                lang_name = LANGUAGE_CODES_AND_NAMES[lang_code]
                if task_name not in all_languages:
                    all_languages[task_name] = []
                all_languages[task_name].append(
                    (lang_code, lang_name, camp_name, task_url)
                )

        print(
            '    Languages "{}": {}'.format(
                task_name,
                str(all_languages.get(task_name, 'none')).encode('utf-8'),
            )
        )

    # Note that the default task type is 'direct'
    current_type = TASK_NAMES.get(current_task.__class__, 'direct')
    print('  Final task type: {0}'.format(current_type))

    current_url = TASK_URLS[current_type]
    print('  URL: {0}'.format(current_url))

    # Provide UUID for the completed task
    # if work_completed:
        # work_completed = generate_confirmation_token(request.user.username, run_qc=True)

    ui_lang = _get_ui_lang(request)
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)

    template_context.update(times)
    template_context.update(
        {
            'annotations': annotations,
            'hits': hits,
            'total_hits': total_hits,
            'current_task': current_task,
            'current_type': current_type,
            'current_url': current_url,
            'languages': languages,
            'language_names': language_names,
            'all_languages': all_languages,
            'debug_times': (_t2 - _t1, _t3 - _t2, _t4 - _t3, _t4 - _t1),
            'template_debug': 'debug' in request.GET,
            # 'work_completed': work_completed,
            'proficiency_level_accepted': proficiency_level_accepted,
            'src': src,
            'tgt': tgt,
            'ui_lang': ui_lang,
            **lang_texts,
        }
    )

    return render(request, 'Dashboard/dashboard.html', template_context)


# pylint: disable=missing-docstring
@login_required
def group_status(request):
    _method = getframeinfo(currentframe()).function
    _msg = '{0}.{1} deprecated as of 7/08/2019.'.format('Dashboard.views', _method)
    raise NotImplementedError(_msg)


# pylint: disable=missing-docstring
@login_required
def multimodal_status(request):
    _method = getframeinfo(currentframe()).function
    _msg = '{0}.{1} deprecated as of 7/08/2019.'.format('Dashboard.views', _method)
    raise NotImplementedError(_msg)


# pylint: disable=missing-docstring
@login_required
def system_status(request):
    _method = getframeinfo(currentframe()).function
    _msg = '{0}.{1} deprecated as of 7/08/2019.'.format('Dashboard.views', _method)
    raise NotImplementedError(_msg)


# pylint: disable=missing-docstring
@login_required
def multimodal_systems(request):
    _method = getframeinfo(currentframe()).function
    _msg = '{0}.{1} deprecated as of 7/08/2019.'.format('Dashboard.views', _method)
    raise NotImplementedError(_msg)


# pylint: disable=missing-docstring
@login_required
@add_deprecated_method
def metrics_status(request):
    _method = getframeinfo(currentframe()).function
    _msg = '{0}.{1} deprecated as of 7/08/2019.'.format('Dashboard.views', _method)
    raise NotImplementedError(_msg)


# pylint: disable=missing-docstring
@login_required
@add_deprecated_method
def fe17_status(request):
    _method = getframeinfo(currentframe()).function
    _msg = '{0}.{1} deprecated as of 7/08/2019.'.format('Dashboard.views', _method)
    raise NotImplementedError(_msg)
