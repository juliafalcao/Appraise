ENGLISH = "eng"
SPANISH = "spa"

"""
general
"""

language_name_english = {
    ENGLISH: "English",
    SPANISH: "Inglés"
}

language_name_spanish = {
    ENGLISH: "Spanish",
    SPANISH: "Español"
}

language_name_basque = {
    ENGLISH: "Basque",
    SPANISH: "Euskera"
}

language_name_maltese = {
    ENGLISH: "Maltese",
    SPANISH: "Maltés"
}

"""
frontpage
"""
welcome_title = {
    ENGLISH: "Welcome!",
    SPANISH: "Bienvenido(a)!",
}

welcome_subtitle = {
    ENGLISH: "A crowd-sourced campaign for evaluation of translations",
    SPANISH: "Una campaña de evaluación de traducciones"
}

onboarding_panel_title = {
    ENGLISH: "The campaign",
    SPANISH: "La campaña"
}

onboarding_text = {
    ENGLISH: """
    <p>Are you a bilingual speaker of Maltese and English, or Spanish and Basque? If so, we need your help!</p>
    <p>We are researchers from the University of Malta (UM) and from the University of the Basque Country (UPV/EHU), and we are conducting this study in order to evaluate the quality of translations into two under-resourced languages, Maltese and Basque. Translation is not an easy task and these are not easy languages, so we would like to hear from you: if you wish to participate, we will show you some sentences and ask you to rate the translations, and that would help us a lot with our research to improve them in the future.</p>
    <p>If you want to read more and try it out, go on and create a profile — we won’t ask you for any private information, just tell us what languages you speak and you’re good to go!</p>
    """,
    SPANISH: """
        <p>¿Eres bilingüe en maltés e inglés o bilingüe en euskera y español? Si es así, ¡necesitamos tu ayuda!</p>
        <p>Somos investigadores de la Universidad de Malta (UM) y de la Universidad del País Vasco (UPV/EHU), y estamos realizando este estudio para evaluar la calidad de las traducciones a dos lenguas con pocos recursos, el maltés y el euskera. La traducción no es una tarea fácil y estos no son idiomas fáciles, por lo que nos gustaría conocer su opinión: si desea participar, le mostraremos algunas frases y le pediremos que puntúe las traducciones, y eso nos ayudaría mucho en nuestra investigación para mejorarlas en el futuro.</p>
        <p>Si quiere saber más y probarlo, cree un perfil: no le pediremos ninguna información privada, sólo díganos qué idiomas habla y listo.</p>
    """
}

dashboard_button = {
    ENGLISH: "Access dashboard",
    SPANISH: "Acceder al panel"
}

register_button = {
    ENGLISH: "Register",
    SPANISH: "Registrarse"
}

"""
dashboard
"""

dashboard_title = {
    ENGLISH: "Dashboard",
    SPANISH: "Panel"
}

task_panel_title = {
    ENGLISH: "The task",
    SPANISH: "La tarea"
}

task_panel_text = {
    ENGLISH: """
    <p>For each item, you will be shown an original sentence in English, and a translation candidate in Maltese. You will then be asked to rate the quality of the translation on a scale of 0 to 100, based on how well you believe the translation expresses the full meaning of the original sentence. Let's say a rating of 100 means that the candidate is a perfect translation: it expresses the same thing as the original sentence, in a clear and correct manner. A candidate may "lose points" if it contains grammatical or ortographic mistakes, if it's missing information, if it contains extra information that was not present in the original sentence, if it sounds unnatural or weird, and so on.</p>
    <p>You cannot edit your rating after you submit it, so please, read both the source sentence and the candidate carefully before you decide on your score.</p>
    """,
    SPANISH: """
    <p>[Waiting for translation from Nora]
    """,
}

task_button_text = {
    ENGLISH: "Go to task",
    SPANISH: "Ir a la tarea"
}

user_status_title = {
    ENGLISH: "User status",
    SPANISH: "Estado de usuario"
}

user_status_unavailable_text = {
    ENGLISH: "Start participating and evaluating translations to be able to see your user status!",
    SPANISH: "¡Empieza a participar y a evaluar traducciones para poder ver tu estado de usuario!"
}

data_warning_title = {
    ENGLISH: "Warning",
    SPANISH: "Aviso"
}

evaluations_done = {
    ENGLISH: "Evaluations done",
    SPANISH: ""
}

