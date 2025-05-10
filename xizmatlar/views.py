from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Xizmat
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Sharh
from .forms import SharhForm
from .forms import XizmatForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Message, User, Availability
from .forms import MessageForm







def book_service(request, xizmat_id):
    xizmat = get_object_or_404(Xizmat, id=xizmat_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.xizmat = xizmat
            message.save()
            return redirect('service_detail', xizmat.id)
    else:
        form = MessageForm()
    return redirect('service_detail', xizmat.id)




@login_required
def chegirmali_xizmat_qoshish(request):
    if request.method == 'POST':
        form = XizmatForm(request.POST, request.FILES)
        if form.is_valid():
            xizmat = form.save(commit=False)
            xizmat.egasi = request.user
            xizmat.skidka = True  # chegirmali belgilanadi
            xizmat.save()
            return redirect('skidka')
    else:
        form = XizmatForm()
    return render(request, 'xizmatlar/skidka_qoshish.html', {'form': form})



def skidka_xizmatlar(request):
    xizmatlar = Xizmat.objects.filter(skidka=True)
    return render(request, 'xizmatlar/skidka.html', {'xizmatlar': xizmatlar})





def santexniklar(request):
    xizmatlar = Xizmat.objects.filter(kategoriya='Сантехник')
    return render(request, 'xizmatlar/santexnik.html', {'xizmatlar': xizmatlar})


def xasharchilar(request):
    xizmatlar = Xizmat.objects.filter(kategoriya="Ҳашарчӣ")  # Kategoriyani o'zingizga moslang
    return render(request, 'xizmatlar/xasharchi.html', {'xizmatlar': xizmatlar})

def barqchilar(request):
    xizmatlar = Xizmat.objects.filter(kategoriya='Барқчӣ')
    return render(request, 'xizmatlar/barqchi.html', {'xizmatlar': xizmatlar,})

def cleaners(request):
    xizmatlar = Xizmat.objects.filter(kategoriya='Тозакунанда')
    return render(request, 'xizmatlar/cleaner.html', {'xizmatlar': xizmatlar,})

def qassoblar(request):
    xizmatlar = Xizmat.objects.filter(kategoriya='Қассоб')
    return render(request, 'xizmatlar/qassob.html', {'xizmatlar': xizmatlar,})



def service_by_category(request, kategoriya):
    services = Xizmat.objects.filter(kategoriya=kategoriya)
    context = {
        'services': services,
        'kategoriya': kategoriya,
    }
    return render(request, 'services/services_by_category.html', context)






def add_santexnik_service(request):
    if request.method == 'POST':
        # Foydalanuvchi kiritgan ma'lumotlarni olish
        nomi = request.POST.get('nomi')
        tavsif = request.POST.get('tavsif')
        narx = request.POST.get('narx')
        joylashuv = request.POST.get('joylashuv')
        telefon = request.POST.get('telefon')
        kategoriya = 'Сантехник'
        rasm = request.FILES.get('rasm')

        # Yangi xizmatni saqlash
        Xizmat.objects.create(
            nomi=nomi,
            tavsif=tavsif,
            narx=narx,
            joylashuv=joylashuv,
            telefon=telefon,
            kategoriya=kategoriya,
            rasm=rasm
        )
        # Xizmat qo'shilib bo'lgach, 'santexniklar' sahifasiga yo'naltirish
        return redirect('santexniklar')  # Bu yerda 'santexniklar' URL nomini ishlatish kerak

    return render(request, 'xizmatlar/add_santexnik_service.html')









def chat_room(request, room_name):
    return render(request, 'xizmatlar/chat_room.html', {
        'room_name': room_name,
        'user': request.user
    })

@login_required
def contact_provider(request, provider_id):
    provider = get_object_or_404(User, id=provider_id)
    messages = Message.objects.filter(sender=request.user, receiver=provider) | Message.objects.filter(sender=provider, receiver=request.user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = provider
            msg.save()
            return redirect('contact_provider', provider_id=provider.id)
    else:
        form = MessageForm()

    availability = Availability.objects.filter(provider=provider)

    return render(request, 'xizmatlar/contact_provider.html', {
        'provider': provider,
        'messages': messages,
        'form': form,
        'availability': availability,
    })



def home(request):
    context = {
        'programmer_name': 'Ismingizni kiriting',  # O'zingizni ismingizni qo'shing
    }
    return render(request, 'xizmatlar/home.html', context)

def about(request):
    return render(request, 'xizmatlar/about.html')



def send_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        # Bu yerda emailni yubormaslikka qaror qilsangiz, faqat konsolga chiqarish yoki ma'lumotlarni saqlash mumkin
        print(f"Xabar: {name}, {phone}, {message}")
        
        return redirect('xizmatlar_royxati')
    return redirect('xizmatlar_royxati')



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('xizmatlar_royxati')
        else:
            print(form.errors)  # Yozib ko‘ring: qayerda xatolik borligini aniqlash uchun
    else:
        form = UserCreationForm()
    return render(request, 'xizmatlar/signup.html', {'form': form})



def delete_service(request, pk, next_url='xizmatlar_royxati'):
    service = get_object_or_404(Xizmat, pk=pk)
    if service.user != request.user:
        return HttpResponseForbidden("Siz bu xizmatni o‘chira olmaysiz!")
    service.delete()
    return redirect(next_url)
  

def delete_santexnik_service(request, pk):
    service = get_object_or_404(Xizmat, pk=pk)
    
    # Tekshiruv: faqat xizmatni yaratgan foydalanuvchi o‘chirishi mumkin
    if service.user != request.user:
        return HttpResponseForbidden("Siz bu xizmatni o‘chira olmaysiz!")
    
    service.delete()
    return redirect('santexniklar')

def xizmat_ochirish(request, xizmat_id):
    xizmat = get_object_or_404(Xizmat, id=xizmat_id)

    if xizmat.user != request.user:
        return HttpResponseForbidden("Сиз бу хизматни ўчира олмайсиз!")

    xizmat.delete()
    return redirect('xizmatlar_royxati')

def xizmatlar_royxati(request):
    qidiruv = request.GET.get('qidiruv', '')
    kategoriya = request.GET.get('kategoriya', '')  

    xizmatlar = Xizmat.objects.all().order_by('-sana')

    if qidiruv:
        xizmatlar = xizmatlar.filter(nomi__icontains=qidiruv)

    if kategoriya:
        xizmatlar = xizmatlar.filter(kategoriya__icontains=kategoriya)




    paginator = Paginator(xizmatlar, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'xizmatlar/xizmatlar_royxati.html', {
        'page_obj': page_obj,
        'qidiruv': qidiruv,
        'kategoriya': kategoriya,
    })

@login_required
def add_service(request):
    if request.method == 'POST':
        nomi = request.POST.get('nomi')
        tavsif = request.POST.get('tavsif')
        narx = request.POST.get('narx')
        joylashuv = request.POST.get('joylashuv')
        telefon = request.POST.get('telefon')
        rasm = request.FILES.get('rasm')
        kategoriya = request.POST.get('kategoriya')  

        if nomi and tavsif:
            Xizmat.objects.create(
                nomi=nomi,
                tavsif=tavsif,
                narx=narx if narx else 0,
                joylashuv=joylashuv,
                telefon=telefon,
                rasm=rasm,
                user=request.user,
                kategoriya=kategoriya  
            )
            return redirect('xizmatlar_royxati')

    return render(request, 'xizmatlar/add_service.html')



@login_required
def service_detail(request, pk):
    xizmat = get_object_or_404(Xizmat, pk=pk)
    sharhlar = xizmat.sharhlar.all()



    if request.method == 'POST':
        form = SharhForm(request.POST)
        if form.is_valid():
            yangi_sharh = form.save(commit=False)
            yangi_sharh.xizmat = xizmat
            yangi_sharh.foydalanuvchi = request.user
            yangi_sharh.save()
            return redirect('service_detail', pk=xizmat.pk)  # 'service_detail' URL nomi to'g'ri bo'lishi kerak
    else:
        form = SharhForm()

    return render(request, 'xizmatlar/service_detail.html', {
        'xizmat': xizmat,
        'sharhlar': sharhlar,
        'form': form
    })
