from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from fraud_detection_app.models import Person, Account, Transaction, FraudCase, userResponse
from fraud_detection_app.algo import predict_fraud
from django.http import JsonResponse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import send_mail
import random
import uuid

def transferAmount(request):
    sender_user_id=request.session.get('user_data', None)['user_id']
    receiver_user_id=request.GET.get('to')
    amount=request.GET.get('amount')
    senderAccount = None
    receiverAccount=None
    try:
        senderAccount=Account.objects.get(user_id=sender_user_id)
    except Account.DoesNotExist:
        print('Sender account does not exist')
        return JsonResponse({'message': 'Sender Account not exist'})
    try:
        receiverAccount=Account.objects.get(user_id=receiver_user_id)
    except Account.DoesNotExist:
        print('Sender account does not exist')
        return JsonResponse({'message': 'Sender Account not exist'})

    transaction=Transaction(
        to_user_id=receiver_user_id,
        from_user_id=sender_user_id,
        from_user_account_id=senderAccount.account_number,
        to_user_account_id=receiverAccount.account_number,
        amount=int(amount)
    )
    transaction.save()
    isFraud = predict_fraud(sender_user_id, receiver_user_id)
    if isFraud=='Fraud':
        fraud=FraudCase(
            transaction_id=transaction.pk,
            description='description',
            isfraud=1
        )
        fraud.save()
        print(f"The transaction is: {isFraud}")
        return JsonResponse({'message': 'true'})
    else :
        fraud=FraudCase(
            transaction_id=transaction.pk,
            description='kkkkkkkkkk',
            isfraud=0
        )
        fraud.save()
        if int(amount) < int(senderAccount.balance):
            senderAccount.balance -= int(amount)
            receiverAccount.balance +=int(amount)
            senderAccount.save()
            receiverAccount.save()
        return JsonResponse({'message': ''})

def sendOTPHelper(email,mesg,sub):
    print(email,mesg,sub)
    # Send the OTP via email
    subject = sub
    message = mesg
    from_email = 'aastha042003@gmail.com'  # Use the email you configured
    recipient_list = [email]  # Replace with the user's email
    send_mail(subject, message, from_email, recipient_list)

def sendOTP(req):
    otp = random.randint(1, 100)
    # Send the OTP via email
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'
    from_email = 'aastha042003@gmail.com'  # Use the email you configured
    recipient_list = [req.GET.get('email')]  # Replace with the user's email
    send_mail(subject, message, from_email, recipient_list)
    return JsonResponse({'otp': otp})

def loginPage(request):
    email = ""
    password = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

    elif request.method == 'GET':
        email = request.GET.get('email')
        password = request.GET.get('password')
        print(
            f'email----------------> "{email}" password-------------> "{password}"')
        # Authenticate the user
    try:
        if email is None or password is None:
            return render(request, 'login.html')
        # Query the database to retrieve the user
        user = Person.objects.get(email=email, password=password)

        # Login successful, create a session and store user data
        print(user)
        try:
            print('jjjjj')
            accounts = Account.objects.filter(user_id=user.user_id)
            print(accounts)
            for account in accounts:
                # 'account' is now each individual account object
                # You can access its attributes, perform operations, or print its data
                print(f"Account Number: {account.account_number}")
                print(f"IFSC: {account.ifsc}")

            print(accounts)
        except Exception:
            print('no account found')
            print(Exception)
            return render(request, 'login.html')

        # Fetch additional data from the database for the authenticated user
        user_data = {
            'email': user.email,
            'name': user.name,
            'user_id': user.user_id,
            'user_logged_out': False
            # Add more user-related information as needed
        }
        print(user_data)
        # Store the user data in the session
        request.session['user_data'] = user_data

        # Redirect to the home page after successful login
        return render(request, 'firstL.html', {'': ''})
    except Person.DoesNotExist:
        print('USer does not exist please try again-------------')
        # Login failed, handle the error
        return render(request, 'login.html', {'error_message': 'Invalid email or password'})

    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    request.session['user_logged_out'] = True
    # del request.session['user_data']
    return redirect('/login')