data_warning_text = {
    ENGLISH: "<p>Some of the sentences you will be shown over the course of this task may contain offensive or otherwise inappropriate statements. Part of the data we used was selected from a social bias dataset, a large collection of texts from the Internet that are offensive to various minority groups, and this dataset was built in order to train applications to detect and mitigate offensive content online. The rest of the sentences were similarly collected from various different sources, publications, media, and the Internet. They may also contain wrong or outdated factual information about various topics. None of the sentences were written by us, and they do not express the views of anyone involved with this project. They also do not need to be factually correct. Our only goal is to analyze the quality of the automatic translations. Thank you for understanding.</p>",
    SPANISH: "<p><i>Awaiting translation from Nora!</i></p>"
}

"""
task page
"""
task_prompt = {
    ENGLISH: """
    <p>For the pair of sentences below, state <strong>how much you agree</strong> that:</p>
    <p align="center"><strong>The candidate translation adequately expresses the meaning of the original text.</strong></p>
    """,
    SPANISH: """
    <p>FPara el par de frases siguientes, indique hasta qué punto está de acuerdo en que:</p>
    <p align="center"><strong>La traducción del candidato expresa adecuadamente el sentido del texto original.</strong></p>
    """
}

"""
create profile
"""
create_profile_title = {
    ENGLISH: "Register to participate",
    SPANISH: "Registrarse para participar"
}

create_profile_subtitle = {
    ENGLISH: "Please create an username and a password, and then tell us which languages you can evaluate.",
    SPANISH: "Por favor, cree un nombre de usuario y una contraseña, y luego díganos qué idiomas puede evaluar."
}

username_label_text = {
    ENGLISH: "Username",
    SPANISH: "Nombre de usuario"
}

username_help_text = {
    ENGLISH: "Please create an username",
    SPANISH: "Por favor, crea un nombre de usuario"
}

password1_label_text = {
    ENGLISH: "Password",
    SPANISH: "Contraseña"
}

password1_help_text = {
    ENGLISH: "Please enter your desired password",
    SPANISH: "Por favor, introduzca la contraseña deseada"
}

password2_label_text = {
    ENGLISH: "Password (again)",
    SPANISH: "Contraseña (otra vez)"
}

password2_help_text = {
    ENGLISH: "Please re-type your password",
    SPANISH: "Vuelva a introducir la contraseña deseada"
}

lp_help_text = {
    ENGLISH: "For this project, we wish to evaluate of translations between two pairs of languages: from English into Maltese, and from Spanish into Basque. Please select below which language pair you would like to contribute with, and tell us your proficiency level in each language.",
    SPANISH: "Para este proyecto, deseamos evaluar traducciones entre dos pares de idiomas: del inglés al maltés, y del español al euskera. Por favor, seleccione con qué par de idiomas le gustaría contribuir, e indíquenos su nivel de competencia en cada uno de ellos."
}

lp_label_text = {
    ENGLISH: "Language pair",
    SPANISH: "Par de idiomas"
}

lp_engmlt_option_text = {
    ENGLISH: "Maltese and English",
    SPANISH: "Maltés e inglés"
}

lp_spaeus_option_text = {
    ENGLISH: "Basque and Spanish",
    SPANISH: "Euskera y español"
}

select_option_text = {
    ENGLISH: "select",
    SPANISH: "seleccionar"
}

proficiency_level_label_text = {
    ENGLISH: "Proficiency level",
    SPANISH: "Nivel de competencia"
}

proficiency_level_beginner = {
    ENGLISH: "beginner",
    SPANISH: "principiante"
}

proficiency_level_intermediate = {
    ENGLISH: "intermediate",
    SPANISH: "intermedio"
}

proficiency_level_advanced = {
    ENGLISH: "advanced",
    SPANISH: "avanzado"
}

proficiency_level_fluent = {
    ENGLISH: "fluent",
    SPANISH: "fluido"
}

proficiency_level_native = {
    ENGLISH: "native",
    SPANISH: "nativo"
}

create_profile_button = {
    ENGLISH: "Create profile",
    SPANISH: "Registrarse",
}

error_msg_warning_header = {
    ENGLISH: "Warning!",
    SPANISH: "¡Atención!"
}

