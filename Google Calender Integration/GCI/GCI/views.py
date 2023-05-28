from django.shortcuts import redirect
from django.views import View
from django.http import HttpResponse 
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar. maagereadonly']
REDIRECT_URI = 'http://your-redirect-url.com/rest/v1/calendar/redirect/'  # Replace with your actual redirect URL

class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'C:\\Users\\vaibh\\Desktop\\Google Calender Integration\\client_secret.json',  # Replace with the path to your client secrets JSON file
            SCOPES,
            redirect_uri=REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        request.session['state'] = state
        return redirect(authorization_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session.pop('state', None)
        if state is None or state != request.GET.get('state', ''):
            return redirect('google_calendar_init')

        flow = InstalledAppFlow.from_client_secrets_file(
            'path/to/client_secrets.json',  # Replace with the path to your client secrets JSON file
            SCOPES,
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(
            authorization_response=request.build_absolute_uri(),
        )
        credentials = flow.credentials

        service = build('calendar', 'v3', credentials=credentials)
        events = service.events().list(calendarId='primary').execute()

        # Process the events as per your requirements

        return HttpResponse('Events fetched successfully')
