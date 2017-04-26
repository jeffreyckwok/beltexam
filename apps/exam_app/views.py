from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
from django.db.models import Count
import datetime


# Create your views here.
def index(request):
    return render(request, 'exam_app/index.html')

def register(request):
    context = {
    'fname': request.POST['first_name'],
    'lname': request.POST['last_name'],
    'pw': request.POST['password'],
    'conf_pw': request.POST['confirm_password'],
    'em': request.POST['email'],
    }
    regResults = User.objects.validateReg(context)

    if regResults['new'] != None:
        request.session['user_id'] = regResults['new'].id
        request.session['user_firstname'] = regResults['new'].first_name
        return redirect('/success')
    else:
        for error_str in regResults['error_list']:
            messages.add_message(request, messages.ERROR, error_str)
        return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')
    else:
        my_trips = Trip.objects.filter(user_id=request.session['user_id'])
        other_trips = Trip.objects.all().exclude(user_id=request.session['user_id'])
        print my_trips
        context = {
        'my_trips': my_trips,
        'other_trips': other_trips
        }
        return render(request, 'exam_app/travels.html', context)

def login(request):
    userLog = {
        'loginEmail': request.POST['email'],
        'loginPw': request.POST['password']
    }

    login_results = User.objects.userLogin(userLog)

    if login_results['list_errors'] != None:
        for error in login_results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['user_id'] = login_results['logged_user'].id
        request.session['user_firstname'] = login_results['logged_user'].first_name
        return redirect ('/success')

def logout(request):
	request.session.clear()
	return redirect('/')

def add(request):
    return render(request, 'exam_app/add.html')

def addtrip(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
     'user_id': user,
     'destination': request.POST['destination'],
     'plan': request.POST['description'],
     'travelstart': request.POST['datefrom'],
     'travelend': request.POST['dateto'],
    }
    newtrip = Trip.objects.addTrip(context)

    if newtrip['new'] != None:
        return redirect('/success')
    else:
        for error_str in newtrip['error_list']:
            messages.add_message(request, messages.ERROR, error_str)
        return redirect('/add')

def viewdestination(request, id):
    this_destination = Trip.objects.filter(id=id)
    destinfo = {
    'destination_info': this_destination,
    }
    return render(request, 'exam_app/destination.html', destinfo)

def jointrip(request, id):
    join_id = int(id)
    join_user = User.objects.get(id=request.session['user_id'])
    trip_join = Trip.objects.get(id=join_id)
    context = {
    'tripuser': int(request.session['user_id']),
    'tripid': join_id
    }
    validation = Trip.objects.tripJoin(context)
    return redirect('/success')
