from jnius import PythonJavaClass, java_method, autoclass

_activity = autoclass('org.renpy.android.PythonActivity').mActivity

_callbacks = {
    'on_new_intent': [],
    'on_activity_result': [] }

class NewIntentListener(PythonJavaClass):
    __javainterfaces__ = ['org/renpy/android/PythonActivity$NewIntentListener']
    __javacontext__ = 'app'

    def __init__(self, callback):
        super(NewIntentListener, self).__init__()
        self.callback = callback

    @java_method('(Landroid/content/Intent;)V')
    def onNewIntent(self, intent):
        self.callback(intent)


class ActivityResultListener(PythonJavaClass):
    __javainterfaces__ = ['org/renpy/android/PythonActivity$ActivityResultListener']
    __javacontext__ = 'app'

    def __init__(self, callback):
        super(ActivityResultListener, self).__init__()
        self.callback = callback

    @java_method('(IILandroid/content/Intent;)V')
    def onActivityResult(self, requestCode, resultCode, intent):
        self.callback(requestCode, resultCode, intent)


def bind(**kwargs):
    for event, callback in kwargs.items():
        if event not in _callbacks:
            raise Exception('Unknown {!r} event'.format(event))
        elif event == 'on_new_intent':
            listener = NewIntentListener(callback)
            _activity.registerNewIntentListener(listener)
            _callbacks[event].append(listener)
        elif event == 'on_activity_result':
            listener = ActivityResultListener(callback)
            _activity.registerActivityResultListener(listener)
            _callbacks[event].append(listener)

def unbind(**kwargs):
    for event, callback in kwargs.items():
        if event not in _callbacks:
            raise Exception('Unknown {!r} event'.format(event))
        else:
            for listener in _callbacks[event][:]:
                if listener.callback is callback:
                    _callbacks[event].remove(listener)
                    if event == 'on_new_intent':
                        _activity.unregisterNewIntentListener(listener)
                    elif event == 'on_activity_result':
                        _activity.unregisterActivityResultListener(listener)

