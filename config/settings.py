DEBUG = True

TESTING = True

DEBUG_TB_PROFILER_ENABLED = True

DEBUG_TB_PANELS = [
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_mongoengine.panels.MongoDebugPanel',
]

SERVER_NAME = 'localhost:8000'

PREFERRED_URL_SCHEME = 'http'

SECRET_KEY = 'supercalifragilisticexpialidocious'

MONGODB_SETTINGS = {'db': 'embryogenesis', 'host': 'localhost', 'port': 27017}

#  CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
#  CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
#  CELERY_ACCEPT_CONTENT = ['json']
#  CELERY_TASK_SERIALIZER = 'json'
#  CELERY_RESULT_SERIALIZER = 'json'
#  CELERY_REDIS_MAX_CONNECTIONS = 5
