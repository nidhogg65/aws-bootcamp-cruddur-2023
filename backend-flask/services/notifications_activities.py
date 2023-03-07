from datetime import datetime, timedelta, timezone
from aws_xray_sdk.core import xray_recorder

class NotificationsActivities: 
    def run():
        # Start a parent subsegment
        parent_subsegment = xray_recorder.begin_subsegment('notifications_activities')
        parent_subsegment.put_annotation('URI', '/api/activities/notifications')

        now = datetime.now(timezone.utc).astimezone()

        # Start a child subsegment
        child_subsegment = xray_recorder.begin_subsegment('returning_mock_data')
        
        results = [{
            'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
            'handle':  'chen',
            'message': '2+2 = 5',
            'created_at': (now - timedelta(days=2)).isoformat(),
            'expires_at': (now + timedelta(days=5)).isoformat(),
            'likes_count': 5,
            'replies_count': 1,
            'reposts_count': 0,
            'replies': [{
                'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
                'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
                'handle':  'Worf',
                'message': 'This post has no honor!',
                'likes_count': 0,
                'replies_count': 0,
                'reposts_count': 0,
                'created_at': (now - timedelta(days=2)).isoformat()
            }],
            },
            {
            'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
            'handle':  'Garek',
            'message': 'My dear doctor, I am just simple tailor',
            'created_at': (now - timedelta(hours=1)).isoformat(),
            'expires_at': (now + timedelta(hours=12)).isoformat(),
            'likes': 0,
            'replies': []
            }
            ]

        xray_dict = {'number': len(results)}
        child_subsegment.put_metadata('notification results', xray_dict)

        # End a parent subsegment
        xray_recorder.end_subsegment()
        # End a child subsegment
        xray_recorder.end_subsegment()
        return results