def homePage(request):
    # check if user session is maintain then only show this page otherwise on session expre redirect to login Page
    user_data = request.session.get('user_data', None)
    if user_data is not None:
        print(user_data)
        account=Account.objects.filter(user_id=user_data['user_id'])
        print(account)
        return render(request, 'firstL.html', {'account': account})
    else:
        logout(request)
        request.session['user_logged_out'] = True
        del request.session['user_data']
        return redirect('/login/')



def home(request):
    return render(request, 'home.html', {'': ''})


@csrf_exempt
def saveUser(request):
    person = Person(
        name = request.POST.get('name'),
        email = request.POST.get('email'),
        password = generate_numeric_uuid(8),
        address = request.POST.get('address'),
        pincode = request.POST.get('pincode'),
        mobile_no = request.POST.get('mobile_no'),
    )
    try:
        print('')
        person.save()
        msg=f'Hii {person.name} your user id is {person.pk} and password is {person.password}  use your email id {person.email} to login'
        sendOTPHelper(person.email,msg,'Grab your details')
        return render(request, 'login.html', {'': ''})
    except Exception as e:
        print(e)
        return render(request, 'register.html', {'message': 'Something Went Wrong Please Try Again'})


def register(request):
    return render(request, 'register.html', {'': ''})


def sendMoney(req):
    # there is mode based on which and session attribute show specific page
    accounts = None
    transactions = None
    user_data = req.session.get('user_data', None)
    if user_data is not None:
        print(user_data['user_id'])
        user_id = user_data['user_id']
        accounts = Account.objects.filter(user_id=user_id)
    context = {
        'accounts': accounts
    }
    print(context)
    return render(req, 'sendmoney.html', context)


def showAccountDetails(req):
    # there is mode based on which show detail of saving and current account details
    accounts = None
    transactions = None
    user_data = req.session.get('user_data', None)
    mode = req.GET.get('type')
    if user_data is not None:
        print(user_data['user_id'])
        user_id = user_data['user_id']
        accounts = Account.objects.filter(user_id=user_id)
        if accounts is not None:
            for account in accounts:
                print(f"Account Number: {account.account_number}")
                print(f"IFSC: {account.ifsc}")

        if mode=='c':
            mode="Current"
        else:
            mode="Savings"
        # Get Transaction Details
        transactions = Transaction.objects.filter(from_user_id=user_id)
        for transaction in transactions:
            print(f"Transaction id : {transaction.transaction_id}")

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'type':mode
    }
    print(context)
    return render(req, 'showaccountdetail.html', context)


def feedback(req):
    # there is mode based on which sget suggestion complain feedback
    message = "s"
    type = "Suggestion"
    try:
        mode = req.GET.get('type')
        print(f"Feedback Mode -------------------> {req.GET.get('type')}")
    except Exception:
        print(Exception)
    if mode == 's':
        message = "Please Provide Your Valuable Suggestion"
        type = "Suggestion"
    elif mode == 'f':
        message = "Please Provide Your Valuable Feedback"
        type = "Feedback"
    else:
        message = "We are heartily regret for bearing."
        type = "Complain"
    context = {
        'message': message,
        'type': type
    }
    print(context)
    return render(req, 'feedback.html', context)


def saveFeedback(req):
    name = ""
    email = ""
    experience = ""
    Feedback = ""
    user_id = 0
    try:
        user_data = req.session.get('user_data', None)
        if user_data is not None:
            print(user_data['user_id'])
            user_id = user_data['user_id']
        print(req.GET)
        name = req.GET.get('name')
        email = req.GET.get('email')
        experience = req.GET.get('experience')
        Feedback = req.GET.get('Feedback')
        print(f'{name} {email} {experience} {Feedback}')
        user_response = userResponse(
            user_id=user_id,
            name=name,
            email=email,
            rating=experience,
            response=Feedback
        )
        # Save the instance to the database
        user_response.save()
    except Exception as e:
        print(e)
        print(Exception.with_traceback)
        return JsonResponse({'message': 'Something went wrong. Please Try Again!!!'})
    data = {'message': 'Data persist successfully.'}
    return JsonResponse(data)

