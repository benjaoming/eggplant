import logging

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from getpaid.forms import PaymentMethodForm

from eggplant.common.views import LoginRequiredMixinView
from ..models import Payment

log = logging.getLogger(__name__)


@login_required
def payments_home(request):
    return redirect('eggplant:market:payment_list')


@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created')
    ctx = {
        'payments': payments
    }
    return render(request, 'eggplant/payments/payment_list.html', ctx)


@login_required
def payment_info(request, pk=None):
    payment = get_object_or_404(Payment, pk=pk, user=request.user)
    ctx = {
        'payments': [payment, ]
    }
    return render(request, 'eggplant/payments/payment_list.html', ctx)


class PaymentView(LoginRequiredMixinView, DetailView):
    model = Payment
    template_name = 'eggplant/payments/payment_detail.html'

    @method_decorator
    @login_required
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Payment.objects.filter(account__profiles=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context['payment_form'] = PaymentMethodForm(
            self.object.amount.currency,
            initial={'payment': self.object}
        )
        return context

payment_detail = PaymentView.as_view()


def payment_accepted(request, pk=None):
    __ = get_object_or_404(Payment, pk=pk, account__profiles=request.user.profile)
    messages.info(request, _("Your payment has been accepted and"
                             " it's being processed."))
    return redirect('eggplant:market:payments_list')


@login_required
def payment_rejected(request, pk=None):
    __ = get_object_or_404(Payment, pk=pk, account__profiles=request.user.profile)
    messages.error(request, _("Your payment has been cancelled."))
    return redirect("eggplant:market:payments_list")