error_msg_invalid_username = {
    ENGLISH: "Invalid or missing username. Please provide a new username.",
    SPANISH: "Falta el nombre de usuario o no es válido. Por favor, introduzca un nuevo nombre de usuario."
}

error_msg_username_already_exists = {
    ENGLISH: "The username you have entered already exists. Please choose a new username.",
    SPANISH: "El nombre de usuario que ha introducido ya existe. Por favor, elija un nuevo nombre de usuario."
}

error_msg_missing_password = {
    ENGLISH: "Missing password. Please type your desired password twice, in both fields.",
    SPANISH: "Falta la contraseña. Por favor, escriba la contraseña deseada dos veces, en ambos campos."
}

error_msg_passwords_not_matching = {
    ENGLISH: "The passwords don't match. Please type the desired password in both fields.",
    SPANISH: "Las contraseñas no coinciden. Por favor, introduzca la contraseña deseada en ambos campos."
}

error_msg_password_too_short = {
    ENGLISH: "The password must be at least 4 characters long. Please try again.",
    SPANISH: "La contraseña debe tener al menos 4 caracteres. Por favor, inténtelo de nuevo."
}

error_msg_no_lang_selected = {
    ENGLISH: "Please choose at least one language for evaluation.",
    SPANISH: "Elija al menos una lengua para evaluación."
}

error_msg_missing_poficiency_level = {
    ENGLISH: "Please select your proficiency level in all the languages you've marked.",
    SPANISH: "Por favor, seleccione su nivel de competencia en todas las lenguas que ha marcado."
}

error_msg_default = {
    ENGLISH: "Something bad happened. Please try again.",
    SPANISH: "Ha ocurrido algo malo. Por favor, inténtelo de nuevo."
}

"""
sign in
"""

user_auth_title = {
    ENGLISH: "User authentication",
    SPANISH: "Autenticación de usuarios"
}

user_auth_subtitle = {
    ENGLISH: "Please enter your username and password so we can verify your credentials.",
    SPANISH: "Introduzca su nombre de usuario y contraseña para que podamos verificar sus credenciales."
}

signin_username_help_text = {
    ENGLISH: "Please enter your username",
    SPANISH: "Introduzca su nombre de usuario"
}

signin_password_help_text = {
    ENGLISH: "And also provide your password",
    SPANISH: "Y escriba también su contraseña"
}

signin_button_text = {
    ENGLISH: "Sign in",
    SPANISH: "Entrar"
}

signin_error_text = {
    ENGLISH: "We did not find a registered user with your username and password. Please try again.",
    SPANISH: "No hemos encontrado ningún usuario registrado con su nombre de usuario y contraseña. Por favor, inténtelo de nuevo."
}

"""
nav
"""

account = {
    ENGLISH: "Account",
    SPANISH: "Cuenta"
}

sign_in = {
    ENGLISH: "Sign in",
    SPANISH: "Entrar"
}

register = {
    ENGLISH: "Register",
    SPANISH: "Registrarse"
}

sign_out = {
    ENGLISH: "Sign out",
    SPANISH: "Salir"
}

home_title = {
    ENGLISH: "Home",
    SPANISH: "Inicio"
}

"""
aux
"""

def _get_lang_texts(texts_module, ui_lang):
    # get vars from texts_module and keep only the text dicts
    text_dicts = {_key : _val for _key, _val in vars(texts_module).items() if (not _key.startswith("_")) and (type(_val) == dict)}

    # given the ui_lang, get each text in that lang and return as key:text dict
    lang_texts = {text_key : text_dict[ui_lang].strip() for text_key, text_dict in text_dicts.items()}

    return lang_texts

"""
This is a horrible hack to make my life easier and get all of the variables from this module as a dict so that I don't have to write them as a dict myself. It accesses the `vars` from this very module and filters out only the relevant text dicts from above, then returns only the texts corresponding to the given `ui_lang`. This delegates the responsibility of choosing the UI lang to Python code, which is much easier than doing it in templates, and then all of the texts can be unpacked at once into the context dict of whatever Django view I want, which is not entirely necessary nor efficient, but is convenient, and hopefully harmless.

    import translated_texts
    lang_texts = translated_texts._get_lang_texts(translated_texts, ui_lang)
    context = { ..., **lang_texts }

Then in templates they can just be included like this:

    <div>{{task_prompt|safe}}</div>

(The `safe` is for when there is HTML inside of the text string.)
"""