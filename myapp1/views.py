from django.shortcuts import render
from django.http import JsonResponse
import requests
import os

# Create your views here.

def index(request):
    return render(request, 'index.html')

titles = 5
after_file = "after.txt"
last_community_file = "last_community.txt"

def get_after():
    if os.path.exists(after_file):
        with open(after_file, "r") as file:
            return file.read().strip()
    return None

def save_after(after):
    with open(after_file, "w") as file:
        file.write(after)

def get_last_community():
    if os.path.exists(last_community_file):
        with open(last_community_file, "r") as file:
            return file.read().strip()
    return None

def save_last_community(community):
    with open(last_community_file, "w") as file:
        file.write(community)

def fetch_reddit_titles(subname, after=None):
    result_titles = []
    url = f"https://www.reddit.com/r/{subname}/new.json?sort=new&limit={titles}"
    if after:
        url += f"&after={after}"
        
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    
    if response.status_code == 200:
        data = response.json()
        for post in data['data']['children']:
            result_titles.append(post['data']['title'])

        new_after = data['data']['after']
        if new_after:
            save_after(new_after)
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
    
    return result_titles

def fetch_titles(request):
    if request.method == 'POST':
        subname = request.POST.get('community')
        last_community = get_last_community()
        
        if last_community != subname:
            save_after("")
            save_last_community(subname)
        
        after = get_after()
        titles_list = fetch_reddit_titles(subname, after)
        return JsonResponse(titles_list, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)