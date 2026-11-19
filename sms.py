"""
KisanAI - SMS Alerts (OPTIONAL / FUTURE SCOPE MODULE)
----------------------------------------------------------
Sends weather/advisory alerts to a farmer's phone via SMS, using
Twilio's free trial account. This is genuinely useful for farmers
without smartphones/internet - the original proposal's core pitch.

--------------------------------------------------------------------
SETUP (5 minutes):
--------------------------------------------------------------------
1. Sign up free at https://www.twilio.com/try-twilio (no card needed
   for trial)
2. From the Twilio Console dashboard, copy:
   - Account SID
   - Auth Token
   - Your trial phone number (Twilio gives you one free)
3. Trial accounts can only send SMS to phone numbers you've verified
   in the Twilio Console (Phone Numbers -> Verified Caller IDs) -
   this is a Twilio trial limitation, not a bug in this code. To
   message farmers you haven't verified, you'd need to upgrade to a
   paid Twilio account (~$0.0079 per SMS in India).
4. Paste your 3 credentials into config.py

This module is intentionally NOT wired into the main app UI - it's a
standalone function you can call from anywhere (e.g. after generating
a weather advisory) once you've tested your Twilio setup works.
--------------------------------------------------------------------
"""

from twilio.rest import Client


def send_sms_alert(to_number, message, account_sid, auth_token,
                    from_number=None, messaging_service_sid=None):
    """
    Sends a single SMS. to_number and from_number must be in E.164
    format, e.g. "+919876543210".

    Pass EITHER from_number OR messaging_service_sid (not both) -
    a Messaging Service is Twilio's newer, recommended way to send,
    and is what you get by default with some trial accounts.

    Returns (success: bool, info: str).
    """
    try:
        client = Client(account_sid, auth_token)
        kwargs = {"body": message, "to": to_number}
        if messaging_service_sid:
            kwargs["messaging_service_sid"] = messaging_service_sid
        elif from_number:
            kwargs["from_"] = from_number
        else:
            return False, "Provide either from_number or messaging_service_sid"

        sms = client.messages.create(**kwargs)
        return True, sms.sid
    except Exception as e:
        return False, str(e)


def format_weather_alert_sms(advisory_day, lang="en"):
    """
    Turns one day's advisory (from weather.generate_advisory) into a
    short SMS-friendly string. SMS should stay under ~160 chars where
    possible to avoid multi-part message charges.
    """
    header = "KisanAI Alert" if lang == "en" else "KisanAI Salah"
    messages = " | ".join(advisory_day["messages"])
    return f"{header} ({advisory_day['date']}): {messages}"