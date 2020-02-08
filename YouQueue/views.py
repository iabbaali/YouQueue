from django.shortcuts import render, redirect
from YouQueue.models import Song
from YouQueue import YTAPI_filter
from django.http import JsonResponse
songs = []
top = 0


def submit(request):
    if len(Song.objects.filter(active=True)) >= 1:
        show_songs = True
    else:
        show_songs = False

    if request.method == "GET":
        url = request.GET.get("submit")
        if url != None:
            api_url = YTAPI_filter.build_url(YTAPI_filter.get_video_id(url))
            info = YTAPI_filter.parse_result(YTAPI_filter.get_contents(api_url))
        # create song object
            song = Song()
            song.title = YTAPI_filter.get_title(info)
            song.thumbnail = YTAPI_filter.get_thumbnail(info)
            song.votes = 0
            song.vid = YTAPI_filter.get_video_id(url)
            song.url = url
            song.save()
            song.duration = YTAPI_filter.get_duration(info)
            print(str(song))
            songs.append(song)
            return redirect('thelist')
    return render(request, 'submit.html', context={"show_songs": show_songs})


def thelist(request):
    current_songs = Song.objects.filter(active=True)
    for song in current_songs:
        print(song.title, song.active)
    if len(current_songs) > 1:
        not_first = current_songs[1:]
    else:
        not_first = None
    if request.method == "GET":
        url = request.GET.get("submit")
        if url != None:
            api_url = YTAPI_filter.build_url(YTAPI_filter.get_video_id(url))
            info = YTAPI_filter.parse_result(YTAPI_filter.get_contents(api_url))
            # create song object
            song = Song()
            song.title = YTAPI_filter.get_title(info)
            song.thumbnail = YTAPI_filter.get_thumbnail(info)
            song.votes = 0
            song.vid = YTAPI_filter.get_video_id(url)
            song.url = url
            song.duration = YTAPI_filter.get_duration(info)
            song.save()
    return render(request, 'queue.html', context={"songs": current_songs, "not_first": not_first})


def upvote(request):
    thisvid = request.GET.get('vid', None)
    thisSong = Song.objects.get(vid=thisvid)
    thisSong.votes += 1
    thisSong.save()
    print(thisSong.title, 'votes:', thisSong.votes)
    res = {
        "newVotes": thisSong.votes
    }
    return JsonResponse(res)


def downvote(request):
    thisvid = request.GET.get('vid', None)
    thisSong = Song.objects.get(vid=thisvid)
    thisSong.votes -= 1

    print(thisSong.title, 'votes:', thisSong.votes)
    if thisSong.votes <= -2:
        thisSong.active = False
    thisSong.save()
    res = {
        "newVotes": thisSong.votes
    }
    return JsonResponse(res)
