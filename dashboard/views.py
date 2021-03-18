from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time
import datetime
import redis
import json
from django.http import StreamingHttpResponse,HttpResponse



r = redis.StrictRedis('localhost', 6379, 0, charset='utf-8', decode_responses=True)





# Create your views here.

def dashboard(request):
    return render(request,
                  'index.html',
                  {'section': 'dashboard','serviceList':['Impala Service','Hadoop Service']})


# @csrf_exempt
# def publish(request):
#     print(request)
#     now = datetime.datetime.now().replace(microsecond=0).time()
#     r.publish('chat', '[%s] : %s' % (now.isoformat(), ""))
#     return HttpResponse(status=204)

def event_stream():
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe('Messages')
    # TODO: handle client disconnection.
    for message in pubsub.listen():
        message=json.loads(message['data'])
        yield 'id:%s\nevent:%s\ndata: %s\n\n' % (1,message['event'],message['msg'])

@csrf_exempt
def lastUpdated(request):
    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    # def event_stream():
    #     while True:
    #         time.sleep(1)
    #         yield 'id:%s\nevent:updated\ndata: %s\n\n' % (1,str(datetime.datetime.now().strftime('%s')))
    # return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


@csrf_exempt
def publish(request):
    while True:
        time.sleep(1)
        now = datetime.datetime.now().replace(microsecond=0).time()
        msg={'event':'updated'
            ,'time':str(now.isoformat())
            ,'msg':str(datetime.datetime.now().strftime('%s'))}
        # yield 'id:%s\nevent:updated\ndata: %s\n\n' % (1,str(datetime.datetime.now().strftime('%s')))
        r.publish('Messages', json.dumps(msg))
        print(json.dumps(msg))
    return HttpResponse(status=204)
