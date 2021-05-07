from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm
from .models import User
import speech_recognition as sr
import time
from gtts import gTTS
import os
from playsound import playsound
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
def signup_view(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect("myapp:home")
    if request.user.is_authenticated and not request.user.is_active:
        return redirect("myapp:auth")

    if request.method == 'POST':
        print(request.POST)
        file = 'test'
        i = '1'
        text1 = "Welcome to our Voice Based Email Portal. SignIn with your email account to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)
        email = introVoice('email',file,i)
        print(email)
        UserObj = User.objects.filter(email=email).first()
        print(UserObj)
        # UserObj = get_object_or_404(User, email=email)
        if(UserObj):
            texttospeech("Already Exists, Try Again", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'failure'})
        passs = introVoice('password',file,i)
        # confirmPass = introVoice('password again',file,i)
        try:
            obj = User.objects.create(email=email,password=passs)
            print(obj)
        except:
            print("Some error")
            texttospeech("There was some error, Please try again")
            return JsonResponse({'result' : 'failure'})
        # form = SignUpForm(email=email,password=passs,auth_code='1010101010')
        # if True:
        #     auth_code = '1010101010'
        #     user = authenticate(email=email, password=passs)
        #     print("************USER******=", user)
        #     print("valid")
        #     return JsonResponse({'result' : 'success'})
        # else:
        #     print(addr)
        #     print('tf')
        #     context['message'] = 'Please enter correct email and password !'
        #     # context['form'] = form
        #     return JsonResponse({'result' : 'failure'})
        if True:
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=passs)
            # login(request, user)
            return JsonResponse({'result' : 'success'})
        else:
            return JsonResponse({'result' : 'failure'})
    else:
        form = SignUpForm()
        return render(request, 'myapp/signup.html', {'form': form})


def home_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("myapp:first")


    if not user.is_active:
        return redirect("myapp:auth")

    print("--------------",user.email)
    # context['auth_code'] = user.auth_code

    context['email'] = user.email
    return render(request, 'myapp/home.html', context)

def ActionVoice():
    flag = True
    addr=''
    passs=''
    while (flag):
        texttospeech("Enter your"+email, file + i)
        i = i + str(1)
        addr = speechtotext(10)
        if addr != 'N':
            texttospeech("You meant " + addr + " say yes to confirm or no to enter again", file + i)
            
            i = i + str(1)
            say = speechtotext(10)
            print(say)
            if say == 'yes' or say == 'Yes' or say=='yes yes':
                flag = False
                addr = addr.strip()
                addr = addr.replace(' ', '')
                addr = addr.lower()
                addr = convert_special_char(addr)
                return addr
        else:
            texttospeech("could not understand what you meant:", file + i)
            i = i + str(1)

def first(request):
    context = {}

    user = request.user
    if user.is_authenticated and user.is_active:
        return redirect("myapp:home")

    if user.is_authenticated and not user.is_active:
        return redirect("myapp:auth")

    return render(request, 'myapp/first.html', context)


def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return


def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        # texttospeech("speak", file + i)
        # i = i + str(1)
        # playsound('output.mp3')
        print("Speak Now")
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
        print(response)
    except:
        response = 'N'
    return response


def convert_special_char(text):
    temp=text
    special_chars = ['dot','underscore','dollar','hash','star','plus','minus','space','dash','at the rate','attherate']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
                elif character == 'at the rate':
                    temp=temp.replace('at the rate','@')
                elif character == 'attherate':
                    temp=temp.replace('attherate','@')
    return temp.strip()

# def login_view(request):
#     context = {}
#     if request.user.is_authenticated:
#         return redirect('/')
#     if request.method == 'POST':
#         print(request.POST)
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password1')
#             auth_code = form.cleaned_data.get('auth_code')
#             user = authenticate(email=email, password=password)
#             # print("valid")
#             if user is not None and auth_code == user.auth_code:
#                 login(request, user)
#                 return redirect("myapp:home")
#             else:
#                 context['form'] = form
#
#         else:
#             try:
#                 acc = User.objects.get(email=request.POST['email'])
#
#             except User.DoesNotExist:
#                 context['message'] = 'Please enter correct email and password !'
#             context['form'] = form
#     else:
#         context['form'] = LoginForm()
#     return render(request, 'myapp/login.html', context)


def logout_view(request):
    logout(request)
    return redirect("myapp:first")


