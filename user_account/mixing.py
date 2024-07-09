#logged in user jeno login page access na korte pare tar jonno mixing create kortesi

from django.shortcuts import redirect

class LogoutRequiredMixin(object):
    # jei kono http method(get, post etc) call hoar age dispatch method call hoy.
    def dispatch(self,request ,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        # authenticated na hole dispatch jemon kaj korar kotha temon kaj korbe
        return super(LogoutRequiredMixin,self).dispatch(request,*args, **kwargs)