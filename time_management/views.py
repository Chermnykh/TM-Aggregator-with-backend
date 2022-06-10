import stripe
# from django.conf import settings
from TM_aggregator import secret
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # redirects user to a certain part of our page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate 
from django.contrib.auth.decorators import login_required
from .models import Task, StripeCustomer, Timer
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt #provides easy-to-use protection against Cross Site Request Forgeries
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

# Register / Login

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('home')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="auth/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="auth/login.html", context={"login_form":form})
    

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'auth/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('profile')



from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'TM-aggregator',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'velur477@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})


# Pomodoro
class TimerView(LoginRequiredMixin, ListView):
    model = Timer
    template_name = 'pomodoro.html'
    context_object_name = 'timers'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # super returns an intermediary object that delegates method calls to a parent or relative class of the specified type
        timer = Timer.objects.filter(user=self.request.user)
        if timer.count() == 0:
            timer = Timer(user=self.request.user)
            timer.save()
        else:
            timer = timer.first()
        context['timer'] = timer
        return context

@csrf_exempt
def restart_timer(request):
    timer = Timer.objects.filter(user=request.user).first()
    timer.timer_time_1 = timer.timer_time_max_1
    timer.timer_time_2 = timer.timer_time_max_2
    timer.timer_time_3 = timer.timer_time_max_3
    timer.timer_time_4 = timer.timer_time_max_4
    timer.timer_time_5 = timer.timer_time_max_5
    timer.timer_time_6 = timer.timer_time_max_6
    timer.timer_time_7 = timer.timer_time_max_7
    timer.timer_time_8 = timer.timer_time_max_8
    timer.save()
    return JsonResponse({'success': str(200)})
    

@csrf_exempt
def update_timer(request):
    timer = Timer.objects.filter(user=request.user).first()
    timer.timer_time_1 = request.POST.get("timer_time_1")
    timer.timer_time_2 = request.POST.get("timer_time_2")
    timer.timer_time_3 = request.POST.get("timer_time_3")
    timer.timer_time_4 = request.POST.get("timer_time_4")
    timer.timer_time_5 = request.POST.get("timer_time_5")
    timer.timer_time_6 = request.POST.get("timer_time_6")
    timer.timer_time_7 = request.POST.get("timer_time_7")
    timer.timer_time_8 = request.POST.get("timer_time_8")
    timer.timer_time_max_1 = request.POST.get("timer_time_max_1")
    timer.timer_time_max_2 = request.POST.get("timer_time_max_2")
    timer.timer_time_max_3 = request.POST.get("timer_time_max_3")
    timer.timer_time_max_4 = request.POST.get("timer_time_max_4")
    timer.timer_time_max_5 = request.POST.get("timer_time_max_5")
    timer.timer_time_max_6 = request.POST.get("timer_time_max_6")
    timer.timer_time_max_7 = request.POST.get("timer_time_max_7")
    timer.timer_time_max_8 = request.POST.get("timer_time_max_8")
    timer.save()
    return JsonResponse({'success': str(200)})

#  Tasks
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    # when the task is submitted redirect user to 'tasks' page
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


# Payment
@login_required
def subscription(request):
    try:
        # Retrieve the subscription & product
        stripe_customer = StripeCustomer.objects.get(user=request.user)
        stripe.api_key = secret.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        return render(request, 'profile.html', {
            'subscription': subscription,
            'product': product,
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'profile.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': secret.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session_personal(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = secret.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id 
                if request.user.is_authenticated 
                else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': secret.STRIPE_PRICE_ID_PERSONAL,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def create_checkout_session_family(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = secret.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id 
                if request.user.is_authenticated 
                else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': secret.STRIPE_PRICE_ID_FAMILY,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def create_checkout_session_business(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = secret.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id 
                if request.user.is_authenticated 
                else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': secret.STRIPE_PRICE_ID_BUSINESS,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# create a new StripeCustomer every time someone subscribes to our service:
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = secret.STRIPE_SECRET_KEY
    endpoint_secret = secret.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripeCustomerId=stripe_customer_id,
            stripeSubscriptionId=stripe_subscription_id,
        )
        print(user.username + ' just subscribed.')

    return HttpResponse(status=200)


@login_required
def success(request):
    return render(request, 'success.html')


@login_required
def cancel(request):
    return render(request, 'cancel.html')

def index(request):
    return render(request, "index.html")

def methods(request):
    return render(request, "methods.html")