def autoFill(req):
    list=[]
    search_term=req.GET.get('input')
    if search_term is not None:
        try:
            # Use the icontains lookup to perform a partial string match
            accounts = Account.objects.filter(account_number__icontains=search_term)
            account_numbers = [account.account_number for account in accounts]
            return JsonResponse(account_numbers, safe=False)
        except Account.DoesNotExist:
            return JsonResponse([], safe=False)
    else:
        return JsonResponse([], safe=False)

def fromAccountGetDetails(req):
    search_term=req.GET.get('input')
    data = {}
    if search_term is not None:
        try:
            # Use the icontains lookup to perform a partial string match
            account = Account.objects.filter(account_number=search_term)
            print(account)
            user_id=0
            accn=0
            IFSC=0
            name=0
            email=0
            address=0
            pin=0
            mobile_no=0
            for acc in account:
                print(acc.account_number,acc.user_id)
                user_id=acc.user_id
                accn=acc.account_number
                IFSC=acc.ifsc
                addr=acc.address
            us = Person.objects.filter(user_id=user_id).first()

            print(us)
            name=us.name
            email=us.email
            address=us.address
            pin=us.pincode
            mobile_no=us.mobile_no
            data = {
                'name': name,
                'email': email,
                'address': address,
                'pincode': pin,
                'mobile_no': mobile_no,
                'account_number': accn,
                'ifsc': IFSC,
                'state': addr,
                'user_id':us.user_id
            }
            return JsonResponse(data)
        except Exception as e:
            print(e)
            return JsonResponse(data)
    else:
        return JsonResponse(data)

def addRecipent(req):
    print(req.session.get('user_data', None))
    return render(req,'addreceipeint.html',{})


def generate_numeric_uuid(length):
    # Generate a random numeric UUID of the specified length
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def openAccount(req):
    #check is already bank exist if exits revert back otherwise open new account
    try:
        user_id=93
        user_data = req.session.get('user_data', None)
        if user_data is not None:
            print(user_data)
            user_id = user_data['user_id']
        print(req.GET)
        account= Account(
            account_number= generate_numeric_uuid(12),
            balance = 0,
            user_id = user_id,
            ifsc = generate_numeric_uuid(8),
            bank_user_id = generate_numeric_uuid(6),
            nominee = req.GET.get('nominee'),
            state = req.GET.get('state'),
            address = req.GET.get('address')
        )
        email=user_data['email']
        msg=f'<h1>Aastha Banking app::</h1> Account number : {account.account_number} IFSC:{account.ifsc} Bank User ID: {account.bank_user_id}'
        sub='Your Details Please save it'
        try:
            sendOTPHelper(email,msg,sub)
        except Exception as e:
            import traceback
            traceback.print_exc()

        account.save()
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        print(Exception.with_traceback)
        return render(req,'addBank.html',{})
    return redirect('/home/')

def withdrawl(req):
    withdrawAmount=req.GET.get('withdrawAmount')
    account_number=req.GET.get('accountNumber')
    try:
        accounts = Account.objects.get(account_number=account_number)
    except Exception as e:
        print(e)
        return JsonResponse({'message' : 'Account not found with given number'})

    temp=int(withdrawAmount)
    if  accounts.balance>=temp:
        accounts.balance -= int(withdrawAmount)
        accounts.save()
        return JsonResponse({'message' : 'sucessfully withdrawl'})
    else :
        return JsonResponse({'message': 'Insufficient Balance'})

def deposite(req):
    withdrawAmount=req.GET.get('depositAmount')
    account_number=req.GET.get('accountNumber')
    try:
        accounts = Account.objects.get(account_number=account_number)
        print(accounts)
    except Exception as e:
        print(e)
        return JsonResponse({'message' : 'Account not found with given number'})

    accounts.balance += int(withdrawAmount)
    accounts.save()
    return JsonResponse({'message' : 'sucessfully Deposit amount!!!'})



def renderDeposit(req):
    return render(req, 'deposit.html', {})

def renderWithr(req):
    return render(req, 'withdrawl.html', {})

