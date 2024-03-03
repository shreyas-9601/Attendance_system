from django.http import StreamingHttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView

from camera import VideoCamera


class HomePageView(TemplateView):
    template_name = 'home.html'


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


class Attend(TemplateView):
    template_name = 'attend.html'
