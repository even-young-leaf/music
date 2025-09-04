from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Song, Label, Dynamic

@require_http_methods(["GET"])
def index_data_api(request):
    """
    首页数据API，提供给Vue前端使用
    """
    # 热搜歌曲
    search_songs = Dynamic.objects.select_related('song').order_by('-search').all()[:8]
    # 音乐分类
    labels = Label.objects.all()
    # 热门歌曲
    popular_songs = Dynamic.objects.select_related('song').order_by('-plays').all()[:10]
    # 新歌推荐
    recommend_songs = Song.objects.order_by('-release').all()[:10]
    # 热门下载
    download_songs = Dynamic.objects.select_related('song').order_by('-download').all()[:6]
    
    # 构建返回数据
    data = {
        'searchs': [
            {
                'id': item.song.id,
                'name': item.song.name,
                'singer': item.song.singer,
                'searches': item.search
            } for item in search_songs
        ],
        'labels': [
            {
                'id': label.id,
                'name': label.name
            } for label in labels
        ],
        'popular': [
            {
                'id': item.song.id,
                'name': item.song.name,
                'singer': item.song.singer,
                'plays': item.plays,
                'img': item.song.img.url if item.song.img else None
            } for item in popular_songs
        ],
        'recommend': [
            {
                'id': song.id,
                'name': song.name,
                'singer': song.singer,
                'release': song.release.strftime('%Y-%m-%d') if song.release else None,
                'img': song.img.url if song.img else None
            } for song in recommend_songs
        ],
        'downloads': [
            {
                'id': item.song.id,
                'name': item.song.name,
                'singer': item.song.singer,
                'downloads': item.download
            } for item in download_songs
        ]
    }
    
    return JsonResponse(data)

@require_http_methods(["GET"])
def ranking_data_api(request, type_name):
    """
    排行榜数据API，提供给Vue前端使用
    type_name: plays, downloads, searches
    """
    if type_name not in ['plays', 'download', 'search']:
        return JsonResponse({'error': 'Invalid ranking type'}, status=400)
    
    # 根据类型获取排行数据
    field_map = {
        'plays': '-plays',
        'download': '-download',
        'search': '-search'
    }
    
    ranking_data = Dynamic.objects.select_related('song').order_by(field_map[type_name]).all()[:20]
    
    # 构建返回数据
    data = [
        {
            'id': item.song.id,
            'name': item.song.name,
            'singer': item.song.singer,
            'plays': item.plays,
            'downloads': item.download,
            'searches': item.search,
            'img': item.song.img.url if item.song.img else None
        } for item in ranking_data
    ]
    
    return JsonResponse(data, safe=False)

@require_http_methods(["GET"])
def play_song_api(request, song_id):
    """
    歌曲播放页数据API，提供给Vue前端使用
    """
    try:
        # 获取歌曲信息
        song = Song.objects.get(id=song_id)
        dynamic = Dynamic.objects.get(song_id=song_id)
        
        # 增加播放次数
        dynamic.plays += 1
        dynamic.save(update_fields=['plays'])
        
        # 构建返回数据
        data = {
            'song': {
                'id': song.id,
                'name': song.name,
                'singer': song.singer,
                'album': song.album,
                'release': song.release.strftime('%Y-%m-%d') if song.release else None,
                'language': song.language,
                'type': song.type,
                'img': song.img.url if song.img else None,
                'file': song.file.url if song.file else None,
                'plays': dynamic.plays,
                'downloads': dynamic.download,
                'searches': dynamic.search
            },
            'lyrics': song.lyrics,
            'comments': []  # 评论功能可以在后续实现
        }
        
        return JsonResponse(data)
    except (Song.DoesNotExist, Dynamic.DoesNotExist):
        return JsonResponse({'error': 'Song not found'}, status=404)

@require_http_methods(["GET"])
def search_api(request):
    """
    搜索API，提供给Vue前端使用
    """
    keyword = request.GET.get('kword', '')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    if not keyword:
        return JsonResponse({'songs': [], 'total_pages': 0})
    
    # 搜索歌曲
    songs = Song.objects.filter(name__icontains=keyword) | \
            Song.objects.filter(singer__icontains=keyword) | \
            Song.objects.filter(album__icontains=keyword)
    
    # 计算总页数
    total_count = songs.count()
    total_pages = (total_count + page_size - 1) // page_size
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    songs_page = songs[start:end]
    
    # 更新搜索次数
    for song in songs_page:
        try:
            dynamic = Dynamic.objects.get(song_id=song.id)
            dynamic.search += 1
            dynamic.save(update_fields=['search'])
        except Dynamic.DoesNotExist:
            pass
    
    # 构建返回数据
    data = {
        'songs': [
            {
                'id': song.id,
                'name': song.name,
                'singer': song.singer,
                'album': song.album,
                'time': song.time,
                'img': song.img.url if song.img else None,
                'file': song.file.url if song.file else None
            } for song in songs_page
        ],
        'total_pages': total_pages
    }
    
    return JsonResponse(data)