def introVoice(email,file,i):
    flag = True
    addr=''
    passs=''
    while (flag):
        texttospeech("Enter your"+email, file + i)
        i = i + str(1)
        addr = speechtotext(10)
        if addr != 'N':
            texttospeech("You meant " + addr + " say yes to confirm or no to enter again", file + i)
            
            i = i + str(1)
            say = speechtotext(10)
            print(say)
            if say == 'yes' or say == 'Yes' or say=='yes yes':
                flag = False
                addr = addr.strip()
                addr = addr.replace(' ', '')
                addr = addr.lower()
                addr = convert_special_char(addr)
                return addr
        else:
            texttospeech("could not understand what you meant:", file + i)
            i = i + str(1)
        

def login_view(request):
    context = {}
    if request.user.is_authenticated and request.user.is_active:
        return redirect("myapp:home")

    if request.user.is_authenticated and not request.user.is_active:
        return redirect("myapp:auth")

    if request.method == 'POST':
        file = 'test'
        i = '1'
        text1 = "Welcome to our Voice Based Email Portal. Login with your email account to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)

        flag = True
        addr=''
        while (flag):
            texttospeech("Enter your Email", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            if addr != 'N':
                texttospeech("You meant " + addr + " say yes to confirm or no to enter again or exit to terminate the program", file + i)
                
                i = i + str(1)
                say = speechtotext(10)
                print(say)
                if say == 'yes' or say == 'Yes' or say=='yes yes' or say=='y' or say=='Y' or say=='why':
                    flag = False
                elif say=='exit':
                    flag = False
                    time.sleep(60)
                    texttospeech("The  application will restart in a minute",file+i)
                    i=i + str(1)
                    return JsonResponse({'result': 'failure', 'message': 'message'})
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
            addr = addr.strip()
            addr = addr.replace(' ', '')
            addr = addr.lower()
            addr = convert_special_char(addr)

        account = User.objects.filter(email=addr).first()
        print("---------------->",account)

        if account:
            print("User Exists")

            flag = True
            passs = ''
            while (flag):
                texttospeech("Enter your password", file + i)
                i = i + str(1)
                passs = speechtotext(10)
                if passs != 'N':
                    texttospeech("You meant " + passs + " say yes to confirm or no to enter again", file + i)

                    i = i + str(1)
                    say = speechtotext(10)
                    print(say)
                    if say == 'yes' or say == 'Yes' or say == 'yes yes' or say=='y' or say=='Y' or say=='why':
                        flag = False
                else:
                    texttospeech("could not understand what you meant:", file + i)
                    i = i + str(1)
            passs = passs.strip()
            passs = passs.replace(' ', '')
            passs = passs.lower()
            passs = convert_special_char(passs)

            # form = LoginForm(email=addr,password=passs,auth_code='1010101010')
            # if account:
            # auth_code = '1010101010'
            user = authenticate(email=addr, password=passs)
            print("USER--------->>>", user)

            if user is not None:
                if not account.is_active:
                    print("Your account is not active, create authentication code to continue")
                    message = 'Account not active'
                    texttospeech("Your account is not active, create authentication code to continue", file + i)
                    i = i + str(1)
                    login(request, user)
                    return JsonResponse({'result': 'failure-active', 'message': message})


                login(request, user)
                return JsonResponse({'result': 'success'})
            else:
                message = 'Incorrect Password!'
                texttospeech("Please enter correct password !", file + i)
                i = i + str(1)
                return JsonResponse({'result': 'failure', 'message': message})
        else:
            print(addr,"does not exist!")
            texttospeech("Please enter correct email address!",file+i)
            i = i + str(1)
            message = 'Please enter correct email address!'
            return JsonResponse({'result': 'failure', 'message': message})
    else:
        context['form'] = LoginForm()

    return render(request, 'myapp/login.html', context)


def auth_view(request):
    if request.method=='GET':
        context = {}
        user = request.user
        print('testng')
        if not user.is_authenticated:
            return redirect("myapp:first")

        if user.is_active:
            # verify Auth Code
            print("Account already active, enter auth code")

        if not user.is_active:
            # create Auth Code
            print("Account not active, create auth code")

        print("Email address----------->", user.email)

        return render(request, 'myapp/login2.html', context)
    else:
        print("We have reached here")
        code = request.POST['authcode']
        print(code)
        
        return render(request,'myapp/login2.html')


